"""Mevcut exp032 üzerine seçim-değerlendirme aktarımı; eğitim yok."""
import hashlib,io,json,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path(__file__).parent
source=Path('C:/Users/Umut/Downloads/cnn_gru_review.zip')
expected=json.loads(Path('research/analyses/cnn-gru-20261031/checks.json').read_text())['source_zip_sha256']
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
z=zipfile.ZipFile(source);rows=[]
for arch in ['gru','cnn_gru']:
 for seed in [42,43,44]:
  for fold in range(38):
   base=f'runs/{arch}/seed_{seed}/fold_{fold:03d}/'
   h=pd.read_csv(z.open(base+'history.csv'));m=json.loads(z.read(base+'metrics.json'))['results']['bce']
   s=pd.read_parquet(io.BytesIO(z.read(base+'bce_selection.parquet')))
   a=pd.read_parquet(io.BytesIO(z.read(base+'bce_assessment.parquet')))
   best=h.loc[h.epoch==m['epoch']].iloc[0];last=h.iloc[-1]
   r=dict(architecture=arch,seed=seed,fold=fold,epoch=m['epoch'],
     after_best_train_delta=float(last.train_bce-best.train_bce),
     after_best_selection_delta=float(last.bce-best.bce))
   for name,p in [('selection',s),('assessment',a)]:
    r[name+'_ap']=m[name]['average_precision'];r[name+'_bce']=m[name]['bce']
    r[name+'_prevalence']=float(p.label.mean());r[name+'_score_mean']=float(p.probability.mean())
    r[name+'_score_q95']=float(p.probability.quantile(.95))
    r[name+'_ap_excess']=r[name+'_ap']-r[name+'_prevalence']
   r['ap_transfer_delta']=r['assessment_ap']-r['selection_ap']
   r['excess_transfer_delta']=r['assessment_ap_excess']-r['selection_ap_excess']
   rows.append(r)
t=pd.DataFrame(rows);assert len(t)==228
t.to_csv(out/'by_run.csv',index=False)
f=t.groupby(['fold','architecture']).mean(numeric_only=True).reset_index()
f.to_csv(out/'by_fold.csv',index=False)
summary={}
for arch,g in t.groupby('architecture'):
 summary[arch]=dict(selection_ap=g.selection_ap.mean(),assessment_ap=g.assessment_ap.mean(),
  selection_prevalence=g.selection_prevalence.mean(),assessment_prevalence=g.assessment_prevalence.mean(),
  selection_excess=g.selection_ap_excess.mean(),assessment_excess=g.assessment_ap_excess.mean(),
  train_down_selection_up=int(((g.after_best_train_delta<0)&(g.after_best_selection_delta>0)).sum()),
  assessment_excess_nonpositive=int((g.assessment_ap_excess<=0).sum()),
  ap_transfer_spearman=float(g.groupby('fold')[['selection_ap','assessment_ap']].mean().corr(method='spearman').iloc[0,1]),
  excess_transfer_spearman=float(g.groupby('fold')[['selection_ap_excess','assessment_ap_excess']].mean().corr(method='spearman').iloc[0,1]),
  median_train_delta=float(g.after_best_train_delta.median()),median_selection_delta=float(g.after_best_selection_delta.median()))
w=f.pivot(index='fold',columns='architecture',values='assessment_ap_excess')
summary['shared']=dict(fold_excess_spearman=float(w.corr(method='spearman').iloc[0,1]),
 both_nonpositive_folds=w.index[(w.gru<=0)&(w.cnn_gru<=0)].tolist(),
 both_positive_folds=int(((w.gru>0)&(w.cnn_gru>0)).sum()))
(out/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
fig,axes=plt.subplots(1,2,figsize=(12,4),layout='constrained')
for arch,label in [('gru','GRU'),('cnn_gru','CNN→GRU')]:
 g=f[f.architecture==arch]
 axes[0].plot(g.fold,100*g.assessment_ap_excess,label=label)
 axes[1].scatter(100*g.selection_ap_excess,100*g.assessment_ap_excess,label=label,alpha=.7)
for ax in axes:ax.axhline(0,color='gray',linestyle=':');ax.legend();ax.grid(alpha=.2)
axes[0].set(xlabel='Dönem (fold)',ylabel='AP − pozitif etiket oranı (yüzde puan)',title='Sonraki validation bölümünde iki mimari')
axes[1].set(xlabel='Seçim bölümünde AP − etiket oranı (puan)',ylabel='Sonraki bölümde AP − etiket oranı (puan)',title='Seçimdeki avantaj sonraki bölüme taşınıyor mu?')
fig.savefig(out/'transfer.png',dpi=150);plt.close(fig)
