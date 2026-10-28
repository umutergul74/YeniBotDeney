import zipfile,io,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path('research/analyses/a6-thresholds-20261028');out.mkdir(parents=True,exist_ok=True)
sources={'control':Path('reports/early-epochs-20261024/source.zip'),'candidate':Path('C:/Users/Umut/Downloads/learning_rate_review (1).zip')}
grid=np.arange(201)/200;rows=[];scores=[];identities={};predictions={}
for condition,path in sources.items():
 z=zipfile.ZipFile(path)
 names=sorted(n for n in z.namelist() if n.startswith('runs/A_') and n.endswith('validation_predictions.parquet'))
 assert len(names)==114
 for name in names:
  seed=int(name.split('/')[2].split('_')[1]);fold=int(name.split('/')[3].split('_')[1])
  p=pd.read_parquet(io.BytesIO(z.read(name)));y=p.label.to_numpy();s=p.probability.to_numpy()
  assert len(p)==1017 and np.isfinite(s).all() and ((s>=0)&(s<=1)).all()
  predictions[condition,seed,fold]=p
  ident=p[['timestamp','label','source_row_position']]
  if condition=='control':identities[seed,fold]=ident
  else:pd.testing.assert_frame_equal(ident,identities[seed,fold])
  decisions=s[:,None]>=grid; n=decisions.sum(0);tp=(decisions&(y[:,None]==1)).sum(0)
  rows.append(pd.DataFrame(dict(condition=condition,seed=seed,fold=fold,threshold=grid,tp=tp,signals=n,positives=int(y.sum()),samples=len(y),empty=(n==0).astype(int))))
  scores.append(dict(condition=condition,seed=seed,fold=fold,q50=np.quantile(s,.5),q90=np.quantile(s,.9),q95=np.quantile(s,.95),q99=np.quantile(s,.99),maximum=s.max()))
d=pd.concat(rows,ignore_index=True)
def aggregate(keys):
 a=d.groupby(keys)[['tp','signals','positives','samples','empty']].sum().reset_index()
 a['precision']=a.tp/a.signals.replace(0,np.nan);a['recall']=a.tp/a.positives
 a['f1']=2*a.tp/(a.signals+a.positives);a['signal_rate']=a.signals/a.samples
 return a
a=aggregate(['condition','threshold']);seeds=aggregate(['condition','seed','threshold'])
folds=aggregate(['condition','fold','threshold'])
a.to_csv(out/'thresholds.csv',index=False);seeds.to_csv(out/'thresholds_by_seed.csv',index=False)
folds.to_csv(out/'thresholds_by_fold.csv',index=False)
pd.DataFrame(scores).to_csv(out/'score_quantiles_by_run.csv',index=False)
sel=a[a.threshold.isin([.3,.35,.4,.45,.5,.55,.6,.65,.7])]
sel.to_csv(out/'selected_thresholds.csv',index=False)
print(sel[['condition','threshold','precision','recall','signal_rate','empty']].round(4).to_string(index=False))
print('SCORE',pd.DataFrame(scores).groupby('condition')[['q50','q90','q95','q99']].mean().round(4).to_string())
# Sanity at the unchanged reference threshold, independently checked last turn.
prev=json.loads(Path('research/analyses/a6-learning-rate-20261028/checks.json').read_text())
for c in sources:
 row=a[(a.condition==c)&(a.threshold==.5)].iloc[0]
 for key in ['precision','recall','f1']:assert np.isclose(row[key],prev['stats'][c]['pooled_'+key])
 for _,g in a[a.condition==c].groupby('condition'):assert (np.diff(g.signals)<=0).all()
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
axes=axes.ravel()
for c,color,label in [('control','#dc2626','0.001 kontrol'),('candidate','#2563eb','0.0001 aday')]:
 g=a[a.condition==c]
 for ax,col in zip(axes,['precision','recall','f1','signal_rate']):
  ax.plot(g.threshold,g[col]*100,color=color,label=label,lw=2)
  for seed in [42,43,44]:
   h=seeds[(seeds.condition==c)&(seeds.seed==seed)]
   ax.plot(h.threshold,h[col]*100,color=color,alpha=.18,lw=.8)
for ax,title in zip(axes,['Precision: sinyallerin isabeti','Recall: TP yakalama','F1: precision-recall dengesi','Sinyal verilen ornekler']):
 ax.set(title=title,xlabel='Esik',ylabel='%',xlim=(.2,.75),ylim=(0,100));ax.axvline(.5,color='gray',ls=':');ax.grid(alpha=.2)
axes[0].legend(fontsize=9)
fig.suptitle('A6 validation: kalin cizgi toplam, ince cizgiler uc seed\nYuksek esikte precision, sinyal sayisiyla birlikte okunmali',fontsize=12)
fig.savefig(out/'comparison.png',dpi=150);plt.close(fig)
manifest={'sources':{c:hashlib.sha256(p.read_bytes()).hexdigest() for c,p in sources.items()},'pairs':114,'grid_step':.005,'aggregation':'sum TP/FP/FN over overlapping fold/seed prediction instances; no deduplication, no ensemble','checks':['matched validation identities','finite probabilities','0.5 matches prior verified pooled metrics','monotonic signal counts'],'new_training':False,'test_evaluations':0,'threshold_selected':False}
(out/'checks.json').write_text(json.dumps(manifest,indent=2)+'\n')

