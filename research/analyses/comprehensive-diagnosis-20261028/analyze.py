"""All existing comparable runs: descriptive diagnostics, no training/test/selection."""
from pathlib import Path
import zipfile,io,json,hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3];out=Path(__file__).parent
sources={'original':ROOT/'reports/early-epochs-20261024/source.zip',
 'A_low':Path.home()/'Downloads/learning_rate_review (1).zip',
 'B_low':Path.home()/'Downloads/learning_rate_review.zip'}
labels=pd.read_csv(ROOT/'research/analyses/a6-period-diagnosis-20261028/label_shift.csv').set_index('fold')
rows=[];top=[];thresholds=[];identities={};hashes={};epoch_rows=[]
for source,path in sources.items():
 hashes[source]=hashlib.sha256(path.read_bytes()).hexdigest();z=zipfile.ZipFile(path)
 protocols=sorted(n for n in z.namelist() if n.endswith('/protocol.json') and n.startswith('runs/'))
 assert len(protocols)==(4 if source=='original' else 1)
 for pn in protocols:
  p=json.loads(z.read(pn));prefix=pn.rsplit('/',1)[0];model=p['experiment'];lr=p['config']['training']['learning_rate']
  name=f'{model}_{lr:g}';assert p['data_sha256']=='ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653'
  assert p['folds']==list(range(38)) and p['seeds']==[42,43,44]
  for seed in [42,43,44]:
   for fold in range(38):
    folder=f'{prefix}/seed_{seed}/fold_{fold:03d}/'
    h=pd.read_csv(io.BytesIO(z.read(folder+'history.csv')));m=json.loads(z.read(folder+'validation_metrics.json'))
    pred=pd.read_parquet(io.BytesIO(z.read(folder+'validation_predictions.parquet')))
    ident=pred[['timestamp','label','source_row_position']]
    if name=='A_0.001':identities[seed,fold]=ident
    else:pd.testing.assert_frame_equal(ident,identities[seed,fold])
    assert m['status']=='complete' and m['test_evaluations']==0 and len(pred)==1017
    b=h.loc[h.bce.idxmin()];a=h.loc[h.average_precision.idxmax()]
    assert m['best_epoch']==b.epoch and np.isclose(m['validation']['bce'],b.bce)
    y=pred.label.to_numpy();s=pred.probability.to_numpy();prev=y.mean()
    assert np.isclose(average_precision_score(y,s),b.average_precision) and np.isclose(prev,labels.loc[fold,'val_tp'])
    rate=labels.loc[fold,'train_tp'];constant=-(prev*np.log(rate)+(1-prev)*np.log(1-rate))
    row=dict(model=name,seed=seed,fold=fold,epochs=len(h),best_epoch=int(b.epoch),ap_peak_epoch=int(a.epoch),
      bce=b.bce,ap=b.average_precision,prevalence=prev,ap_lift=b.average_precision/prev,
      ap_peak=a.average_precision,ap_gap=a.average_precision-b.average_precision,
      bce_cost=a.bce-b.bce,epoch_disagrees=int(a.epoch!=b.epoch),ap_peak_later=int(a.epoch>b.epoch),
      bce_gain_constant=constant-b.bce,signals_050=int((s>=.5).sum()),
      after_best_train_falls=int(h.iloc[-1].train_bce<b.train_bce),last_ap=h.iloc[-1].average_precision,
      score_mean=s.mean(),mean_score_error=s.mean()-prev)
    rows.append(row)
    epoch_rows.append(h.assign(model=name,seed=seed,fold=fold))
    order=np.argsort(-s,kind='stable')
    for frac in [.01,.02,.05,.1,.2]:
     k=round(len(y)*frac);tp=y[order[:k]].sum()
     cutoff=s[order[k-1]];above=s>cutoff;ties=s==cutoff;needed=k-int(above.sum())
     tiepos=int(y[ties].sum());tieneg=int(ties.sum())-tiepos;base=int(y[above].sum())
     low=(base+max(0,needed-tieneg))/k;high=(base+min(needed,tiepos))/k
     top.append(dict(model=name,seed=seed,fold=fold,fraction=frac,k=k,tp=int(tp),precision=tp/k,lift=(tp/k)/prev,
       boundary_tie=int(s[order[k-1]]==s[order[k]]),tie_precision_low=low,tie_precision_high=high))
    for t in [.3,.35,.4,.45,.5,.55,.6,.65,.7]:
     sel=s>=t;n=sel.sum();tp=y[sel].sum()
     thresholds.append(dict(model=name,seed=seed,fold=fold,threshold=t,signals=int(n),tp=int(tp),positives=int(y.sum()),samples=len(y),empty=int(n==0)))
