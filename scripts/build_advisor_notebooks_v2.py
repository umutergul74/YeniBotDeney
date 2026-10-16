"""Generate thin, isolated-runtime advisor notebooks. Never import old builders."""
from pathlib import Path
import json
import subprocess
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
BASELINE = '741d1d4bebbb7fe2a931d09d56f5fe6d87bac006'
RELEASE = 'advisor-notebooks-v2.0.2'
NAMES = {
    'basic':'06_advisor_ablation_colab.ipynb',
    'full':'07_advisor_full_features_colab.ipynb',
    'wavelet':'08_advisor_wavelet_colab.ipynb',
    'loss':'09_advisor_losses_colab.ipynb',
    'final':'10_advisor_final_test_colab.ipynb',
}


def cell(kind, text):
    result={'cell_type':kind,'metadata':{},'source':dedent(text).strip()+'\n'}
    if kind=='code':result.update(execution_count=None,outputs=[])
    return result


def build(phase, *, render_only=False):
    name=NAMES[phase]
    mode='recovery' if phase in ('basic','full') else ('archive' if phase=='final' else 'research')
    experiments={'basic':['A'],'full':['B','C','D'],'wavelet':['W_ON'],
                 'loss':['L_WEIGHTED_BCE','L_FOCAL','L_BCE_PEARSON','L_FOCAL_PEARSON'],'final':[]}[phase]
    titles={'basic':'Temel özellikler: veri kurtarma veya yeni A deneyi',
            'full':'Tam özellikler: veri kurtarma veya yeni B–C–D deneyleri',
            'wavelet':'Yeni çalışma alanında wavelet karşılaştırması',
            'loss':'Yeni çalışma alanında kayıp karşılaştırması',
            'final':'Tamamlanan final testinin salt okunur denetimi'}
    cells=[cell('markdown',f'''
    # {name[:2]} — {titles[phase]}

    **Sürüm 2.** Notebook yalnızca komutları düzenler; araştırma kodu Python modüllerindedir.
    Colab'ın Python/Torch paketleri araştırma için kullanılmaz. Sabit Python 3.13.15 ve
    hashli paket kilidiyle ayrı süreç ortamı kurulur. İlk kurulum ve GPU paketleri zaman alabilir.

    **Eski `colab_v1` arşivi salt okunurdur.** Bu notebook eski sonuçları güncellemez.
    06/07 varsayılanı eksik iki tabloyu yeniden oluşturup özgün SHA ile karşılaştırmaktır;
    başarılı dosyalar ayrı recovery klasörüne yazılır. Bu bir yeniden eğitim değildir.
    Yeni eğitim için 06/07'de MODE='research', ortak WORKSPACE_ID ve ALLOW_TRAINING=True gerekir.
    08/09 eski kontrol sonuçlarını yeni ortamla birleştirmez; aynı yeni workspace'in
    A–D sonuçlarını kullanır. 10, görülmüş Eylül 2026 testini yeniden çalıştırmaz.

    **Akış:** ayarlar → Drive → sabit Git sürümü → izole ortam → veri/işlem → durum → yedek.
    Aynı workspace'i iki Colab oturumunda eşzamanlı çalıştırmayın.
    ''')]
    cells.append(cell('markdown','## 1 — Çalışma ayarları\n\nAynı deneye devam ederken WORKSPACE_ID ve sürümü değiştirmeyin.'))
    cells.append(cell('code',f'''
    from pathlib import Path
    from datetime import datetime, timezone
    import json, os, subprocess, sys

    MODE = {mode!r}  # recovery: yalnızca tablolar; research: yeni deney; archive: finali oku
    PHASE = {phase!r}
    WORKSPACE_ID = 'advisor_protocol_v2'
    EXPERIMENTS = {experiments!r}
    ALLOW_TRAINING = False
    RELEASE_TAG = {RELEASE!r}  # Sabit yayın; dalın güncel ucunu otomatik çekmez.
    REPO_URL = 'https://github.com/umutergul74/yeniBot.git'
    REPO_DIR = Path('/content/advisor_reproducible_repo')
    RUNTIME_DIR = Path('/content/advisor_isolated_runtime')
    DRIVE_BASE = Path('/content/drive/MyDrive/yeniBot/advisor_experiments')
    SESSION = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    assert WORKSPACE_ID.replace('_','').replace('-','').isalnum()
    assert MODE in ('recovery','research','archive')
    assert PHASE != 'final' or MODE == 'archive', 'Görülmüş final testi yeniden çalıştırılmaz.'
    ''') )
    cells.append(cell('markdown','## 2 — Drive ve ayrı çıktı alanı\n\nHazırlanmış tablolar, ağırlıklar ve ilerleme kalıcı alana yazılır.'))
    cells.append(cell('code','''
    from google.colab import drive
    drive.mount('/content/drive')
    LEGACY_ROOT = DRIVE_BASE / 'colab_v1'
    namespace = {'recovery':'recovery_v2','research':'research_v2','archive':'archive_audit_v2'}[MODE]
    ROOT = DRIVE_BASE / namespace / WORKSPACE_ID
    ROOT.mkdir(parents=True,exist_ok=True)
    LOG_DIR = ROOT / 'sessions' / SESSION
    LOG_DIR.mkdir(parents=True,exist_ok=True)
    print('Eski arşiv (salt okunur):',LEGACY_ROOT)
    print('Bu çalışmanın kalıcı alanı:',ROOT)
    print('Oturum günlükleri:',LOG_DIR)
    ''') )
    cells.append(cell('markdown','## 3 — Sabit Git yayını\n\nYerel değişiklik varsa otomatik silinmez; yanlış sürümle devam edilmez.'))
    cells.append(cell('code','''
    if not (REPO_DIR/'.git').exists():
        subprocess.run(['git','clone','--branch',RELEASE_TAG,'--single-branch',REPO_URL,str(REPO_DIR)],check=True)
    def git(*args):
        return subprocess.check_output(['git','-C',str(REPO_DIR),*args],text=True).strip()
    assert not git('status','--porcelain','--untracked-files=no'), 'Kodda yerel değişiklik var.'
    assert git('rev-parse','HEAD') == git('rev-parse',RELEASE_TAG+'^{commit}'), 'Yanlış yayın; yeni runtime açın.'
    print('Kod sürümü:',git('rev-parse','HEAD'))
    ''') )
    cells.append(cell('markdown','''
    ## 4 — Kilitli araştırma ortamı

    Sistem Python'una pip install yapılmaz. Ayrı Python + venv kullanılır; bütün
    bağımlılıklar sürüm ve SHA ile sabittir. Drive'daki indirme önbelleği tekrar kullanılır.
    uv kilitleri ve paket onbellegi /content altinda tutulur. Drive kalici ciktilari
    ve dogrulanmis kurucu dosyasini saklar. Yeni runtime paketleri yeniden indirebilir.
    Kurulum başarısızsa sonraki hücreye geçmeyin. Eğitim için Tesla T4 seçin.
    ''') )
    cells.append(cell('code','''
    def logged(command, name):
        with (LOG_DIR/name).open('a',encoding='utf-8',buffering=1) as log:
            env=dict(os.environ)
            for key in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','IPYTHONDIR','JUPYTER_CONFIG_DIR'):
                env.pop(key,None)
            env['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
            env['MPLBACKEND']='Agg'  # Colab inline backend is host-only.
            with subprocess.Popen(command,cwd=REPO_DIR,env=env,stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,text=True,bufsize=1) as process:
                try:
                    for line in process.stdout:
                        print(line,end=''); log.write(line)
                    code=process.wait()
                except BaseException:
                    process.terminate(); process.wait(); raise
                if code: raise subprocess.CalledProcessError(code,command)
    RECEIPT=RUNTIME_DIR/'environment_receipt.json'
    logged([sys.executable,'-I',str(REPO_DIR/'scripts/bootstrap_advisor.py'),
            '--repo',str(REPO_DIR),'--runtime',str(RUNTIME_DIR),
            '--cache',str(DRIVE_BASE/'reproducibility_cache_v2'),
            '--receipt',str(RECEIPT)],'environment_setup.log')
    runtime=json.loads(RECEIPT.read_text())
    RESEARCH_PYTHON=runtime['python']
    print('İzole Python:',RESEARCH_PYTHON)
    print('Paket kilidi:',runtime['lock_sha256'])

    def execute_step(action):
        command=[RESEARCH_PYTHON,'-I',str(REPO_DIR/'scripts/advisor_workspace.py'),action,
                 '--root',str(ROOT),'--legacy',str(LEGACY_ROOT),'--mode',MODE,
                 '--phase',PHASE,'--session',SESSION,'--experiments',*EXPERIMENTS]
        if ALLOW_TRAINING: command.append('--allow-training')
        logged(command,action+'.log')
    ''') )
    if phase=='final':
        cells.extend([cell('markdown','''
        ## 5 — Arşivlenen finali doğrula

        Model/scaler, fit/test tablo ve tahmin hashleri kontrol edilir. Ağırlıklar
        yüklenmez; predict/evaluate/fit çağrılmaz. Sonuç ayrı rapor alanına yazılır.
        Yeni final döneminin kullanımı ayrı bilimsel protokol gerektirir.
        '''),cell('code',"execute_step('audit-final')")])
    else:
        cells.extend([cell('markdown','''
        ## 5 — Veriyi hazırla ve Drive'a kalıcı kaydet

        Veri + manifest birlikte saklanır; `reports/prepared_frames.zip` gerçek
        tabloları da içerir. Recovery modunda özgün tablo hash'i eşleşmezse durur.
        Eski modeller veya tablolar değiştirilmez. Research modunda yeni kontrol
        çalışmaları kendi namespace'inde hazırlanır. Kaynaklar eski sabit snapshot'tır.
        '''),cell('code',"execute_step('prepare')"),cell('markdown','''
        ## 6 — Eğitim / kaldığı yerden devam

        Recovery modunda eğitim yapılmaz. Research modunda ALLOW_TRAINING=True
        seçilmelidir. Her epoch'un ağırlıkları, optimizer/RNG, en iyi model ve scaler
        mevcut motor tarafından Drive'a yazılır. Uyumlu bitmiş foldlar atlanır.
        Yeni ortamda kontrol sonuçları farklı çıkarsa eski kazanan zorlanmaz;
        mevcut dar wavelet/loss protokolü durur ve yeni araştırma kararı gerekir.
        '''),cell('code',"if MODE == 'research':\n    execute_step('train')\nelse:\n    print('Recovery tamamlandı; eğitim başlatılmadı.')")])
    cells.extend([cell('markdown','## 7 — İlerleme ve çıktıların yeri'),cell('code',"execute_step('status')\nprint('Durum:',ROOT/'STATUS.md')\nprint('Hazırlanmış tablolar:',ROOT/'data')\nprint('Checkpointler:',ROOT/'runs')"),
                  cell('markdown','''
                  ## 8 — İnceleme paketi ve tam dosya envanteri

                  Küçük inceleme ZIP'i modelleri içermez. Prepared ZIP'i tabloları içerir.
                  Ağırlıklar/raw veriler Drive klasöründedir; tam yedek için workspace
                  klasörünün tamamını indirin. `full_artifact_inventory.json` tüm dosyaların
                  hashlerini listeler; aktif oturum loglarini ayri belirtir. Runtime kapanırsa notebooku baştan çalıştırın.
                  Sert VM kapanmasından sonra `.writer_lease` kalmışsa başka yazıcı
                  olmadığını doğrulamadan kilidi kaldırmayın. Ortam/sürüm değişirse eski
                  çalışma sessizce devam etmez. Platformlar arasında bit eşitliği garanti değildir.
                  '''),cell('code',"execute_step('bundle')\nprint('İnceleme paketi:',ROOT/'reports/advisor_latest_review_bundle.zip')\nprint('Tam envanter:',ROOT/'reports/full_artifact_inventory.json')")])
    for i,c in enumerate(cells):
        c['id']=f'advisor-v2-{phase}-{i:02d}'
        if c['cell_type']=='code':compile(c['source'],name+str(i),'exec')
    notebook={'cells':cells,'metadata':{'colab':{'name':name,'provenance':[]},
        'kernelspec':{'display_name':'Python 3 (orchestrator)','language':'python','name':'python3'},
        'language_info':{'name':'python'},'accelerator':'GPU'},'nbformat':4,'nbformat_minor':5}
    if render_only:
        return notebook
    target=ROOT/'notebooks'/name
    target.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8',newline='\n')
    return target


