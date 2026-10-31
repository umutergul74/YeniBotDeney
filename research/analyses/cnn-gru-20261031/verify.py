"""Kayıtlı ZIP tahminlerini doğrular; eğitim veya eşik optimizasyonu yapmaz."""
import hashlib, io, json, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, log_loss

archive=Path(sys.argv[1]);z=zipfile.ZipFile(archive)
out=Path(__file__).parent
read=lambda name:json.loads(z.read(name))
sha=lambda b:hashlib.sha256(b).hexdigest()
study=sha(''.join(sha(z.read(p)) for p in ['reproducibility/workspace_identity.json','artifacts/design.json','artifacts/control.json']).encode())
table=pd.read_csv(z.open('reports/by_run.csv'))
assert len(table)==684 and not table.duplicated(['architecture','seed','fold','policy']).any()
assert read('reproducibility/workspace_identity.json')['commit']=='dafcb21aa65883c7dc5c53d77a934e0cce565f55'
identities={};epochs=[];hashes=0;rows=0;preds=[]
for arch in ['gru','cnn_gru']:
 for seed in [42,43,44]:
  for fold in range(38):
   base=f'runs/{arch}/seed_{seed}/fold_{fold:03d}/'
   marker=read(base+'complete.json');m=read(base+'metrics.json');sel=read(base+'selection.json')
   signature=sha(f'{sha(f"{study}:{arch}".encode())}:{seed}:{fold}'.encode())
   assert marker['signature']==m['signature']==sel['signature']==signature
   assert m['test_evaluations']==0 and all(b['passed'] for b in m['boundary_audit'].values())
   for name,digest in marker['files'].items():
    if name.endswith('.pt'):continue
    assert sha(z.read(base+name))==digest;hashes+=1
   h=pd.read_csv(z.open(base+'history.csv'))
   epoch=int(h.loc[h.bce.idxmin(),'epoch']);assert sel['epochs']=={'bce':epoch}
   epochs.append(dict(architecture=arch,seed=seed,fold=fold,epoch=epoch,length=len(h)))
   s=pd.read_parquet(io.BytesIO(z.read(base+'bce_selection.parquet')))
   a=pd.read_parquet(io.BytesIO(z.read(base+'bce_assessment.parquet')))
   assert len(s)==len(a)==465 and s.timestamp.max()<a.timestamp.min()
   identity=(tuple(s.timestamp),tuple(s.label),tuple(a.timestamp),tuple(a.label))
   key=(seed,fold)
   if key in identities:assert identities[key]==identity
   identities[key]=identity
   assert np.isfinite(a.probability).all() and a.probability.between(0,1).all()
   for r in table[(table.architecture==arch)&(table.seed==seed)&(table.fold==fold)].itertuples():
    threshold=.5 if r.policy=='fixed_050' else float(np.sort(s.probability)[-int(np.ceil(465*(.05 if r.policy=='selection_top5' else .1)))])
    assert np.isclose(r.threshold,threshold,atol=1e-15,rtol=0)
    mask=a.probability>=threshold
    assert r.epoch==epoch and r.signals==mask.sum() and r.tp==a.loc[mask,'label'].sum() and r.positives==a.label.sum() and r.samples==465
    assert np.isclose(r.ap,average_precision_score(a.label,a.probability),atol=1e-7)
    assert np.isclose(r.bce,log_loss(a.label,a.probability),atol=1e-6)
    rows+=1
   preds.append(a.assign(architecture=arch,seed=seed,fold=fold))
summary=pd.read_csv(z.open('reports/summary.csv'))
for r in summary.itertuples():
 g=table[(table.architecture==r.architecture)&(table.policy==r.policy)]
 for field in ['signals','tp','positives','samples']:assert getattr(r,field)==g[field].sum()
 assert np.isclose(r.precision,g.tp.sum()/g.signals.sum())
 assert np.isclose(r.recall,g.tp.sum()/g.positives.sum())
 assert np.isclose(r.f1,2*g.tp.sum()/(g.signals.sum()+g.positives.sum()))
 assert r.no_signal_runs==(g.signals==0).sum()
 assert np.isclose(r.ap_mean,g.ap.mean()) and np.isclose(r.bce_mean,g.bce.mean())
e=pd.DataFrame(epochs);e.to_csv(out/'epochs.csv',index=False)
g=table[table.policy=='selection_top5'].groupby(['fold','architecture'])[['tp','signals','samples']].sum()
g['precision']=g.tp/g.signals.replace(0,np.nan);g['signal_rate']=g.signals/g.samples;g.to_csv(out/'by_fold.csv')
base=table[table.policy=='fixed_050'];wide=base.pivot(index=['seed','fold'],columns='architecture',values=['ap','bce'])
print('EPOCHS',e.groupby('architecture').epoch.agg(['mean','median','min','max']).to_string())
for metric in ['ap','bce']:
 d=wide[metric].cnn_gru-wide[metric].gru;print(metric,'delta',d.mean(),'positive',int((d>1e-8).sum()),'negative',int((d< -1e-8).sum()))
 print('fold means',d.groupby('fold').mean().describe().to_dict())
print('SEEDS',base.groupby(['seed','architecture'])[['ap','bce']].mean().to_string())
print('LAST',g.tail(4).to_string())
print('TOP5 SEEDS',table[table.policy=='selection_top5'].groupby(['seed','architecture'])[['tp','signals']].sum().to_string())
for name in ['summary.csv','comparison.png','by_run.csv']: (out/name).write_bytes(z.read('reports/'+name))
checks=dict(runs=len(e),nonweight_hashes=hashes,decision_rows=rows,source_zip_sha256=sha(archive.read_bytes()),weights_verified=False,final_test_evaluations=0)
(out/'checks.json').write_text(json.dumps(checks,indent=2));print(checks)
