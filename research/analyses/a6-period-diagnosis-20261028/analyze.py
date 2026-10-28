"""Read-only train/validation distribution diagnosis; never evaluate test slices."""
import hashlib, io, json, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp, wasserstein_distance, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from yenibot.training.walk_forward import PurgedWalkForwardCV
out=Path(__file__).parent
source=ROOT/'reports/a6-period-diagnosis-20261028/shared37.parquet'
z=zipfile.ZipFile(ROOT/'reports/early-epochs-20261024/source.zip')
prefix='runs/A_96e471f6e5da'
protocol=json.loads(z.read(prefix+'/protocol.json'))
digest=hashlib.sha256(source.read_bytes()).hexdigest()
assert digest==protocol['data_sha256']=='ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653'
for relative in ['yenibot/training/walk_forward.py','yenibot/training/dataset.py']:
 expected=next(v for k,v in protocol['source_hashes'].items() if k.endswith('/'+relative))
 assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected
features=protocol['features'];cfg=protocol['config'];offset=cfg['model']['seq_len']-1
frame=pd.read_parquet(source,columns=['timestamp','label',*features])
assert len(frame)==33551 and np.isfinite(frame[features]).all().all()
assert pd.to_datetime(frame.timestamp,utc=True).diff().iloc[1:].eq(pd.Timedelta(hours=1)).all()
folds=list(PurgedWalkForwardCV(**cfg['walk_forward'],label_horizon_bars=10).split(len(frame)))
assert len(folds)==38
dist=[];labels=[];relations=[]
for fold in folds:
 tr=frame.iloc[fold.train];va=frame.iloc[fold.val]
 yt=tr.label.iloc[offset:];yv=va.label.iloc[offset:]
 assert len(yt)==4977 and len(yv)==1017
 for seed in [42,43,44]:
  p=pd.read_parquet(io.BytesIO(z.read(f'{prefix}/seed_{seed}/fold_{fold.fold:03d}/validation_predictions.parquet')))
  assert np.array_equal(p.label.to_numpy(),yv.to_numpy())
  assert np.array_equal(pd.to_datetime(p.timestamp,utc=True).astype('int64'),pd.to_datetime(va.timestamp.iloc[offset:],utc=True).astype('int64'))
  assert np.array_equal(p.source_row_position,np.arange(offset,len(va)))
 labels.append(dict(fold=fold.fold,train_start=str(tr.timestamp.iloc[0]),train_end=str(tr.timestamp.iloc[-1]),
   val_start=str(va.timestamp.iloc[offset]),val_end=str(va.timestamp.iloc[-1]),
   train_tp=yt.mean(),val_tp=yv.mean(),delta_tp=yv.mean()-yt.mean(),train_row_tp=tr.label.mean(),val_row_tp=va.label.mean()))
 for feature in features:
  x=tr[feature].to_numpy();v=va[feature].to_numpy();q=np.quantile(x,[.01,.25,.5,.75,.99]);iqr=q[3]-q[1]
  assert iqr>0
  dist.append(dict(fold=fold.fold,feature=feature,train_median=q[2],val_median=np.median(v),train_iqr=iqr,
    val_iqr=np.quantile(v,.75)-np.quantile(v,.25),median_shift_iqr=(np.median(v)-q[2])/iqr,
    wasserstein_iqr=wasserstein_distance(x,v)/iqr,ks=ks_2samp(x,v).statistic,
    val_outside_train_p01_p99=np.mean((v<q[0])|(v>q[4]))))
  # Marginal endpoint associations, not an explanation of a recurrent sequence model.
  relations.append(dict(fold=fold.fold,feature=feature,
    train_spearman=spearmanr(x[offset:],yt).statistic,val_spearman=spearmanr(v[offset:],yv).statistic))
