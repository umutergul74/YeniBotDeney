# CNN → GRU sonuç incelemesi

31 Ekim 2026 · exp-032 · Sonuç: **Bu CNN→GRU adayı genel iyileşme sağlamadı; GRU kontrolü korunur.**

## Eksiksizlik ve karşılaştırma

Kullanıcının verdiği `C:/Users/Umut/Downloads/cnn_gru_review.zip` incelendi.
228/228 çalışma (iki mimari ×38 fold ×3 seed) mevcut. 1140 ağırlık dışı dosya
hashi completion kayıtlarıyla eşleşti. 684 eşik satırında eşik/sinyal/TP ve
örnek sayıları, AP/BCE ham tahminlerden doğrulandı; özet tablolar yeniden
hesaplanan değerlerle eşleşti. Seçilen epochlar history minimum BCE ile
uyumlu. Bölüm başına465 örnek, eşleşen tarih/etiket ve sınır denetimleri doğru.
Kayıtlarda final test sayısı sıfır. Eksik eğitim veya rapor sorunu görülmedi.
Ağırlıklar ZIP'te olmadığı için içerikleri ayrıca doğrulanmadı; Drive remount
doğrulaması bu yerel ZIP incelemesinin kapsamında değildir.

Kod dafcb21aa65883c7dc5c53d77a934e0cce565f55, A100-SXM4-40GB. Altı özellik
log_return, volume_log_zscore, realized_vol_14, gk_vol_14, atr_14_pct,
vwap_dist_atr. Kayıtlı veri SHA256 ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653.
Verinin kendisi ZIP dışında; hash protokol kaydıdır. Deney koşulları
[önceden kaydedilmiş planda](../cnn-gru-20261030/PLAN.md).

Yeni GRU'nun114 assessment tahmin dosyası, yereldeki önceki checkpoint
deneyinin BCE seçilmiş GRU dosyalarıyla byte düzeyinde aynı. Kontrol yeniden
üretilebildi. Bu, bütün veri/etiket üretiminin hatasız olduğunu tek başına kanıtlamaz.

## Sonuçlar

Epoch/eşik seçiminden sonraki validation değerlendirme bölümü:

| Ölçüt | GRU | CNN→GRU |
|---|---:|---:|
| Ortalama AP (yüksek iyi) | 0.40410 | 0.40078 |
| Ortalama BCE (düşük iyi) | 0.61186 | 0.61337 |
| En iyi epoch ortalaması | 5.92 | 5.04 |
| En iyi epoch medyanı | 5 | 4 |

CNN için AP114 eşleşmenin54'ünde arttı,60'ında düştü. BCE53'ünde iyileşti,
61'inde kötüleşti. Ortalama fark küçük; burada istatistiksel anlamlılık iddiası
yok. Yeni mimari erken epochta en iyi sonucun alınmasını ortadan kaldırmadı.

| Kural | GRU precision | CNN precision | GRU recall | CNN recall | GRU/CNN sinyal | GRU/CNN sinyalsiz çalışma |
|---|---:|---:|---:|---:|---:|---:|
| Sabit0.50 | %41.91 | %40.63 | %10.20 | %7.83 | 3982 /3153 | 15 /33 |
| Seçim üst%5 eşiği | %41.15 | %42.44 | %8.59 | %8.37 | 3414 /3226 | 3 /6 |
| Seçim üst%10 eşiği | %42.12 | %41.35 | %15.06 | %14.66 | 5853 /5801 | 2 /3 |

Üst%5, precision hedefi değil; seçim skorlarının üst%5'ini ayıran cutoff'tur.
Değerlendirmede gerçekleşen kapsam GRU%6.44/CNN%6.09. CNN üst%5 kuralında
precision +1.28 yüzde puan yükselirken daha az sinyal veriyor. Eşit kapsam
karşılaştırması değildir; tek başına genel üstünlük kanıtlamaz. F1 sırasıyla
GRU/CNN: sabit0.5'te%16.41/%13.13; üst%5'te%14.21/%13.98;
üst%10'da%22.19/%21.65. AP ve BCE eşik bağımsız değerlendirilir.

Sayılar mimari başına53,010 model-örnek değerlendirmesidir; seedler aynı
tarihleri tekrar değerlendirir, bağımsız işlem sayısı değildir. Precision,
recall,F1 toplam TP/sinyal/pozitiflerden; AP/BCE eşit run ortalamasından gelir.
Precision TP-first etiketiyle ilişkilidir, ekonomik kazanç oranı değildir.

## Kararlılık

Üst%5 precision38 dönemin18'inde arttı,19'unda düştü,1'inde aynı kaldı.
Seed42 ve43'te üst%5 precision artarken seed44'te azaldı. Ortalama AP:

| Seed | GRU | CNN→GRU |
|---|---:|---:|
|42|0.40027|0.39727|
|43|0.40849|0.40090|
|44|0.40354|0.40418|

Son fold'da üst%5 kuralıyla CNN üç seedde0/0,0/7,0/5 doğru/sinyal verdi;
toplam0/12. GRU4/17 idi. Küçük sayılar kesin başarısızlık oranı tahmini için
yetersizdir, ancak son dönemde iyileşme kanıtı yok. Sıfır sinyal precision'ı
başarı sayılmaz. Dönem/seed tutarlılığı ve sinyalsiz çalışma sorunu çözülmedi.

## Ne öğrendik, ne öğrenmedik?

Bu somut CNN(32 kanal,pencere3,GELU)→GRU değişikliğini, bu altı özellik ve
sabit eğitim koşullarıyla iyileştirme olarak benimsemiyoruz. GRU kontrolü
korunur; final teste geçiş kararı verilmez. Bütün CNN/RNN mimarilerinin işe
yaramadığını veya özelliklerin kesin yetersiz olduğunu söyleyemeyiz.
Parametre sayıları eşit değildir; sonuç yalnız bu aday için geçerlidir.

Yeni büyük eğitimden önce mevcut başarısız dönemlerde train–seçim kayıp
ayrışması ve seçim–değerlendirme skor/etiket değişimini yan yana incelemek
neden hipotezini daraltabilir. Bu bir öneridir; bu incelemede yeni yöntem,
eşik optimizasyonu, eğitim veya final test uygulanmadı.

Kontrol betiği `verify.py`, kapsam ve ZIP hashi `checks.json`; ayrıntılar
`summary.csv`, `by_run.csv`, `by_fold.csv`, `epochs.csv`. Tek mevcut grafik
`comparison.png`. Model kodu değişmedi; pytest çalıştırılmadı.
