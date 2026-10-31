"""Aynı altı girdide GRU ve nedensel CNN ardından GRU karşılaştırması."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd
import torch
from torch import nn
from yenibot.experiment.advisor_checkpoint_selection import (
    DESIGN as BASE_DESIGN, train_fold, split_validation, run_signature,
    validate_completed, verify_reference_runtime, coverage_threshold, decision_counts)
from yenibot.experiment.advisor_storage import immutable_json, sha256
from yenibot.training.advisor_models import SingleEncoder

DESIGN = dict(BASE_DESIGN, version=1, selectors=['bce'], architectures=['gru','cnn_gru'],
              cnn=dict(channels=32,kernel_size=3,activation='GELU',padding='left_only'),
              trajectories=228)


class CnnGru(nn.Module):
    def __init__(self, n_features, settings):
        super().__init__()
        self.conv=nn.Conv1d(n_features,32,3,padding=0)
        self.activation=nn.GELU()
        self.recurrent=SingleEncoder(32,'gru',settings)

    def encode_local(self,x):
        return self.activation(self.conv(nn.functional.pad(x.transpose(1,2),(2,0)))).transpose(1,2)

    def forward(self,x,*,return_logits=False):
        return self.recurrent(self.encode_local(x),return_logits=return_logits)


def model_factory(architecture):
    if architecture=='gru': return lambda n,s:SingleEncoder(n,'gru',s)
    if architecture=='cnn_gru': return CnnGru
    raise ValueError('Bilinmeyen mimari')


def architecture_signature(study,architecture):
    if architecture not in DESIGN['architectures']:raise ValueError('Bilinmeyen mimari')
    return hashlib.sha256(f'{study}:{architecture}'.encode()).hexdigest()


def report(root,signature,*,comparisons=None,archive_name='cnn_gru_review.zip',description=None):
    comparisons = comparisons or {a:(root/'runs'/a,architecture_signature(signature,a)) for a in DESIGN['architectures']}
    labels=list(comparisons)
    if len(labels)!=2:raise ValueError('İki karşılaştırma gerekli')
    records=[]; predictions=[]; identities={}
    for architecture,(run_root,run_identity) in comparisons.items():
        for seed in (42,43,44):
            for fold in range(38):
                folder=run_root/f'seed_{seed}'/f'fold_{fold:03d}'
                sig=run_signature(run_identity,seed,fold)
                if not validate_completed(folder,sig):raise ValueError('228 eğitimin tamamlanması gerekli')
                info=json.loads((folder/'metrics.json').read_text())
                if set(info['results'])!={'bce'}:raise ValueError('Yalnız BCE seçimi bekleniyor')
                sel=pd.read_parquet(folder/'bce_selection.parquet')
                val=pd.read_parquet(folder/'bce_assessment.parquet')
                if len(sel)!=465 or len(val)!=465:raise ValueError('Örnek sayısı uyuşmuyor')
                identity=(tuple(sel.timestamp),tuple(sel.label),tuple(val.timestamp),tuple(val.label))
                key=(seed,fold)
                if key in identities and identities[key]!=identity:raise ValueError('Eşleşen veri/etiket bekleniyor')
                identities[key]=identity
                predictions.append(val.assign(architecture=architecture,seed=seed,fold=fold))
                thresholds={'fixed_050':.5,**{f'selection_top{int(c*100)}':coverage_threshold(sel.probability,c) for c in (.05,.1)}}
                for policy,threshold in thresholds.items():
                    r=info['results']['bce']
                    records.append(dict(architecture=architecture,seed=seed,fold=fold,policy=policy,
                        threshold=threshold,epoch=r['epoch'],bce=r['assessment']['bce'],ap=r['assessment']['average_precision'],
                        **decision_counts(val.label,val.probability,threshold)))
    out=root/'reports';out.mkdir(exist_ok=True)
    table=pd.DataFrame(records);table.to_csv(out/'by_run.csv',index=False)
    grouped=table.groupby(['architecture','policy'])
    summary=grouped[['signals','tp','positives','samples']].sum()
    summary['precision']=summary.tp/summary.signals.replace(0,np.nan)
    summary['recall']=summary.tp/summary.positives
    summary['f1']=2*summary.tp/(summary.signals+summary.positives)
    summary['signal_rate']=summary.signals/summary.samples
    summary['no_signal_runs']=grouped.signals.apply(lambda s:int((s==0).sum()))
    summary[['bce_mean','ap_mean']]=grouped[['bce','ap']].mean()
    summary.to_csv(out/'summary.csv')
    table[table.architecture==labels[0]].merge(table[table.architecture==labels[1]],
        on=['seed','fold','policy'],suffixes=('_'+labels[0],'_'+labels[1]),validate='one_to_one').to_csv(out/'paired.csv',index=False)
    pd.concat(predictions).to_parquet(out/'assessment_predictions.parquet',index=False)
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for arch in labels:
        g=table[(table.architecture==arch)&(table.policy=='selection_top5')].groupby('fold')[['tp','signals','samples']].sum()
        axes[0].plot(g.index,100*g.tp/g.signals.replace(0,np.nan),label=arch)
        axes[1].plot(g.index,100*g.signals/g.samples,label=arch)
    for ax in axes:ax.set_xlabel('Dönem (fold)');ax.grid(alpha=.2);ax.legend()
    axes[0].set_ylabel('Precision (%)');axes[1].set_ylabel('Gerçekleşen sinyal oranı (%)')
    fig.suptitle('Seçim bölümündeki üst %5 eşiğiyle sonraki validation bölümü')
    fig.savefig(out/'comparison.png',dpi=150);plt.close(fig)
    (out/'README.md').write_text((description or '228 eğitim; yalnız seçim BCE ile epoch seçimi. Eşikler seçim bölümünden gelir. ')+
        'Değerlendirme: bölüm başına 465 hedef. Tarihsel validation; final test değildir. '
        'Seed ve dönemler bağımsız işlemler değildir. Otomatik kazanan yok. Ağırlıklar runs klasöründe.\n',encoding='utf-8')
    with zipfile.ZipFile(out/archive_name,'w',zipfile.ZIP_DEFLATED) as z:
        for parent in ['runs','reports','artifacts','reproducibility']:
            for p in sorted((root/parent).rglob('*')):
                if p.is_file() and p.suffix in {'.csv','.json','.md','.parquet','.png'}:z.write(p,p.relative_to(root).as_posix())
        for label,(run_root,_) in comparisons.items():
            if not run_root.is_relative_to(root):
                for p in sorted(run_root.rglob('*')):
                    if p.is_file() and p.suffix in {'.csv','.json','.parquet'}:z.write(p,'control_runs/'+label+'/'+p.relative_to(run_root).as_posix())
    print(summary.to_string());print('İnceleme ZIP:',out/archive_name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report'])
    parser.add_argument('--source',type=Path,required=True);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve();root=args.root.resolve()
    if root==source or root.is_relative_to(source) or source.is_relative_to(root):raise ValueError('Ayrı çalışma alanı gerekli')
    from yenibot.experiment.advisor_feature_comparison import verified
    from yenibot.experiment.advisor_learning_rate import one_run
    from yenibot.experiment.advisor_runtime import runtime_identity,freeze_workspace_identity
    from yenibot.experiment.advisor_workspace import REPO
    from yenibot.training import advisor as engine
    from yenibot.training.walk_forward import PurgedWalkForwardCV
    import sys,sklearn
    cfg=verified(source);protocol=json.loads((one_run(source,'A')/'protocol.json').read_text())
    if protocol['config']!=cfg or protocol['experiment']!='A':raise ValueError('A6 kaynak kimliği uyuşmuyor')
    for path,digest in protocol['source_hashes'].items():
        if sha256(REPO/path.split('/advisor_feature_comparison_repo/')[1])!=digest:raise ValueError('Sabit motor değişmiş')
    if cfg['training']['learning_rate']!=.001 or cfg['training']['patience']!=15 or cfg['model']['seq_len']!=64:raise ValueError('Kontrol koşulları değişmiş')
    identity=runtime_identity(REPO,require_gpu=True,hardware='selective-a100')
    verify_reference_runtime(protocol,dict(python=sys.version,torch=torch.__version__,numpy=np.__version__,
        pandas=pd.__version__,sklearn=sklearn.__version__,gpu=torch.cuda.get_device_name(0),
        cuda=torch.version.cuda,cudnn=torch.backends.cudnn.version()))
    root.mkdir(parents=True,exist_ok=True);freeze_workspace_identity(REPO,root,identity)
    immutable_json(root/'artifacts/design.json',DESIGN);immutable_json(root/'artifacts/control.json',protocol)
    signature=hashlib.sha256(''.join(sha256(root/p) for p in ['reproducibility/workspace_identity.json','artifacts/design.json','artifacts/control.json']).encode()).hexdigest()
    frame=pd.read_parquet(cfg['data']['frame']);features=protocol['features']
    folds=list(PurgedWalkForwardCV(**cfg['walk_forward'],label_horizon_bars=10).split(len(frame)))
    if len(folds)!=38 or len(features)!=6:raise ValueError('38 fold ve altı özellik gerekli')
    for fold in folds:
        sel,assessment=split_validation(fold.val)
        engine.audit_boundary(frame,fold.train,sel,10);engine.audit_boundary(frame,sel,assessment,10)
    with engine.exclusive_run(root):
        if args.action=='prepare':print('A6 doğrulandı: 2 mimari × 38 fold × 3 seed; eğitim henüz başlatılmadı.')
        elif args.action=='train':
            for arch in DESIGN['architectures']:
                for seed in (42,43,44):
                    for fold in folds:
                        print(f'Mimari: {arch}',flush=True)
                        train_fold(frame,fold,cfg,features,seed,root/'runs'/arch/f'seed_{seed}'/f'fold_{fold.fold:03d}',
                            run_signature(architecture_signature(signature,arch),seed,fold.fold),torch.device('cuda'),
                            model_factory=model_factory(arch),selectors=('bce',))
        else:report(root,signature)


if __name__=='__main__':main()