def build_workflows():
    """Three task-oriented entry points; the versioned v2 entry points stay intact."""
    destination = ROOT / 'notebooks' / 'workflows'
    destination.mkdir(parents=True, exist_ok=True)
    descriptions = {
        'recovery': ('01_recover_data.ipynb', 'Eksik hazırlanmış tabloları kurtar',
            'Eski A ve B/C/D tablolarını sabit ham snapshot’tan yeniden oluşturur. '
            'Özgün SHA eşleşmesi zorunludur. Eğitim yapmaz. Tablolar zaten tam ise atlayın.'),
        'research': ('02_research.ipynb', 'Kontroller ve isteğe bağlı deneyler',
            'Her oturumda tek aşama seçin: basic → full → isteğe bağlı wavelet → loss. '
            'Aşamalar aynı yeni workspace ve sürümü kullanır. Varsayılan eğitim kapalıdır. '
            'Bu, dondurulmuş protokolün yeni ortamda tekrar üretimidir; yeni yöntem protokolü değildir.'),
        'archive': ('03_audit_archive.ipynb', 'Tarihsel finalin bütünlüğünü denetle',
            'Yalnızca mevcut dosyaları ve hashlerini okur. Model yüklemez, tahmin veya '
            'yeni test üretmez. Günlük araştırma için zorunlu değildir.'),
    }
    for mode, (name, title, description) in descriptions.items():
        notebook = build('final' if mode == 'archive' else 'basic', render_only=True)
        cells = notebook['cells']
        cells[0] = cell('markdown', f'''# {title}

{description}

**Yayın:** advisor-notebooks-v2.1.0 · **Depo:** umutergul74/YeniBotDeney

**Girdi:** Drive `MyDrive/yeniBot/advisor_experiments/colab_v1` arşivi.
**Çıktı:** ayrı workspace; veriler `data/`, modeller `runs/`, raporlar `reports/`.
Drive hesabı: `icinbedava34@gmail.com`. Bağlarken hesabı kontrol edin.

**Başarı ölçütü:** işlem hatasız tamamlanır, `STATUS.md` ve inceleme paketi oluşur.
Bu teknik başarı, modelin iyi performans verdiği anlamına gelmez.

Hücreleri yukarıdan aşağı çalıştırın. İlk kurulum paket indirebilir.
Eğitim için T4 gerekir. Aynı workspace'e ikinci oturumdan yazmayın.
Kesintiden sonra aynı sürüm/ayarlarla baştan çalıştırın; uyumlu checkpointler kullanılır.
v2.0.x workspace'ine v2.1.0 ile devam etmeyin; yeni WORKSPACE_ID kullanın.
''')
        settings = cells[2]['source']
        settings = settings.replace("MODE = 'recovery'", f'MODE = {mode!r}')
        settings = settings.replace("WORKSPACE_ID = 'advisor_protocol_v2'", f"WORKSPACE_ID = 'advisor_v21_{mode}_001'")
        settings = settings.replace(RELEASE, 'advisor-notebooks-v2.1.0')
        settings = settings.replace('umutergul74/yeniBot.git', 'umutergul74/YeniBotDeney.git')
        settings = settings.replace('/content/advisor_reproducible_repo', '/content/advisor_deney_v21_repo')
        if mode == 'research':
            settings = settings.replace("PHASE = 'basic'", "PHASE = 'basic'  # @param ['basic', 'full', 'wavelet', 'loss']")
            settings = settings.replace("EXPERIMENTS = ['A']", """EXPERIMENTS = {
    'basic': ['A'],
    'full': ['B', 'C', 'D'],
    'wavelet': ['W_ON'],
    'loss': ['L_WEIGHTED_BCE', 'L_FOCAL', 'L_BCE_PEARSON', 'L_FOCAL_PEARSON'],
}[PHASE]""")
            settings += "\nprint('Seçilen aşama:', PHASE, '| Deneyler:', EXPERIMENTS)\n"
            settings += "print('Planlanan fold × seed:', len(EXPERIMENTS) * 38 * 3, '| Eğitim izni:', ALLOW_TRAINING)\n"
            cells[1]['source'] += '''
| Aşama | Amaç | Önkoşul | Yeni eğitim sayısı |
|---|---|---|---:|
| basic | A: temel özellik/GRU kontrolü | Sabit ham arşiv | 114 |
| full | B/C/D: özellik ve mimari kontrolleri | Aynı workspace'te tamamlanmış A | 342 |
| wavelet | Nedensel filtre katkısı, isteğe bağlı | Tam A–D; desteklenen A kazananı | 114 |
| loss | Kayıp fonksiyonu katkısı, isteğe bağlı | A–D ve wavelet karşılaştırması | 456 |

Loss mevcut protokolde wavelet kararını gerektirir; wavelet atlanarak loss çalıştırılmaz.
08/09'un tarihsel sonucu wavelet kapalı + saf BCE'dir. Bu tüm yöntem ailesi için
üstünlük iddiası değildir. Aday seçimi validation BCE; Eylül 2026 testine dönülmez.
`ALLOW_TRAINING=False` hazırlığa izin verir; eğitim hücresi açıklama yazıp durur.
'''
            for c in cells:
                if c['cell_type'] == 'code' and "if MODE == 'research':" in c['source']:
                    c['source'] = "if ALLOW_TRAINING:\n    execute_step('train')\nelse:\n    print('Yalnızca hazırlık tamamlandı. Eğitim için ayarlarda ALLOW_TRAINING=True seçin.')\n"
        cells[2]['source'] = settings
        if mode == 'recovery':
            for c in cells:
                if c['cell_type'] == 'code' and c['source'].strip() == "execute_step('prepare')":
                    c['source'] = "for PHASE in ('basic', 'full'):\n    EXPERIMENTS = []\n    print('Kurtarılan tablo kapsamı:', PHASE)\n    execute_step('prepare')\n"
        # Refuse reuse of a checkout from the old source repository.
        for c in cells:
            if c['cell_type'] == 'code' and "assert not git('status'" in c['source']:
                c['source'] += "assert git('remote', 'get-url', 'origin') == REPO_URL, 'Yanlış kaynak depo; yeni runtime açın.'\n"
        notebook['metadata']['colab']['name'] = name
        if mode != 'research':
            notebook['metadata'].pop('accelerator', None)
        for i, c in enumerate(cells):
            c['id'] = f'advisor-workflow-{mode}-{i:02d}'
            if c['cell_type'] == 'code':
                compile(c['source'], f'{name}:{i}', 'exec')
        (destination / name).write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')