# Fixed global thresholds: match the old model's coverage, without choosing by labels.
matched=[]
for t in [.35,.4,.45,.5,.55,.6]:
 ref=a[(a.condition=='control') & (a.threshold==t)].iloc[0]
 cand=a[a.condition=='candidate']
 hit=cand.loc[(cand.signal_rate-ref.signal_rate).abs().idxmin()]
 matched.append(dict(control_threshold=t,candidate_threshold=hit.threshold,
     control_precision=ref.precision,candidate_precision=hit.precision,
     control_coverage=ref.signal_rate,candidate_coverage=hit.signal_rate,
     control_empty=ref['empty'],candidate_empty=hit['empty']))
pd.DataFrame(matched).to_csv(out/'matched_global.csv',index=False)

# Equal top-k in EACH fold/seed isolates within-period ranking from score scale.
# Retrospective diagnostic, not an executable signal rule. No labels used in sorting.
rankrows=[];periodrows=[]
for (c,seed,fold),p in predictions.items():
 y=p.label.to_numpy();s=p.probability.to_numpy()
 order=np.argsort(-s,kind='stable')
 for coverage in [.01,.02,.05,.1,.2]:
  k=max(1,round(len(p)*coverage));chosen=order[:k]
  assert k==len(set(chosen))
  rankrows.append(dict(condition=c,seed=seed,fold=fold,coverage=coverage,k=k,
      tp=int(y[chosen].sum()),precision=float(y[chosen].mean()),
      prevalence=float(y.mean()),cutoff=float(s[chosen[-1]]),
      tied_boundary=bool(k<len(s) and s[order[k]]==s[order[k-1]])))
 periodrows.append(dict(condition=c,seed=seed,fold=fold,start=str(p.timestamp.min()),
     end=str(p.timestamp.max()),prevalence=y.mean(),mean_score=s.mean(),
     max_score=s.max(),signals_050=int((s>=.5).sum())))
r=pd.DataFrame(rankrows);r.to_csv(out/'matched_by_run.csv',index=False)
period=pd.DataFrame(periodrows);period.to_csv(out/'periods.csv',index=False)
rs=r.groupby(['condition','coverage']).agg(precision=('precision','mean'),
    min_precision=('precision','min'),median_precision=('precision','median'),
    p10_precision=('precision',lambda x:x.quantile(.1)),p90_precision=('precision',lambda x:x.quantile(.9)),
    tp=('tp','sum'),signals=('k','sum'),ties=('tied_boundary','sum')).reset_index()
rs.to_csv(out/'matched_summary.csv',index=False)
rp=r.pivot(index=['seed','fold','coverage'],columns='condition',values='precision').reset_index()
rp['delta']=rp.candidate-rp.control;rp.to_csv(out/'matched_pairs.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
for c,color,label in [('control','#dc2626','LR 0.001'),('candidate','#2563eb','LR 0.0001')]:
 g=rs[rs.condition==c];axes[0].plot(g.coverage*100,g.precision*100,'o-',color=color,label=label)
 h=r[(r.condition==c)&(r.coverage==.05)].groupby('fold').precision.mean()
 axes[1].plot(h.index,h*100,color=color,label=label)
axes[0].set(xlabel='Her eğitimde seçilen en yüksek skorlu örnekler (%)',ylabel='Precision (%)',title='Eşit sayıda örnek: sıralama becerisi')
axes[1].set(xlabel='Fold (zaman sırası)',ylabel='Precision (%)',title='Her foldun en yüksek skorlu %5’i; üç seed ortalaması')
axes[0].set_ylim(0,100);axes[1].set_ylim(0,100)
baseline=period[period.condition=='control'].groupby('fold').prevalence.mean()
axes[0].axhline(baseline.mean()*100,color='gray',ls=':',label='Ortalama TP oranı')
axes[1].plot(baseline.index,baseline*100,color='gray',ls=':',label='Dönemin TP oranı')
for ax in axes:ax.grid(alpha=.2);ax.legend()
fig.suptitle('A6 validation — geçmişe dönük teşhis; yeni sinyal kuralı seçilmedi')
fig.savefig(out/'matched_coverage.png',dpi=150);plt.close(fig)
print('MATCHED GLOBAL\n',pd.DataFrame(matched).round(4).to_string(index=False))
print('TOP K\n',rs.round(4).to_string(index=False))
print('PAIRED\n',rp.groupby('coverage').delta.agg(['mean',lambda x:(x>0).sum(),lambda x:(x<0).sum()]).to_string())
print('LAST FOLD TOP5\n',r[(r.fold==37)&(r.coverage==.05)].to_string(index=False))
manifest['checks']+=['equal top-k per run; stable score sorting; boundary ties counted']
manifest['matched_global_rule']='nearest coverage on 0.005 threshold grid; no label optimization'
manifest['matched_within_run_rule']='top round(1017 * coverage), retrospective diagnostic only'
(out/'checks.json').write_text(json.dumps(manifest,indent=2)+'\n')

