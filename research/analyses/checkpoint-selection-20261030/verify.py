import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, log_loss
root=Path('reports/checkpoint-review-20261030/source')
table=pd.read_csv(root/'reports/by_run.csv')
assert len(table)==684
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
study=hashlib.sha256(''.join(sha(root/p) for p in ['reproducibility/workspace_identity.json','artifacts/design.json','artifacts/control.json']).encode()).hexdigest()
epochs=[]; verified=0; decisions=0; samples=[]
for seed in (42,43,44):
 for fold in range(38):
  folder=root/f'runs/seed_{seed}/fold_{fold:03d}'
  marker=json.loads((folder/'complete.json').read_text()); selection=json.loads((folder/'selection.json').read_text()); m=json.loads((folder/'metrics.json').read_text())
  sig=hashlib.sha256(f'{study}:{seed}:{fold}'.encode()).hexdigest()
  assert marker['signature']==selection['signature']==m['signature']==sig
  assert m['test_evaluations']==0 and all(x['passed'] for x in m['boundary_audit'].values())
  for name,digest in marker['files'].items():
   if name.endswith('.pt'):continue
   assert sha(folder/name)==digest; verified+=1
  h=pd.read_csv(folder/'history.csv')
  assert selection['epochs']==dict(bce=int(h.loc[h.bce.idxmin(),'epoch']),ap=int(h.loc[h.average_precision.idxmax(),'epoch']))
  epochs.append(dict(seed=seed,fold=fold,**selection['epochs'],length=len(h)))
  pair=[]
  for rule in ['bce','ap']:
   s=pd.read_parquet(folder/f'{rule}_selection.parquet'); a=pd.read_parquet(folder/f'{rule}_assessment.parquet')
   assert len(s)==len(a)==465 and s.timestamp.max()<a.timestamp.min()
   assert np.isfinite(a.probability).all() and a.probability.between(0,1).all()
   pair.append(a[['timestamp','label','frame_row_position']])
   rows=table[(table.seed==seed)&(table.fold==fold)&(table.rule==rule)]
   assert set(rows.policy)=={'fixed_050','selection_top5','selection_top10'}
   for row in rows.itertuples():
    threshold=.5 if row.policy=='fixed_050' else float(np.sort(s.probability)[-int(np.ceil(len(s)*(.05 if row.policy=='selection_top5' else .1)))])
    assert np.isclose(row.threshold,threshold,rtol=0,atol=1e-15)
    mask=a.probability>=threshold
    assert row.signals==mask.sum() and row.tp==a.loc[mask,'label'].sum() and row.positives==a.label.sum() and row.samples==465
    assert np.isclose(row.ap,average_precision_score(a.label,a.probability),atol=1e-7)
    assert np.isclose(row.bce,log_loss(a.label,a.probability),atol=1e-6)
    decisions+=1
   samples.append(dict(seed=seed,fold=fold,rule=rule,selection_ap=m['results'][rule]['selection']['average_precision'],assessment_ap=m['results'][rule]['assessment']['average_precision']))
  pd.testing.assert_frame_equal(*pair)
e=pd.DataFrame(epochs); p=pd.DataFrame(samples)
print('HASHED',verified,'DECISION_ROWS',decisions,'RUNS',len(e))
print('EPOCHS',e[['bce','ap','length']].agg(['mean','median','min','max']).to_string())
print('same_epochs',int((e.bce==e.ap).sum()),'AP_later',int((e.ap>e.bce).sum()),'BCE_first3',int((e.bce<=3).sum()))
print('AP selection vs assessment',p.groupby('rule')[['selection_ap','assessment_ap']].mean().to_string())
base=table[table.policy=='fixed_050']; wide=base.pivot(index=['seed','fold'],columns='rule',values=['bce','ap'])
for metric in ['bce','ap']:
 d=wide[metric]['ap']-wide[metric]['bce']; print(metric,'AP minus BCE',d.mean(),'positive',(d>1e-8).sum(),'negative',(d< -1e-8).sum(),'tie',(d.abs()<=1e-8).sum())
print('BY_SEED',base.groupby(['seed','rule'])[['bce','ap']].mean().to_string())
g=table[table.policy=='selection_top5'].groupby(['fold','rule'])[['tp','signals','samples']].sum();g['precision']=g.tp/g.signals;g['coverage']=g.signals/g.samples
print('FOLD top5 ranges',g.groupby('rule')[['precision','coverage']].agg(['min','median','max']).to_string())
print('LAST',g.tail(4).to_string())
out=Path('research/analyses/checkpoint-selection-20261030');out.mkdir(exist_ok=True)
e.to_csv(out/'epochs.csv',index=False);g.to_csv(out/'by_fold.csv');table.to_csv(out/'by_run.csv',index=False)
(out/'checks.json').write_text(json.dumps(dict(runs=len(e),hashes_checked=verified,decision_rows_recomputed=decisions,source_zip_sha256=sha(root.parent/'source.zip'),weights_verified=False,final_test_evaluations=0),indent=2))