d=pd.DataFrame(rows);r=pd.DataFrame(top);t=pd.DataFrame(thresholds)
assert len(d)==684 and not d.duplicated(['model','seed','fold']).any()
d.to_csv(out/'run_diagnostics.csv',index=False);r.to_csv(out/'topk_by_run.csv',index=False)
summary=d.groupby('model').agg(runs=('fold','size'),bce=('bce','mean'),ap=('ap','mean'),
 epoch_disagrees=('epoch_disagrees','sum'),ap_peak_later=('ap_peak_later','sum'),
 median_best_epoch=('best_epoch','median'),mean_ap_gap=('ap_gap','mean'),median_ap_gap=('ap_gap','median'),
 mean_bce_cost=('bce_cost','mean'),bce_beats_constant=('bce_gain_constant',lambda x:(x>0).sum()),
 zero_signal_runs=('signals_050',lambda x:(x==0).sum()),mean_ap_lift=('ap_lift','mean'))
summary.to_csv(out/'summary.csv')
r.groupby(['model','fraction'])[['precision','lift']].mean().to_csv(out/'topk_summary.csv')
ta=t.groupby(['model','threshold'])[['signals','tp','positives','samples','empty']].sum()
ta['precision']=ta.tp/ta.signals.replace(0,np.nan);ta['recall']=ta.tp/ta.positives
ta['f1']=2*ta.tp/(ta.signals+ta.positives);ta['signal_rate']=ta.signals/ta.samples
ta.to_csv(out/'threshold_summary.csv')
fold=d.groupby(['model','fold'])[['bce','ap','ap_lift','ap_gap','bce_gain_constant','score_mean','mean_score_error']].mean().reset_index()
fold=fold.merge(r[r.fraction==.05].groupby(['model','fold'])[['precision','lift']].mean().reset_index(),on=['model','fold'],validate='one_to_one')
fold.to_csv(out/'fold_summary.csv',index=False)
# All chronological folds, grouped into four contiguous blocks, no outcome-based filtering.
d['time_block']=pd.cut(d.fold,[-1,9,19,29,37],labels=['00-09','10-19','20-29','30-37'])
d.groupby(['model','time_block'],observed=True)[['bce','ap','ap_lift','ap_gap']].mean().to_csv(out/'time_blocks.csv')
relations=pd.read_csv(ROOT/'research/analyses/a6-period-diagnosis-20261028/feature_label_association.csv')
relations['abs_association_change']=(relations.train_spearman-relations.val_spearman).abs()
shift=pd.read_csv(ROOT/'research/analyses/a6-period-diagnosis-20261028/feature_shift.csv').groupby('fold').wasserstein_iqr.mean()
ass=relations.groupby('fold').abs_association_change.mean()
context=fold.merge(shift.rename('feature_shift'),on='fold').merge(ass.rename('association_change'),on='fold')
context=context.merge(labels[['delta_tp']],on='fold')
cor=[]
for model,g in context.groupby('model'):
 for x in ['feature_shift','association_change','delta_tp']:
  for y in ['ap_lift','precision','lift','ap_gap']:
   cor.append(dict(model=model,x=x,y=y,spearman=g[x].corr(g[y],method='spearman')))
