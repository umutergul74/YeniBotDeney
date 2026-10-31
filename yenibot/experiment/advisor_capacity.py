"""GRU hidden128 kontrolüne karşı yalnız hidden64; eski kontrol salt okunur."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from yenibot.experiment import advisor_cnn_gru as previous
from yenibot.experiment.advisor_checkpoint_selection import train_fold,split_validation,run_signature,validate_completed,verify_reference_runtime
from yenibot.experiment.advisor_storage import immutable_json,sha256

CONTROL_COMMIT='dafcb21aa65883c7dc5c53d77a934e0cce565f55'
DESIGN=dict(previous.BASE_DESIGN,selectors=['bce'],changed_factor='gru_hidden',control_hidden=128,
            candidate_hidden=64,new_trajectories=114,reused_trajectories=114)


def study_signature(root):
    return hashlib.sha256(''.join(sha256(root/p) for p in ['reproducibility/workspace_identity.json','artifacts/design.json','artifacts/control.json']).encode()).hexdigest()


def candidate_config(cfg):
    if cfg['model']['gru_hidden']!=128:raise ValueError('Kontrol GRU hidden128 olmalı')
    candidate=copy.deepcopy(cfg);candidate['model']['gru_hidden']=64
    return candidate


def verify_control(control,protocol,current_runtime):
    identity=json.loads((control/'reproducibility/workspace_identity.json').read_text())
    if identity['commit']!=CONTROL_COMMIT:raise ValueError('Beklenen CNN-GRU kontrol yayını değil')
    if json.loads((control/'artifacts/design.json').read_text())!=previous.DESIGN:raise ValueError('Kontrol tasarımı değişmiş')
    if json.loads((control/'artifacts/control.json').read_text())!=protocol:raise ValueError('Kontrol veri/ayar kimliği değişmiş')
    if identity['runtime']!=current_runtime:raise ValueError('Kontrol GPU/ortam kimliği farklı')
    sig=previous.architecture_signature(study_signature(control),'gru')
    evidence={}
    for seed in (42,43,44):
        for fold in range(38):
            folder=control/'runs/gru'/f'seed_{seed}'/f'fold_{fold:03d}'
            if not validate_completed(folder,run_signature(sig,seed,fold)):raise ValueError('114 GRU kontrolü tamamlanmamış')
            marker=json.loads((folder/'complete.json').read_text())
            evidence[str(folder.relative_to(control)/'complete.json')]=sha256(folder/'complete.json')
            for name,digest in marker['files'].items():evidence[str(folder.relative_to(control)/name)]=digest
    return sig,evidence


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report'])
    for name in ['source','control','root']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve();control=args.control.resolve();root=args.root.resolve()
    for other in (source,control):
        if root==other or root.is_relative_to(other) or other.is_relative_to(root):raise ValueError('Ayrı çalışma alanı gerekli')
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
    candidate=candidate_config(cfg)
    identity=runtime_identity(REPO,require_gpu=True,hardware='selective-a100')
    verify_reference_runtime(protocol,dict(python=sys.version,torch=torch.__version__,numpy=np.__version__,
        pandas=pd.__version__,sklearn=sklearn.__version__,gpu=torch.cuda.get_device_name(0),
        cuda=torch.version.cuda,cudnn=torch.backends.cudnn.version()))
    control_sig,evidence=verify_control(control,protocol,identity)
    old_identity=json.loads((control/'reproducibility/workspace_identity.json').read_text())
    for name in ['yenibot/experiment/advisor_checkpoint_selection.py','yenibot/training/advisor_models.py']:
        if old_identity['sources'][name]!=sha256(REPO/name):raise ValueError('Kontrolle ortak eğitim kodu değişmiş')
    root.mkdir(parents=True,exist_ok=True)
    frame=pd.read_parquet(cfg['data']['frame']);features=protocol['features']
    folds=list(PurgedWalkForwardCV(**cfg['walk_forward'],label_horizon_bars=10).split(len(frame)))
    if len(folds)!=38 or len(features)!=6:raise ValueError('38 fold ve altı özellik gerekli')
    with engine.exclusive_run(root):
        freeze_workspace_identity(REPO,root,identity)
        immutable_json(root/'artifacts/design.json',DESIGN);immutable_json(root/'artifacts/control.json',protocol)
        immutable_json(root/'artifacts/config.json',candidate)
        immutable_json(root/'artifacts/control_evidence.json',dict(source=str(control),signature=control_sig,files=evidence))
        immutable_json(root/'artifacts/reused_workspace_identity.json',old_identity)
        immutable_json(root/'artifacts/reused_design.json',previous.DESIGN)
        signature=study_signature(root)
        for fold in folds:
            sel,assessment=split_validation(fold.val)
            engine.audit_boundary(frame,fold.train,sel,10);engine.audit_boundary(frame,sel,assessment,10)
            for seed in (42,43,44):
                folder=control/'runs/gru'/f'seed_{seed}'/f'fold_{fold.fold:03d}'
                for split,indices in [('selection',sel),('assessment',assessment)]:
                    p=pd.read_parquet(folder/f'bce_{split}.parquet');expected=frame.iloc[indices[63:]]
                    if len(p)!=465 or not np.array_equal(p.frame_row_position,indices[63:]) or not np.array_equal(p.label,expected.label) or not np.array_equal(pd.to_datetime(p.timestamp,utc=True),pd.to_datetime(expected.timestamp,utc=True)):
                        raise ValueError('Kontrol tarih/etiket/bölme uyuşmazlığı')
        if args.action=='prepare':print('114 kontrol doğrulandı. Yalnız hidden64 için114 yeni eğitim hazır; final test yok.')
        elif args.action=='train':
            for seed in (42,43,44):
                for fold in folds:
                    train_fold(frame,fold,candidate,features,seed,root/'runs/gru64'/f'seed_{seed}'/f'fold_{fold.fold:03d}',
                        run_signature(signature,seed,fold.fold),torch.device('cuda'),selectors=('bce',))
        else:
            previous.report(root,signature,comparisons={'gru128':(control/'runs/gru',control_sig),
                'gru64':(root/'runs/gru64',signature)},archive_name='capacity_review.zip',
                description='114 eski hidden128 kontrolü +114 yeni hidden64 eğitim. Kontrol ağırlıkları kaynak CNN-GRU workspace içinde kalır. ')


if __name__=='__main__':main()
