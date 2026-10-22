# 22 Ekim: açıklanabilir raporlama güncellemesi

Bu, yeni eğitim deneyi değildir. A6/B37/C37/D37 girdileri, 2/5 etiketi,
veri/bölmeler, seedler ve minimum validation BCE ile epoch seçimi değişmez.
Kullanıcı A ve B run-directory tamamlanma çıktılarını paylaştı; C/D'nin
tamamlandığı henüz doğrulanmadı. Drive dosyaları bu düzenlemede incelenmedi.

## Yarım eğitime devam

Eğitim checkout'u `advisor-feature-comparison-v1.0.0` olarak kalır.
Yeni raporlama kodu bu checkout'a kopyalanmaz: bütün yenibot kaynaklarının
hash'i ve Git commit'i workspace kimliğinde sabit olduğu için bunu yapmak
mevcut eğitimin devamını engellerdi. Rapor yardımcısı ayrı dosyada, ayrı
`advisor-feature-reports-v1.0.0` yayını ve notebook içine yazılmış SHA256 ile
çalışır. Eski etiket taşınmaz. Yeni rapor sürümü yayımlanmadan güncellenmiş
notebookun rapor hücresi GitHub'dan indirilemez.

Aynı ROOT / aynı A100 / aynı eğitim sürümü kullanılır. Train komutu tamamlanmış
validation_metrics.json kayıtlarını atlar; yarım fold için last.pt'den sürer.
Eğitim checkpointleri veya dondurulmuş workspace kimliği değiştirilmez.
Çalışma aynı anda başka bir runtime'da açık olmamalıdır. Dört yapı ve bütün
seed/foldlar tamamlanmadan rapor üretilmez.

## Yeni çıktılar: reports/explained_v1

| Dosya | Okuma amacı |
|---|---|
| summary_at_050.csv | Ortak 0,50 referansı: ortalama BCE/AP, precision, recall, F1, sinyal/sinyalsiz grup oranı |
| 01_threshold_comparison.png | Dört modelin eşik eğrileri; TP/FP/FN sayıları toplanarak hesaplanır |
| 02_seed_thresholds.png | Her modelde üç seed'in precision, sinyal oranı ve sinyalsiz fold oranı |
| 03_period_stability.png | Dönemlere göre BCE, AP ve 0,50 sinyal oranı; AP için pozitif sınıf oranı referansı |
| latest_fold_thresholds.csv | Son fold'daki her seed/eşik için precision ve gerçek sinyal sayısı |
| paired_differences.csv | Aynı fold/seed'de B−A özellik genişletmesi; C−B/D−B mimari farkları |
| thresholds_all.csv | Toplam sinyal precision'ı ve sinyal veren grupların precision ortalaması ayrı |
| thresholds_by_seed.csv | Aynı hesaplar seed başına |
| thresholds_by_fold_seed.csv | Bütün eşiklerde TP/FP/FN/TN ve tanımsız metrikler |
| reference_thresholds.csv | 0,30/0,40/0,50/0,60/0,70/0,80 gösterim tablosu; seçim kuralı değildir |
| metrics_by_fold_seed.csv | BCE/AP ve epoch bilgisi, dönem kimliğiyle |
| report_identity.json | Rapor yardımcısının SHA256'sı; eğitim değişmedi/test değerlendirmesi yok |

Sinyal yoksa precision tanımsızdır (CSV boş / NaN); ortalamaya sıfır diye
eklenmez. `precision_signals` sayım ağırlıklıdır; `precision_active_mean`
yalnız sinyal veren gruplara eşit ağırlık verir. Her ikisi de sinyal desteği
ve sinyalsiz fold oranıyla okunur. Örtüşen pencereler ve seed tekrarları
toplam sinyal sayısını benzersiz/bağımsız işlem sayısı yapmaz.

Eski rapor dosyaları eski anlamlarıyla korunur; notebook yeni alt klasörü
gösterir. Epoch seçiminde kullanılan validation üzerinde tanımlayıcı rapor
üretilir. Kalibrasyon, otomatik eşik/kazanan seçimi, final test ve strateji
getirisi iddiası yoktur. Yazılım kontrolleri sentetik tahminlerle yapılır.

## Doğrulama

Yerel kapsam: rapor hesapları/çıktıları, özgün feature-comparison regresyonları,
notebook akışı ve kontrol kapsamı yönlendirmesi. İlk grup 34 test + 10 alt kontrol
geçti. Görsel eksen düzeni ve ek satır eşleşmesi kontrolünden sonra yalnız
etkilenen dört kontrol tekrar çalıştırıldı: 4 geçti. Toplam 35 farklı test
kapsandı; tam paket tekrar edilmedi. Üç grafik sentetik çıktıdan görsel olarak
incelendi. Loglar: `reports/feature-report-20261022.log` ve
`reports/feature-report-final-20261022.log` (Git dışında).
Colab/Drive üzerinde gerçek yürütme bu düzenleme sırasında yapılmadı.
