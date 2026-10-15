"""Bounded development-only barrier comparison; frozen labeling, no model selection."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prior_diagnostics',ROOT/'scripts/analyze_advisor_diagnostics.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
SCENARIOS=[(2,5),(2,2),(3,2),(1,1),(1,2),(1.5,1.5),(1.5,2),(2,1),(2,3),(3,3)]


def pareto_mask(costs):
    values=np.asarray(costs,dtype=float)
    if values.ndim!=2 or not np.isfinite(values).all():raise ValueError('Finite cost matrix required')
    return np.array([not any(np.all(other<=row) and np.any(other<row) for other in values) for row in values])


def summarize(hit,forward):
    n=len(hit)
    prior.require(n>0 and np.isin(hit,[0,1,2,3]).all(),'Invalid hit codes')
    result={'n':n,'profit_first':int((hit==1).sum()),'stop_first':int(np.isin(hit,[2,3]).sum()),
            'timeout':int((hit==0).sum()),'both_same_bar':int((hit==3).sum())}
    for key in ['profit_first','stop_first','timeout','both_same_bar']:result[key+'_pct']=100*result[key]/n
    result['balance_distance_pp']=abs(result['profit_first_pct']-50)
    for name,mask in [('positive',hit==1),('negative',hit!=1),('timeout',hit==0)]:
        values=forward[mask]
        result[name+'_mean_fwd_pct']=float(values.mean()*100) if len(values) else None
        result[name+'_median_fwd_pct']=float(np.median(values)*100) if len(values) else None
        result[name+'_positive_return_pct']=float((values>0).mean()*100) if len(values) else None
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--detail',type=Path,required=True)
    args=parser.parse_args();out=args.output.resolve();detail=args.detail.resolve()
    prior.require(not out.exists() and not detail.exists(),'New output directories required')
    inventory=[]
    def check(path,expected=None):
        sha=prior.sha(path)
        if expected:prior.require(sha==expected,'Input hash mismatch: '+str(path))
        inventory.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha})
        return path
    frame_path=ROOT/'evidence/prepared_recovery/v2.0.1/data/development_wavelet_off.parquet'
    frame=pd.read_parquet(check(frame_path,'f6346a93ee4b97125d00e8d26223ba11a141806cdff675934e033a00940977a8'))
    raw_path=ROOT/'evidence/drive_snapshot/colab_v1/inputs/market_snapshot_v1/btc_1h.parquet'
    raw=pd.read_parquet(check(raw_path,'a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c'))
    frame.timestamp=pd.to_datetime(frame.timestamp,utc=True);raw.timestamp=pd.to_datetime(raw.timestamp,utc=True)
    prior.require(len(frame)==33551 and frame.timestamp.is_unique and frame.timestamp.max()<pd.Timestamp('2026-01-01',tz='UTC'),'Unexpected development scope')
    raw=raw.loc[raw.timestamp<=frame.timestamp.max()+pd.Timedelta(hours=10)].reset_index(drop=True)
    prior.require(raw.timestamp.is_unique and raw.timestamp.diff().dropna().eq(pd.Timedelta(hours=1)).all(),'Raw hourly gaps')
    prior.require(np.isfinite(raw[['close','high','low']]).all().all(),'Nonfinite prices')
    positions=pd.Index(raw.timestamp).get_indexer(frame.timestamp)
    prior.require((positions>=0).all() and (positions+10<len(raw)).all(),'Missing common horizon')
    atr=prior.atr14(raw).to_numpy()
    prior.require(np.allclose(atr[positions],frame.atr_14,rtol=1e-12,atol=1e-10),'ATR parity failed')
    for col in ['close','high','low']:prior.require(np.array_equal(raw[col].to_numpy()[positions],frame[col]),'Price parity failed')
    forward=raw.close.to_numpy()[positions+10]/raw.close.to_numpy()[positions]-1
    prior.require(np.allclose(forward,frame.fwd_return_10h,rtol=1e-12,atol=1e-12),'Forward parity failed')
    previous=pd.read_csv(check(ROOT/'research/analyses/diagnostics-20261015/results/barrier_counts.csv')).set_index('tp_sl_atr')
    out.mkdir(parents=True);detail.mkdir(parents=True)
    loop=prior.label_loop();rows=[];yearly=[]
    for tp,sl in SCENARIOS:
        name=f'{tp:g}/{sl:g}'
        labels,gains,hits,exits=loop(raw.close.to_numpy(),raw.high.to_numpy(),raw.low.to_numpy(),atr,tp,sl,10)
        hit=hits[positions]; y=labels[positions]
        prior.require((y>=0).all(),'Unlabelable common sample')
        row={'scenario':name,'tp':tp,'sl':sl,'tp_sl_ratio':tp/sl,'previously_tested':name in previous.index,**summarize(hit,forward)}
        if name in previous.index:
            old=previous.loc[name]
            for key in ['n','profit_first','stop_first','timeout']:prior.require(row[key]==old[key],'Old scenario count mismatch')
            prior.require(row['both_same_bar']==old['both_same_bar_assigned_stop'],'Ambiguity parity failed')
        if name=='2/5':prior.require(np.array_equal(y,frame.label) and np.allclose(gains[positions],frame.tb_return),'Frozen target parity failed')
        rows.append(row)
        for year in sorted(frame.timestamp.dt.year.unique()):
            mask=frame.timestamp.dt.year.to_numpy()==year
            yearly.append({'scenario':name,'year':int(year),**summarize(hit[mask],forward[mask])})
        pd.DataFrame({'timestamp':frame.timestamp,'label':y,'hit_code':hit,'barrier_return':gains[positions],
                      'forward_return_10h':forward}).to_csv(detail/f'labels_tp{tp:g}_sl{sl:g}.csv',index=False,lineterminator='\n')
    table=pd.DataFrame(rows);years=pd.DataFrame(yearly)
    objectives=['balance_distance_pp','timeout_pct','both_same_bar_pct']
    table['diagnostic_pareto']=pareto_mask(table[objectives].to_numpy())
    table.to_csv(out/'barrier_comparison.csv',index=False,lineterminator='\n')
    years.to_csv(out/'barrier_by_year.csv',index=False,lineterminator='\n')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(12,7),layout='constrained');left=np.zeros(len(table))
    names=[x+(' · önceki' if old else '') for x,old in zip(table.scenario,table.previously_tested)]
    for key,label,color in [('profit_first_pct','Kâr önce / etiket 1','#0d9488'),('stop_first_pct','Zarar önce','#e76f51'),('timeout_pct','Süre dolumu','#94a3b8')]:
        values=table[key].to_numpy();ax.barh(names,values,left=left,label=label,color=color,height=.7)
        for i,v in enumerate(values):
            if v>4:ax.text(left[i]+v/2,i,f'%{v:.1f}',ha='center',va='center',color='white',fontsize=10,fontweight='bold')
        left+=values
    ax.invert_yaxis();ax.set(xlim=(0,100),xlabel='Aynı 33.551 saatin yüzdesi',ylabel='TP / SL · ATR',title='10 saat ufukta 10 bariyer senaryosu')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.1),ncol=3);fig.savefig(out/'barrier_comparison.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5.5),layout='constrained')
    for _,r in table.iterrows():
        axes[0].scatter(r.profit_first_pct,r.timeout_pct,s=60+100*r.both_same_bar_pct,
                        color='#0d9488' if r.diagnostic_pareto else '#64748b',alpha=.8)
        axes[0].annotate(r.scenario,(r.profit_first_pct,r.timeout_pct),xytext=(5,5),textcoords='offset points',fontsize=9)
    axes[0].axvline(50,color='#9d174d',ls='--',alpha=.6)
    axes[0].set(xlabel='Pozitif etiket (%)',ylabel='Süre dolumu (%)',title='Yeşil: üç teşhis ölçütünde Pareto adayı\nNokta büyüklüğü: çift-temas oranı')
    matrix=years.pivot(index='scenario',columns='year',values='profit_first_pct').reindex(table.scenario)
    im=axes[1].imshow(matrix.to_numpy(),aspect='auto',vmin=0,vmax=60,cmap='YlGnBu')
    axes[1].set_xticks(range(len(matrix.columns)),matrix.columns);axes[1].set_yticks(range(len(matrix)),matrix.index)
    axes[1].set_title('Yıllara göre pozitif etiket (%)')
    for i in range(len(matrix)):
        for j in range(len(matrix.columns)):axes[1].text(j,i,f'{matrix.iloc[i,j]:.1f}',ha='center',va='center',color='white' if matrix.iloc[i,j]>35 else 'black',fontsize=9)
    fig.colorbar(im,ax=axes[1],label='%');fig.savefig(out/'barrier_tradeoffs.png',dpi=170);plt.close(fig)
    payload={'scenarios':[list(x) for x in SCENARIOS],'objectives_minimized':objectives,'pareto_candidates':table.loc[table.diagnostic_pareto,'scenario'].tolist(),
             'scope':{'n':len(frame),'start':str(frame.timestamp.min()),'end':str(frame.timestamp.max()),'excluded':0},
             'inputs':inventory,'script_sha256':prior.sha(Path(__file__)),'shared_analysis_sha256':prior.sha(ROOT/'scripts/analyze_advisor_diagnostics.py'),
             'label_code_sha256':prior.sha(ROOT/'yenibot/labeling/triple_barrier.py'),'python':sys.version,'numpy':np.__version__,
             'pandas':pd.__version__,'matplotlib':matplotlib.__version__,'platform':platform.platform(),
             'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
             'training_operations':0,'test_evaluations':0,'old_scenario_parity':True,'deployment_barrier_selected':False}
    (out/'manifest.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    outputs=[{'path':p.relative_to(ROOT).as_posix(),'sha256':prior.sha(p),'bytes':p.stat().st_size} for folder in [out,detail] for p in sorted(folder.iterdir()) if p.is_file()]
    (out/'output_manifest.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(table[['scenario','profit_first_pct','stop_first_pct','timeout_pct','both_same_bar_pct','diagnostic_pareto']].to_string(index=False))


if __name__=='__main__':main()