d=pd.DataFrame(dist);l=pd.DataFrame(labels);rel=pd.DataFrame(relations)
d.to_csv(out/'feature_shift.csv',index=False);l.to_csv(out/'label_shift.csv',index=False);rel.to_csv(out/'feature_label_association.csv',index=False)
metrics=pd.read_csv(ROOT/'research/analyses/a6-learning-rate-20261028/audit_by_run.csv')
top=pd.read_csv(ROOT/'research/analyses/a6-thresholds-20261028/matched_by_run.csv')
m=metrics.groupby(['condition','fold'])[['bce','ap','best_epoch']].mean().reset_index()
t=top[top.coverage==.05].groupby(['condition','fold']).precision.mean().reset_index(name='top5_precision')
m=m.merge(t,on=['condition','fold'],validate='one_to_one').merge(l,on='fold',validate='many_to_one')
m=m.merge(d.groupby('fold').agg(mean_shift=('wasserstein_iqr','mean'),max_shift=('wasserstein_iqr','max')),on='fold',validate='many_to_one')
m['ap_lift']=m.ap/m.val_tp;m['top5_lift']=m.top5_precision/m.val_tp
m['train_constant_bce']=-(m.val_tp*np.log(m.train_tp)+(1-m.val_tp)*np.log(1-m.train_tp))
m['val_oracle_entropy']=-(m.val_tp*np.log(m.val_tp)+(1-m.val_tp)*np.log(1-m.val_tp))
m.to_csv(out/'period_summary.csv',index=False)
cor=[]
for c,g in m.groupby('condition'):
 for x in ['mean_shift','max_shift','delta_tp']:
  for y in ['ap','ap_lift','top5_precision','top5_lift']:
   cor.append(dict(condition=c,x=x,y=y,spearman=spearmanr(g[x],g[y]).statistic))
pd.DataFrame(cor).to_csv(out/'descriptive_correlations.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(13,4.8),layout='constrained')
axes[0].plot(l.fold,l.train_tp*100,label='Train TP');axes[0].plot(l.fold,l.val_tp*100,label='Validation TP')
axes[0].set(xlabel='Fold',ylabel='TP (%)',title='Sequence hedeflerindeki TP orani');axes[0].legend();axes[0].grid(alpha=.2)
pivot=d.pivot(index='feature',columns='fold',values='wasserstein_iqr').reindex(features)
im=axes[1].imshow(pivot,aspect='auto',cmap='YlOrRd',vmin=0)
axes[1].set(yticks=range(6),yticklabels=features,xlabel='Fold',title='Dagilim farki / train IQR (0: ayni dagilim)')
for ax in axes:
 for k in [28,37]:ax.axvline(k,color='black',ls=':',alpha=.6)
fig.colorbar(im,ax=axes[1],label='Wasserstein / IQR')
fig.savefig(out/'distribution_shift.png',dpi=150);plt.close(fig)
checks={'frame_sha256':digest,'source_drive_id':'14kXQEYSUVQY2rwWD4YFSYTiCRZUrs4B6','folds':38,'prediction_identity_pairs':114,
 'train_targets':4977,'validation_targets':1017,'split_and_dataset_hashes_match':True,'test_evaluations':0,
 'scope':'raw feature rows within train/validation; labels at sequence endpoints; no sequence weighting',
 'limitations':'Marginal distributions and descriptive associations; dependent folds; no p-values or causal claim.'}
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(m[m.fold.isin([28,37])].round(4).to_string(index=False))
print(d[d.fold.isin([28,37])].round(4).to_string(index=False))
print('SHIFT RANK',m[m.condition=='candidate'].sort_values('mean_shift',ascending=False)[['fold','mean_shift','top5_precision']].head(10).to_string(index=False))
print('CORRELATIONS',pd.DataFrame(cor).round(3).to_string(index=False))

# Existing epoch logs only; no checkpoint replacement or inference.
# User Downloads is sibling to Desktop, not part of the repository.
candidate_zip=Path.home()/'Downloads/learning_rate_review (1).zip'
cz=zipfile.ZipFile(candidate_zip)
cp=next(n.rsplit('/',1)[0] for n in cz.namelist() if n.endswith('/protocol.json'))
epochs=[]
for fold in [28,37]:
 for seed in [42,43,44]:
  h=pd.read_csv(io.BytesIO(cz.read(f'{cp}/seed_{seed}/fold_{fold:03d}/history.csv')))
  b=h.loc[h.bce.idxmin()];a=h.loc[h.average_precision.idxmax()]
  epochs.append(dict(fold=fold,seed=seed,bce_selected_epoch=int(b.epoch),selected_bce=b.bce,selected_ap=b.average_precision,
    retrospective_max_ap_epoch=int(a.epoch),retrospective_max_ap=a.average_precision,bce_at_max_ap=a.bce))
pd.DataFrame(epochs).to_csv(out/'epoch_tradeoff.csv',index=False)