def build_barrier_workflow():
    notebook = build('basic', render_only=True)
    cells = notebook['cells'][:9]
    cells[0] = cell('markdown', '''# Seçici sinyal · özgün 38-fold bariyer karşılaştırması

**Amaç:** Önümüzdeki 10 bar içinde TP'ye SL'den önce ulaşacak örnekleri seçmek.
TP=1; SL ve timeout=0. Negatif karar kesin SL demek değildir. Aynı mumda çift temas: SL önce.

**Sabit veri:** 1 Mart 2022 04:00–28 Aralık 2025 02:00 UTC, 33.551 saat.
38 fold; train/validation/test bölüm boyutları 5040/1080/720; adım720;
purge24/embargo24; seq64 → 4977/1017/657 dizi. Test bölümü puanlanmaz.
Altı temel özellik, GRU, BCE, wavelet kapalı. Epoch seçimi validation BCE.
B25=2/5, B11=1/1, B12=1/2, B152=1.5/2, B22=2/2, B32=3/2.
Her aday 38 fold × 3 seed = 114 eğitim; toplam **684**. Uzun bir Colab çalışmasıdır.
Adayları ayrı oturumlarda çalıştırabilirsiniz; aynı aday kaldığı fold/epoch'tan devam eder.

**F1 maksimizasyonu ve otomatik kazanan kaldırıldı.** %60/%65/%70 precision
senaryoları seçilmiş politikalar değildir. Precision, recall, sinyal sayısı,
sinyalsiz dönemler, fold/seed istikrarı, SL/timeout ayrımı ve AP/BCE referansları raporlanır.
Aynı validation epoch seçimi için de kullanıldığından sonuçlar iyimser geliştirme sonuçlarıdır.

**Test komutu yoktur.** Eylül/Ekim okunmaz; final eğitim/test ayrı sonraki protokoldür.
A100 (NVIDIA A100-SXM4-40GB) seçin. Drive hesabı: icinbedava34@gmail.com. Eski workspace'i koruyun;
yeni varsayılan workspace ve advisor-selective-v1.1.0 sürümünü kullanın.
Çıktılar/checkpointler Drive'da. Aynı workspace'e eşzamanlı iki runtime yazdırmayın.
İnceleme ZIP'i satır bazlı validation tahminlerini içerir; tam model yedeği tüm workspace'tir.
''')
    cells[2]['source'] = cells[2]['source'].replace("MODE = 'recovery'", "MODE = 'research'")
    for old, new in {
        "WORKSPACE_ID = 'advisor_protocol_v2'": "WORKSPACE_ID = 'selective_a100_v11_001'",
        "EXPERIMENTS = ['A']": "EXPERIMENTS = ['B25', 'B11', 'B12', 'B152', 'B22', 'B32']  # İsterseniz tek aday seçin; her aday 114 eğitimdir.",
        RELEASE: 'advisor-selective-v1.1.0',
        'umutergul74/yeniBot.git': 'umutergul74/YeniBotDeney.git',
        '/content/advisor_reproducible_repo': '/content/advisor_selective_a100_v11_repo',
        '/content/advisor_isolated_runtime': '/content/advisor_selective_a100_v11_runtime',
    }.items():
        cells[2]['source'] = cells[2]['source'].replace(old, new)
    cells[2]['source'] += '\nos.environ["MPLBACKEND"] = "Agg"\nAUTO_DISCONNECT = True\nSUCCESSFUL_STEPS = {}\n'
    cells[4]['source'] = cells[4]['source'].replace("'research':'research_v2'", "'research':'selective_research_v1'")
    cells[6]['source'] += "\nassert git('remote','get-url','origin') == REPO_URL, 'Yanlış depo'\n"
    setup = cells[8]['source'].split('def execute_step(action):')[0]
    cells[8]['source'] = setup + dedent('''
    def step_identity():
        return (str(ROOT), RELEASE_TAG, tuple(EXPERIMENTS), ALLOW_TRAINING)

    def execute_step(action):
        order = ['prepare', 'train', 'report', 'bundle']
        for stale in order[order.index(action):]:
            SUCCESSFUL_STEPS.pop(stale, None)
        command = [RESEARCH_PYTHON, '-I', str(REPO_DIR/'scripts/advisor_selective.py'), action,
                   '--root', str(ROOT), '--legacy', str(LEGACY_ROOT), '--session', SESSION,
                   '--candidates', *EXPERIMENTS]
        if ALLOW_TRAINING: command.append('--allow-training')
        logged(command, action+'.log')
        SUCCESSFUL_STEPS[action] = step_identity()
    ''')
    for title, description, code in [
        ('5 · Sabit kohort hazırlığı', 'Ham snapshot hashleri, 33.551 ortak saat, özellikler ve 38 fold doğrulanır. Yeni veri indirilmez.', "import os\nos.environ['MPLBACKEND'] = 'Agg'\nexecute_step('prepare')"),
        ('6 · Eğitim', 'ALLOW_TRAINING=True seçin. Her aday 114 eğitim; checkpointler kalıcı. Aday listesi daraltılabilir.',
         "if ALLOW_TRAINING:\n    execute_step('train')\nelse:\n    print('Eğitim kapalı; ayarlarda ALLOW_TRAINING=True seçin.')"),
        ('7 · Seçicilik raporu', 'Seçili adayların 38×3 koşusu tamamlanmalıdır. Eşik veya kazanan otomatik seçilmez. Precision hedefleri betimseldir.',
         "if ALLOW_TRAINING:\n    execute_step('report')\nelse:\n    print('Rapor eğitim tamamlandıktan sonra hazırlanır.')"),
        ('8 · Ayrıntılı inceleme paketi', 'Validation tahminleri, history ve metrikler ZIP içinde. Ham veri/ağırlıklar için tüm workspace yedeklenir. Tüm seçili adayların eğitim, rapor ve ZIP adımları başarıyla tamamlanınca runtime otomatik bırakılır (AUTO_DISCONNECT=True). Hata varsa kapatılmaz.',
         "execute_step('bundle')\nprint('Raporlar:', ROOT/'reports')\nprint('Modeller:', ROOT/'runs')\nif AUTO_DISCONNECT and ALLOW_TRAINING and all(SUCCESSFUL_STEPS.get(step) == step_identity() for step in ('prepare', 'train', 'report', 'bundle')):\n    from google.colab import runtime\n    runtime.unassign()\nelse:\n    print('Otomatik kapatma yapılmadı: bütün aşamalar bu ayarlarla başarıyla tamamlanmalı.')"),
    ]:
        cells.extend([cell('markdown', '## '+title+'\n\n'+description), cell('code', code)])
    for i, c in enumerate(cells):
        c['id'] = f'barrier-study-{i:02d}'
        if c['cell_type'] == 'code': compile(c['source'], f'barrier:{i}', 'exec')
    notebook['cells'] = cells
    notebook['metadata']['colab']['name'] = '04_barrier_study.ipynb'
    notebook['metadata']['accelerator'] = 'GPU'
    target = ROOT/'notebooks/workflows/04_barrier_study.ipynb'
    target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1)+'\n', encoding='utf-8', newline='\n')


def build_all():
    archive=ROOT/'notebooks/archive/advisor_v1'
    archive.mkdir(parents=True,exist_ok=True)
    records=[]
    import hashlib
    for name in NAMES.values():
        payload=subprocess.check_output(['git','-C',str(ROOT),'show',BASELINE+':notebooks/'+name])
        target=archive/name
        if target.exists() and target.read_bytes()!=payload:
            raise ValueError('Historical notebook archive changed')
        target.write_bytes(payload)
        records.append(hashlib.sha256(payload).hexdigest()+'  '+name)
    (archive/'SHA256SUMS').write_text('\n'.join(records)+'\n',encoding='utf-8',newline='\n')
    for phase in NAMES:print('Generated',build(phase))
    build_workflows()
    build_barrier_workflow()


if __name__=='__main__':build_all()
