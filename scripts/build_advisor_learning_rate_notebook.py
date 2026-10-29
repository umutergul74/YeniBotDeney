"""Reuse the proven setup/storage cells; one new A6 learning-rate candidate."""
import json
from pathlib import Path
from scripts.build_advisor_feature_notebook import build as original

ROOT=Path(__file__).resolve().parents[1]


def build():
    nb=original()
    cells=nb['cells']
    cells[0]['source']='# A6 GRU — yalnız öğrenme hızı 0.001 → 0.0001\n\nA100 ve icinbedava34@gmail.com hesabıyla çalıştırın. Eski A6 kontrolü yeniden eğitilmez.\n38 fold × 3 seed = 114 yeni eğitim; veri, özellikler, 2/5 ATR, loss, patience ve eşik aynı.\nFinal test yok. Sonuç: bir grafik, özet ve eşleşmiş fold/seed tabloları.\nYeni Colab oturumunda hücreleri sırayla çalıştırın. Aynı workspace kesilirse devam eder.\n'
    cells[1]['source']=cells[1]['source'].replace("ROOT=Path('/content/drive/MyDrive/yeniBot/advisor_experiments/feature_comparison_v1/a100_001')", "SOURCE=Path('/content/drive/MyDrive/yeniBot/advisor_experiments/feature_comparison_v1/a100_001')\nROOT=Path('/content/drive/MyDrive/yeniBot/advisor_experiments/learning_rate_v1/a6_lr0001_a100_001')")
    cells[1]['source']=cells[1]['source'].replace("RELEASE='advisor-feature-comparison-v1.0.0'","RELEASE='advisor-learning-rate-v1.1.0'")
    cells[1]['source']='\n'.join(line for line in cells[1]['source'].splitlines() if not line.startswith(('REPORT_RELEASE=','ALLOW_TRAINING=')))+'\n'
    cells[2]['source']='## İzole ortam\nEski çalışmayla aynı kilitli Python/paketler ve A100 kullanılır. Eski veri salt okunur; yeniden veri çekilmez.\n'
    cells[3]['source']=cells[3]['source'].replace("['prepare','train','report','bundle']","['prepare','train','report']").replace('scripts/advisor_feature_comparison.py','scripts/advisor_learning_rate.py').replace("'--root',str(ROOT),'--legacy',str(LEGACY)","'--root',str(ROOT),'--source',str(SOURCE),'--experiment','A'").replace("    if ALLOW_TRAINING:command.append('--allow-training')\n",'')
    cells[4]['source']='## Kontrol verisini, 114 sonucu ve çalışma kimliğini doğrula\n'
    cells[6]['source']='## A6, öğrenme hızı 0.0001 — 114 eğitim\nKontrol sonuçları korunur; yeni workspace içinde tamamlanan eğitimler atlanır.\n'
    cells[8]['source']='## Tek grafik ve karşılaştırma tabloları\nTüm 114 eğitim tamamlanmadan özet üretilmez.\n'
    cells[9]['source']="step('report')\nfrom IPython.display import display, Image\ndisplay(Image(filename=str(ROOT/'reports/comparison.png')))\nprint((ROOT/'reports/summary.csv').read_text())\nprint('Review ZIP:',ROOT/'reports/learning_rate_review.zip')\n"
    cells[10]['source']='## Drive doğrulaması ve otomatik kapanış\nDosyalar yeniden bağlanınca doğrulanmadan oturum kapanmaz.\n'
    end=cells[11]['source']
    end=end[end.index('def digest(path):'):]
    cells[11]['source']="if 'report' not in SUCCESS:raise RuntimeError('Önce rapor hücresini tamamlayın')\n"+end
    return nb


def build_checkpoint():
    nb=build();cells=nb['cells']
    cells[0]['source']='# A6 — BCE / AP checkpoint seçimi\n\nA100, aynı kilitli ortam. 114 yeni ortak eğitim; 228 seçilmiş checkpoint.\nTrain5040 değişmez. Validation528 seçim +24 boşluk +528 değerlendirme: her bölüm465 hedef.\nLR0.001; ortak durdurma seçim BCE/patience15. AP erken durdurma denenmez.\nEski validation daha önce görülmüştür; bu final test değildir. Yeni Colab oturumunda sırayla çalıştırın.\n'
    cells[1]['source']=cells[1]['source'].replace('learning_rate_v1/a6_lr0001_a100_001','checkpoint_selection_v1/a6_bce_ap_a100_001').replace('advisor-learning-rate-v1.1.0','advisor-checkpoint-selection-v1.0.0')
    cells[3]['source']=cells[3]['source'].replace('scripts/advisor_learning_rate.py','scripts/advisor_checkpoint_selection.py').replace(",'--experiment','A'",'')
    cells[4]['source']='## Dondurulmuş A6 verisi ve bölüm sınırlarını doğrula\n'
    cells[6]['source']='## 114 ortak eğitim; BCE ve AP ağırlıklarını ayrı sakla\nDeğerlendirme bölümü epoch veya eşik seçimine katılmaz. Kesilen eğitim aynı kimlikle devam eder.\n'
    cells[8]['source']='## Seçimden türetilen eşiklerle değerlendirme\n0.5 referansı ve seçim bölümünün üst %5/%10 skor eşikleri. Otomatik kazanan yok.\n'
    cells[9]['source']="step('report')\nfrom IPython.display import display, Image\ndisplay(Image(filename=str(ROOT/'reports/comparison.png')))\nprint((ROOT/'reports/summary.csv').read_text())\nprint('Review ZIP:',ROOT/'reports/checkpoint_selection_review.zip')\n"
    return nb


if __name__=='__main__':
    (ROOT/'notebooks/workflows/06_learning_rate.ipynb').write_text(json.dumps(build_checkpoint(),ensure_ascii=False,indent=1)+'\n',encoding='utf-8',newline='\n')
