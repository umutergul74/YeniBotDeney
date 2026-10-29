"""All 37 existing inputs, descriptive only; no model/data transformation."""
from pathlib import Path
import io,json,zipfile,hashlib
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance,spearmanr
ROOT=Path(__file__).resolve().parents[3];out=Path(__file__).parent
source=ROOT/'reports/a6-period-diagnosis-20261028/shared37.parquet'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653'
z=zipfile.ZipFile(ROOT/'reports/early-epochs-20261024/source.zip')
p=json.loads(z.read('runs/B_46d8c88f55e3/protocol.json'));features=p['features'];assert len(features)==37
basic=json.loads(z.read('runs/A_96e471f6e5da/protocol.json'))['features']
cfg=p['config']['walk_forward'];assert cfg==dict(train_bars=5040,val_bars=1080,test_bars=720,step_bars=720,purge_bars=24,embargo_bars=24)
f=pd.read_parquet(source,columns=['label',*features]);assert len(f)==33551 and np.isfinite(f[features]).all().all()
rows=[]
for fold in range(38):
 start=fold*cfg['step_bars'];tr=f.iloc[start:start+5040];va=f.iloc[start+5064:start+6144]
 assert len(tr)==5040 and len(va)==1080
 for feature in features:
  x=tr[feature].to_numpy();v=va[feature].to_numpy();iqr=np.quantile(x,.75)-np.quantile(x,.25)
  rt=spearmanr(x[63:],tr.label.iloc[63:]).statistic if np.ptp(x[63:])>0 else np.nan
  rv=spearmanr(v[63:],va.label.iloc[63:]).statistic if np.ptp(v[63:])>0 else np.nan
  rows.append(dict(fold=fold,feature=feature,basic=int(feature in basic),train_iqr=iqr,
   shift=wasserstein_distance(x,v)/iqr if iqr>0 else np.nan,
   train_rho=rt,val_rho=rv,association_change=abs(rt-rv),
   train_nonzero_rate=np.mean(x!=0),val_nonzero_rate=np.mean(v!=0),
   train_constant=int(np.ptp(x)==0),val_constant=int(np.ptp(v)==0)))
d=pd.DataFrame(rows);assert len(d)==1406
d.to_csv(out/'all37_feature_context.csv',index=False)
d[d.train_iqr==0].to_csv(out/'sparse_inputs.csv',index=False)
fold=pd.read_csv(out/'fold_summary.csv');result=[]
for model,g in fold.groupby('model'):
 dd=d[d.basic==1] if model.startswith('A_') else d
 context=dd.groupby('fold')[['shift','association_change']].mean()
 assert context.notna().all().all()
 gg=g.merge(context,on='fold',validate='one_to_one')
 for x in ['shift','association_change']:
  for y in ['ap_lift','lift','precision','ap_gap']:
   result.append(dict(model=model,features=6 if model.startswith('A_') else 37,x=x,y=y,spearman=gg[x].corr(gg[y],method='spearman')))
pd.DataFrame(result).to_csv(out/'model_input_correlations.csv',index=False)
d.groupby('feature').agg(median_shift=('shift','median'),max_shift=('shift','max'),
 median_association_change=('association_change','median'),missing_shift=('shift',lambda s:s.isna().sum()),
 missing_association=('association_change',lambda s:s.isna().sum())).to_csv(out/'feature_context_summary.csv')
(out/'feature_checks.json').write_text(json.dumps({'frame_hash_verified':True,'features':37,'folds':38,
 'feature_fold_pairs':1406,'zero_train_iqr':int((d.train_iqr==0).sum()),
 'undefined_association_changes':int(d.association_change.isna().sum()),
 'zero_spread_policy':'record undefined, do not impute; count available dimensions','test_evaluations':0},indent=2)+'\n')
print(pd.DataFrame(result).query("y == 'lift'").round(3).to_string(index=False))
print('undefined',d[['shift','association_change']].isna().sum().to_dict())
