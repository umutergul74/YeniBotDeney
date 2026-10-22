# Notebook giriş noktaları

**Araştırmanın ana ekranı [deney defteridir](../research/INDEX.md).**
Bu notebooklar kayıt sisteminin yerine geçmez. Yeni öneri önce plan olarak
kaydedilir; her yeni deney için yeni notebook oluşturmak gerekmez.
Buradaki araştırma notebooku mevcut A–D/wavelet/loss protokolüne aittir;
Eşik/bariyer teşhisleri tamamlandı; sonuçlar deney defterindedir.
Yeni altı bariyerin eğitim karşılaştırması ayrı 04 girişindedir.

Aktif kullanıcı akışı **workflows/** içindeki görev notebooklarıdır:

| Notebook | Ne zaman? | Ne üretir? |
|---|---|---|
| [01 · Veri kurtarma](workflows/01_recover_data.ipynb) | Eski hazırlanmış tablolar eksikse | SHA doğrulanmış A ve B/C/D tabloları |
| [02 · Araştırma](workflows/02_research.ipynb) | Sabit protokolü yeni izole ortamda çalıştırmak için | Seçilen aşamanın model, checkpoint ve raporları |
| [03 · Arşiv denetimi](workflows/03_audit_archive.ipynb) | Tamamlanmış final dosyalarını doğrulamak için | Salt okunur denetim raporu |
| [05 · Özellik kapsamı düzeltmesi](workflows/05_feature_comparison.ipynb) | A6/B37/C37/D37; tek 2/5 bariyer, A100 | Eşit özellik kapsamıyla456 train/validation sonucu; test yok |
| [04 · Seçici sinyal](workflows/04_barrier_study.ipynb) | Altı bariyer, özgün 33.551 saat / 38 fold | Validation seçicilik raporları; test/eşik kilidi yok |

**Altı bariyer çalışması 04'tür:** [seçici sinyal planı](../research/analyses/selective-walkforward-20261016/PLAN.md).
`advisor-selective-v1.1.0` yayını ve yeni `selective_a100_v11_001`
workspace'i kullanılır. Önceki tek ayrımlı bariyer notebookları farklı kohorttur;
bu çalışma için kullanılmaz. Eski modeller ve sonuçlar korunur.
A100 (NVIDIA A100-SXM4-40GB) seçin; eğitim için `ALLOW_TRAINING=True`. Her aday 38×3=114 eğitim,
altısı toplam684; `EXPERIMENTS` ile bir veya birkaç aday seçip sırayla ilerleyin.
Aynı adayı aynı workspace'te yeniden çağırmak uygun checkpointten devam eder.
Prepare altı adayın ortak veri/split sözleşmesini denetler. Report yalnızca
seçili adayların tamamlanmış 114 koşusunu inceler; eksik kapsamda durur.
F1 maksimizasyonu yok. %60/%65/%70 precision senaryoları betimseldir;
minimum sinyal sayısı ve dönem tutarlılığı görülmeden eşik/başarı ilan edilmez.
Bu sürümde **test komutu yoktur**. Sonuçlar `selective_research_v1/<WORKSPACE_ID>/reports/`.
ZIP satır bazlı validation tahminlerini de içerir; tüm modeller için workspace yedeği gerekir.

Bunlar zorunlu bir 01 → 02 → 03 eğitim zinciri değildir. Kurtarma sonuçları
research workspace'e otomatik taşınmaz; araştırma kendi girdilerini doğrular.
Drive hesabı `icinbedava34@gmail.com`; eski `colab_v1` snapshot'ı gereklidir.
Bu sürüm sıfırdan yeni piyasa verisi indiren bir araştırma protokolü sunmaz.

02 içinde `PHASE`: basic → full; yalnızca gerekliyse wavelet → loss.
Bir oturum bir aşamadır. Aynı sürüm ve workspace ile aşama değiştirilebilir;
aynı workspace'e eşzamanlı iki oturum yazamaz. Eğitim varsayılan kapalıdır.
basic 114, full 342, wavelet 114, loss 456 fold/seed çalışması planlar.

## Özellik karşılaştırmasını düzeltme

18 Ekim çalışması için **05** kullanılır: [tasarım ve sabit koşullar](../research/analyses/feature-comparison-20261018/PLAN.md).
A–B özellik genişletmesini, B/C/D aynı37 girdiyle mimari farkını ölçer.

22 Ekim [rapor güncellemesi](../research/analyses/feature-comparison-20261018/REPORTING.md)
eğitim sürümünü sabit tutar; mevcut A/B sonuçları yeniden eğitilmez.
`reports/explained_v1` altında seed/dönem grafikleri, sinyal desteği ve son fold
tabloları bulunur. Rapor yardımcısı ayrı sürüm ve SHA256 ile doğrulanır.
A kontrolü dahil dört yapı aynı yeni A100 workspace'inde çalışır.

## Eski 08, 09, 10 ne oldu?

- **08:** Wavelet filtre katkısını ölçer. Tarihsel BCE 0.595259; filtresiz
  kontrol 0.594507. Bu protokolde iyileşme göstermedi. Artık 02'de isteğe bağlı.
- **09:** Weighted BCE, focal ve Pearson yardımcı kayıplarını karşılaştırır.
  Tarihsel seçim saf BCE. Artık 02'de isteğe bağlı; mevcut motor wavelet
  kararını gerektirdiğinden doğrudan basic → loss sıçraması desteklenmez.
- **10:** Yeni final testi değildir. Mevcut dosya bütünlüğünün denetimidir;
  artık adı açıkça 03 · Arşiv denetimi.

Eski 00–05 ana projenin tarihsel akışıdır. 06–10 sabit v2.0.2 uyumluluk
girişleridir; eski oturum bağlantıları kırılmasın diye korunur. Yeni kullanıcı
bunlardan başlamaz. `archive/advisor_v1` özgün, değiştirilemez kanıttır.

## Çalıştırma ve sürüm

Yeni notebooklar `advisor-notebooks-v2.1.0` yayınını YeniBotDeney'den yükler.
Colab'da notebooku açın, ayarları okuyun ve hücreleri sırayla çalıştırın.
Mevcut v2.0.x çalışma alanına devam etmek için özgün sürümü kullanın.
Yeni yayında yeni WORKSPACE_ID gerekir. Python/bağımlılık/GPU kimliği uyuşmazsa
devam engellenir. Hash uyuşmazlığını dosyayı silerek çözmeyin.

`STATUS.md` son işlemin durumudur; bütün aşamaların tamamlandığını tek başına
kanıtlamaz. `reports/advisor_latest_review_bundle.zip` küçük inceleme paketidir;
tam model yedeği için workspace'in tamamını saklayın.

Geliştirici: notebookları elle düzenlemek yerine
`python scripts/build_advisor_notebooks_v2.py` ile üretin.
Üç giriş aynı ortam/komut şablonunu paylaşır; bilimsel kod notebooklara taşınmaz.

## Seçici çalışma A100 güncellemesi

04 notebooku A100-SXM4-40GB profiline bağlıdır; eski T4 akışları değişmedi.
Yeni kod için yeni varsayılan workspace kullanın, eski dosyaları silmeyin.
MPLBACKEND=Agg ayarlarda ve prepare hücresinde açıkça atanır.
AUTO_DISCONNECT=True: seçili adayların prepare/train/report/bundle adımları
aynı ayarlarla başarılı olursa son hücre runtime.unassign() çağırır. Hata veya
eğitim kapalıysa oturum otomatik bırakılmaz. Kapatmayı önlemek için False seçin.
Veri, split, model, loss ve precision senaryoları değişmedi.
