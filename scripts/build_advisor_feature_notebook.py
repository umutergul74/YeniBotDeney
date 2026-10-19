"""Build the thin Colab entry for the four-structure feature correction."""
import json
from pathlib import Path
from textwrap import dedent

ROOT=Path(__file__).resolve().parents[1]


def build():
    cells=[]
    def cell(kind,text):
        record={'cell_type':kind,'metadata':{},'source':dedent(text).strip()+'\n'}
        if kind=='code':record.update(execution_count=None,outputs=[])
        cells.append(record)
    cell('markdown','''
    # 05 · A6 / B37 / C37 / D37 — eşit özellik kapsamı
    **A100 (NVIDIA A100-SXM4-40GB)** ve Drive hesabı **icinbedava34@gmail.com**.
    A–B: aynı GRU ile özellik genişletmesi. B/C/D: aynı37 girdi ile mimari karşılaştırması.
    A–C/D saf mimari karşılaştırması değildir. Eski çalışmalar korunur.
    2/5 ATR, 10 saat, özgün33551 saat, 38fold ×3seed; dört yapı toplam456 eğitim.
    Yeni workspace'te A kontrolü de yeniden eğitilir. Validation BCE ile epoch seçimi;
    0,50 referansı ve eşik eğrileri. Final test veya otomatik eşik seçimi yok.
    Sırayla çalıştırın. Yarım kalan çalışma aynı workspace ve sürümle devam eder.
    ''')
    cell('code','''
    import os
    os.environ['MPLBACKEND']='Agg'
    os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
    from pathlib import Path
    from google.colab import drive
    drive.mount('/content/drive')
    LEGACY=Path('/content/drive/MyDrive/yeniBot/advisor_experiments/colab_v1')
    ROOT=Path('/content/drive/MyDrive/yeniBot/advisor_experiments/feature_comparison_v1/a100_001')
    ALLOW_TRAINING=True  # 4 x38 x3 eğitim; False yalnız hazırlık/rapor içindir.
    AUTO_DISCONNECT=True
    RELEASE='advisor-feature-comparison-v1.0.0'
    REPO=Path('/content/advisor_feature_comparison_repo')
    RUNTIME=Path('/content/advisor_feature_comparison_runtime')
    SUCCESS=set()
    ''')
    cell('markdown','''
    ## İzole ortam
    Sabit sürüm indirilir; kilitli Python/paketler yerel `/content` altında kurulur.
    İlk hazırlık eski ham snapshot ve OI arşivinden aynı hazırlanmış tabloyu
    geri üretir ve eski SHA256 ile doğrular. Eksik kaynakta durur; başka veri çekmez.
    ''')
    cell('code','''
    import subprocess,sys,json,hashlib
    from datetime import datetime,timezone
    SESSION=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    LOGS=ROOT/'sessions'/SESSION
    LOGS.mkdir(parents=True,exist_ok=True)
    ENV=dict(os.environ)
    for key in ['PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','IPYTHONDIR','JUPYTER_CONFIG_DIR']:
        ENV.pop(key,None)
    ENV.update(MPLBACKEND='Agg',PYTHONNOUSERSITE='1',CUBLAS_WORKSPACE_CONFIG=':4096:8',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4')
    def logged(command,name):
        with (LOGS/name).open('a',encoding='utf-8') as log:
            process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env=ENV)
            try:
                for line in process.stdout:
                    print(line,end='');log.write(line);log.flush()
                code=process.wait()
                if code:raise subprocess.CalledProcessError(code,command)
            except BaseException:
                if process.poll() is None:process.terminate();process.wait()
                raise
    URL='https://github.com/umutergul74/YeniBotDeney.git'
    if not REPO.exists():
        logged(['git','clone','--branch',RELEASE,'--depth','1',URL,str(REPO)],'setup.log')
    def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
    assert git('remote','get-url','origin')==URL
    assert git('rev-parse','HEAD')==git('rev-parse',RELEASE+'^{commit}')
    assert not git('status','--porcelain','--untracked-files=no')
    receipt=RUNTIME/'environment_receipt.json'
    logged([sys.executable,'-I',str(REPO/'scripts/bootstrap_advisor.py'),'--repo',str(REPO),
        '--runtime',str(RUNTIME),'--cache',str(ROOT/'bootstrap_cache'),'--receipt',str(receipt)],'setup.log')
    PYTHON=json.loads(receipt.read_text())['python']
    def step(action):
        order=['prepare','train','report','bundle']
        SUCCESS.difference_update(order[order.index(action):])
        command=[PYTHON,'-I',str(REPO/'scripts/advisor_feature_comparison.py'),action,
            '--root',str(ROOT),'--legacy',str(LEGACY)]
        if ALLOW_TRAINING:command.append('--allow-training')
        logged(command,action+'.log')
        SUCCESS.add(action)
    ''')
    cell('markdown','## Sabit veriyi doğrula ve 37 özellik kapsamını hazırla')
    cell('code',"step('prepare')")
    cell('markdown','## A, B, C, D eğitimleri — aynı A100 ortamında\nTamamlanan foldlar korunur; yarım eğitimler aynı kimlikle devam eder.')
    cell('code',"step('train')")
    cell('markdown','## Validation raporları — dört yapı tamamlanmadan eksik ortalama üretilmez')
    cell('code',"step('report')\nfrom IPython.display import display,Image\ndisplay(Image(filename=str(ROOT/'reports/thresholds.png')))\nprint((ROOT/'reports/validation_summary.csv').read_text())")
    cell('markdown','## Review ZIP, Drive doğrulaması ve otomatik kapanış\nAğırlıklar ZIP dışında, runs klasöründe kalır. Yeniden bağlanınca dosyalar eşleşmezse oturum kapanmaz.')
    cell('code','''
    step('bundle')
    if not {'report','bundle'}<=SUCCESS:raise RuntimeError('Rapor/ZIP tamamlanmadı')
    def digest(path):
        h=hashlib.sha256()
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(4*1024*1024),b''):h.update(block)
        return h.hexdigest()
    expected={str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if p.is_file()}
    if not expected:raise RuntimeError('Workspace boş')
    drive.flush_and_unmount()
    drive.mount('/content/drive')
    for relative,checksum in expected.items():
        p=ROOT/relative
        if not p.is_file() or digest(p)!=checksum:raise RuntimeError('Drive doğrulaması başarısız: '+relative)
    print('Drive dosyaları yeniden bağlandıktan sonra doğrulandı. Raporlar:',ROOT/'reports')
    if AUTO_DISCONNECT:
        from google.colab import runtime
        runtime.unassign()
    ''')
    return {'nbformat':4,'nbformat_minor':5,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},'cells':cells}


if __name__=='__main__':
    target=ROOT/'notebooks/workflows/05_feature_comparison.ipynb'
    target.write_text(json.dumps(build(),ensure_ascii=False,indent=1)+'\n',encoding='utf-8',newline='\n')
