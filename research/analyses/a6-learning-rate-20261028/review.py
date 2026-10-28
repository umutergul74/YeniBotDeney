import json,io,zipfile,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score,log_loss
root=Path.cwd(); out=root/'research/analyses/a6-learning-rate-20261028';out.mkdir(exist_ok=True,parents=True)
source=Path('C:/Users/Umut/Downloads/learning_rate_review (1).zip')
z=zipfile.ZipFile(source);old=zipfile.ZipFile('reports/early-epochs-20261024/source.zip')
assert z.testzip() is None
read=lambda archive,n:json.loads(archive.read(n))
run=next(n.rsplit('/',1)[0] for n in z.namelist() if n.endswith('/protocol.json'))
oldrun=next(n.rsplit('/',1)[0] for n in old.namelist() if n.startswith('runs/A_') and n.endswith('/protocol.json'))
p=read(z,run+'/protocol.json'); c=read(old,oldrun+'/protocol.json')
assert read(z,'artifacts/control.json')['protocol']==c
for key in ['gpu','python','torch','cuda','cudnn','data_sha256','source_hashes','features','folds','seeds','numpy','pandas','sklearn']:
    assert p[key]==c[key],key
cfg=json.loads(json.dumps(p['config']));cfg['training']['learning_rate']=.001;cfg['output']=c['config']['output']
assert cfg==c['config'] and p['config']['training']['learning_rate']==.0001
evidence=read(z,'artifacts/control_evidence.json')
assert len(evidence)==342
for name,digest in evidence.items():assert hashlib.sha256(old.read(oldrun+'/'+name)).hexdigest()==digest,name
paired=pd.read_csv(io.BytesIO(z.read('reports/paired.csv'))).set_index(['seed','fold'])
assert len(paired)==114 and paired.index.is_unique
rows=[];hist=[]
for condition,archive,prefix in [('control',old,oldrun),('candidate',z,run)]:
    for seed in [42,43,44]:
        for fold in range(38):
            folder=f'{prefix}/seed_{seed}/fold_{fold:03d}/'
            m=read(archive,folder+'validation_metrics.json')
            h=pd.read_csv(io.BytesIO(archive.read(folder+'history.csv')))
            pred=pd.read_parquet(io.BytesIO(archive.read(folder+'validation_predictions.parquet')))
            if condition=='candidate':
                reference=pd.read_parquet(io.BytesIO(old.read(f'{oldrun}/seed_{seed}/fold_{fold:03d}/validation_predictions.parquet')))
                pd.testing.assert_frame_equal(pred[['timestamp','label','source_row_position']],reference[['timestamp','label','source_row_position']])
            assert len(pred)==1017 and pred.timestamp.is_unique
            assert h.epoch.tolist()==list(range(1,len(h)+1))
            assert np.isfinite(h[['train_bce','bce','average_precision']]).all().all()
            assert m['best_epoch']==int(h.loc[h.bce.idxmin(),'epoch']) and m['epochs_trained']==len(h)
            assert len(h)==min(100,m['best_epoch']+15) and m['test_evaluations']==0 and m['status']=='complete'
            y=pred.label.to_numpy(); prob=pred.probability.to_numpy(); decision=prob>=.5
            assert np.isin(y,[0,1]).all() and np.isfinite(prob).all() and ((prob>=0)&(prob<=1)).all()
            tp=int(((y==1)&decision).sum());n=int(decision.sum());pos=int(y.sum())
            recomputed=dict(average_precision=average_precision_score(y,prob),precision=tp/n if n else 0,recall=tp/pos,f1=2*tp/(n+pos))
            for k,v in recomputed.items():assert np.isclose(v,m['validation'][k],atol=1e-7)
            assert np.isclose(log_loss(y,prob,labels=[0,1]),m['validation']['bce'],atol=2e-6)
            for k in ['bce','average_precision','precision','recall','f1']:
                assert np.isclose(m['validation'][k],paired.loc[(seed,fold),k+'_'+condition],atol=1e-8)
            assert n==paired.loc[(seed,fold),'signals_'+condition]
            b=h.loc[h.bce.idxmin()];last=h.iloc[-1]
            rows.append(dict(condition=condition,seed=seed,fold=fold,best_epoch=m['best_epoch'],epochs=len(h),tp=tp,signals=n,positives=pos,
                bce=m['validation']['bce'],ap=m['validation']['average_precision'],last_bce=last.bce,last_ap=last.average_precision,
                train_falls_val_rises=bool(last.train_bce<b.train_bce and last.bce>b.bce),ap_falls=bool(last.average_precision<b.average_precision),
                epoch16_bce=h.iloc[15].bce,epoch16_ap=h.iloc[15].average_precision))
            hist.append(h.assign(condition=condition,seed=seed,fold=fold))
d=pd.DataFrame(rows);d.to_csv(out/'audit_by_run.csv',index=False)
for name in ['summary.csv','seed_summary.csv','paired.csv','comparison.png']:(out/name).write_bytes(z.read('reports/'+name))
stats={}
for name,g in d.groupby('condition'):
    sums=g[['tp','signals','positives']].sum()
    stats[name]={'no_signal_runs':int((g.signals==0).sum()),'best_epoch_median':float(g.best_epoch.median()),'best_epoch_max':int(g.best_epoch.max()),'best_epoch_le3':int((g.best_epoch<=3).sum()),'epochs_min':int(g.epochs.min()),'epochs_max':int(g.epochs.max()),'bce_mean':g.bce.mean(),'ap_mean':g.ap.mean(),'last_bce_mean':g.last_bce.mean(),'last_ap_mean':g.last_ap.mean(),'epoch16_bce_mean':g.epoch16_bce.mean(),'epoch16_ap_mean':g.epoch16_ap.mean(),'train_falls_val_rises':int(g.train_falls_val_rises.sum()),'ap_falls_best_to_last':int(g.ap_falls.sum()),'pooled_precision':float(sums.tp/sums.signals),'pooled_recall':float(sums.tp/sums.positives),'pooled_f1':float(2*sums.tp/(sums.signals+sums.positives)), 'median_seed_range_bce':float(g.groupby('fold').bce.agg(lambda s:s.max()-s.min()).median()),'median_seed_range_ap':float(g.groupby('fold').ap.agg(lambda s:s.max()-s.min()).median())}
stats['paired']={'bce_improved':int((paired.delta_bce<0).sum()),'ap_improved':int((paired.delta_average_precision>0).sum()),'both_improved':int(((paired.delta_bce<0)&(paired.delta_average_precision>0)).sum()),'bce_delta_mean':paired.delta_bce.mean(),'ap_delta_mean':paired.delta_average_precision.mean()}
print(json.dumps(stats,indent=2))
print('LAST FOLD\n',paired.loc[(slice(None),37),['bce_control','bce_candidate','average_precision_control','average_precision_candidate','signals_control','signals_candidate']].to_string())
(out/'checks.json').write_text(json.dumps({'zip_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crc':'passed','candidate_runs':114,'control_runs':114,'control_hashes_matched':342,'only_learning_rate_changed':True,'runtime_and_engine_matched':True,'selection_patience_and_predictions_checked':True,'test_evaluations':0,'stats':stats},indent=2)+'\n',encoding='utf-8')