pd.DataFrame(cor).to_csv(out/'context_correlations.csv',index=False)
# Paired LR effect across every fold/seed, not just selected poor periods.
paired=[]
for model in ['A','B']:
 a=d[d.model==model+'_0.001'].set_index(['seed','fold']);b=d[d.model==model+'_0.0001'].set_index(['seed','fold'])
 for metric in ['bce','ap','ap_gap']:
  delta=b[metric]-a[metric];paired.append(dict(model=model,metric=metric,delta_mean=delta.mean(),lower=int((delta<0).sum()),higher=int((delta>0).sum())))
pd.DataFrame(paired).to_csv(out/'paired_lr.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
summary.epoch_disagrees.plot.bar(ax=axes[0],color='#2563eb')
axes[0].set(title='BCE ve AP farkli epochta en iyi',ylabel='Run sayisi / 114',xlabel='',ylim=(0,114))
summary.mean_ap_gap.plot.bar(ax=axes[1],color='#d97706')
axes[1].set(title='Kayitli maksimum AP - secilen AP',ylabel='Ortalama AP farki (sonradan bakis)',xlabel='')
for ax in axes:ax.tick_params(axis='x',rotation=30);ax.grid(axis='y',alpha=.2)
fig.savefig(out/'epoch_divergence.png',dpi=150);plt.close(fig)
mat=fold.pivot(index='model',columns='fold',values='lift')
fig,ax=plt.subplots(figsize=(13,4),layout='constrained');im=ax.imshow(mat,aspect='auto',cmap='RdYlGn',vmin=0,vmax=2.5)
ax.set(yticks=range(len(mat)),yticklabels=mat.index,xlabel='Fold',title='Top %5 precision / donemin TP orani (1: donem taban orani)')
fig.colorbar(im,ax=ax);fig.savefig(out/'period_ranking.png',dpi=150);plt.close(fig)
checks=dict(runs=684,models=6,folds=38,seeds=3,matched_validation_identities=True,source_sha256=hashes,
 minimum_bce_epoch_and_saved_ap_verified=True,topk_ties=int(r.boundary_tie.sum()),
 tie_rule='Stable original row order; possible precision bounds recorded for boundary ties',test_evaluations=0,new_training=0,
 limitation='AP peak uses already-selected validation and a BCE-stopped history; not alternative checkpoint policy performance.')
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(summary.round(4).to_string());print('TOP5',r[r.fraction==.05].groupby('model')[['precision','lift']].mean().round(4).to_string())
print('PAIRED',pd.DataFrame(paired).round(4).to_string(index=False))

# Sensitivity views from the same outputs; neither is a new selection rule.
seed=d.groupby(['model','seed'])[['bce','ap','ap_gap','signals_050']].mean()
seed.to_csv(out/'seed_summary.csv')
parity=d.assign(fold_parity=d.fold%2).groupby(['model','fold_parity'])[['bce','ap','ap_gap']].mean()
parity.to_csv(out/'nonoverlap_sensitivity.csv')
extra=[]
for model,g in d.groupby('model'):
 rr=r[(r.model==model)&(r.fraction==.05)]
 extra.append(dict(model=model,ap_gap_gt001=int((g.ap_gap>.01).sum()),ap_gap_gt002=int((g.ap_gap>.02).sum()),
   ap_peak_earlier=int((g.ap_peak_epoch<g.best_epoch).sum()),best_epoch1=int((g.best_epoch==1).sum()),
   seed_range_top5_median=rr.groupby('fold').precision.agg(lambda s:s.max()-s.min()).median(),
   fold_top5_min=rr.groupby('fold').precision.mean().min(),fold_top5_max=rr.groupby('fold').precision.mean().max(),
   top5_below_prevalence=int((rr.lift<1).sum())))
pd.DataFrame(extra).to_csv(out/'stability_summary.csv',index=False)
