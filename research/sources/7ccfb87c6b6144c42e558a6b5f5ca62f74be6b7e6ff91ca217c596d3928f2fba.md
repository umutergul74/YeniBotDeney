# GRU hidden64: sınırlı kazanım, genel çözüm değil

31 Ekim2026 · exp034 · Sonuç:karışık; otomatik model/eşik seçimi yok.

## Kanıt ve eksiksizlik

icinbedava34@gmail.com Drive kimliği doğrulandı.
[Kaynak ZIP](https://drive.google.com/file/d/1A8Y0aW_MEjRkZiMaIYrWPPmmR8yQR65E/view),
gru_capacity_v1/hidden64_a100_001, kod2942e1e4649467f9a8c3936c422274919cdbc1cb.
114 yeni hidden64 ve114 yeniden kullanılan hidden128 kontrolü mevcut.
1140 ağırlık dışı dosya hashi,228 run imzası/minimum-BCE epochu,684 eşik
satırının sinyal/TP/örnek/AP/BCE değerleri ve özetler doğrulandı. Bölüm başına
465 hedef, karşılaştırmada aynı tarih/etiket; sınır denetimleri geçti.
Kayıtlarda final test sayısı sıfır. Eksik eğitim/rapor bulunmadı.

Config kopyasında yalnız gru_hidden64→128 geri alındığında özgün kontrol
config'i birebir elde ediliyor.114 kontrol assessment dosyası önceki CNN-GRU
ZIP'indeki GRU dosyalarıyla byte düzeyinde aynı. Ağırlıklar ZIP dışında:
bu inceleme ağırlıkları veya Drive remount çıktısını ayrıca doğrulamadı.
Yeni eğitim, etiket üretimi veya test paketi çalıştırılmadı.

## Sonraki validation bölümünde sonuçlar

| Ölçüt | hidden128 | hidden64 |
|---|---:|---:|
| AP, yüksek iyi |0.40410|0.40251|
| BCE, düşük iyi |0.61186|0.60807|
| En iyi epoch ortalaması |5.92|7.11|
| En iyi epoch medyanı |5|5|

BCE farkı−0.00379;114 eşleşmenin66'sında iyileşti,48'inde kötüleşti.
AP farkı−0.00159;58'inde arttı,56'sında düştü. Ortalama epoch ileri gitse de
medyan aynı; erken epoch sorununun çözüldüğü söylenemez. BCE iyileşmesi
tek başına aşırı kapasitenin kesin neden olduğunu veya daha iyi kalibrasyonu
kanıtlamaz. İstatistiksel anlamlılık iddiası yapılmadı.

| Eşik kuralı |128 precision|64 precision|128 recall|64 recall|128/64 sinyal|128/64 sinyalsiz run|
|---|---:|---:|---:|---:|---:|---:|
|0.50|%41.91|%40.39|%10.20|%7.25|3982/2939|15/24|
|Seçim üst%5|%41.15|%41.78|%8.59|%7.89|3414/3090|3/4|
|Seçim üst%10|%42.12|%43.01|%15.06|%15.34|5853/5838|2/2|

Üst%10 sonucu bu deneyin en anlamlı olumlu gözlemi: neredeyse aynı sinyal
sayısında doğru TP sayısı2465→2511, precision+0.90 yüzde puan. F1%22.19→%22.62.
Ancak38 dönemin21'inde precision artarken17'sinde düşüyor; tutarlı genel
iyileşme değil. Seed42/44'te üst%10 precision artıyor,43'te düşüyor.
Üst%5 precision+0.63 puan fakat324 daha az sinyal; recall ve F1 düşüyor.
Üst%5 dönem precision21 kez artıyor,16 kez düşüyor,1 kez eşit.
Bu gözlemlerle sonradan üst%10'u yeni optimum eşik diye kilitlemiyoruz.

Üst%5/%10 precision hedefi değil; seçim skorlarından dondurulan cutoff.
Değerlendirmede gerçek sinyal oranları üst%10 için%11.04/%11.01,
üst%5 için%6.44/%5.83. AP/BCE eşit run ortalaması; precision/recall/F1
toplam sayılardan.53,010 model-örnek/mimari bağımsız işlem sayısı değildir.

## Seed/dönem kararlılığı

|Seed|128 AP|64 AP|128 BCE|64 BCE|
|---|---:|---:|---:|---:|
|42|0.40027|0.40491|0.61202|0.60751|
|43|0.40849|0.39449|0.60837|0.61188|
|44|0.40354|0.40812|0.61518|0.60483|

Seed42/44 iki ölçütte de iyileşirken43 kötüleşiyor. Üç seedin dönem ortalama
AP aralığı yaklaşık0.00822→0.01363 genişliyor; bu ölçüde kararlılık artmadı.
Bu aralık tam varyans ayrıştırması değildir.
Son fold üst%5'te128 için4/17,64 için4/14; iyileşen oran daha fazla doğru
sinyalden gelmiyor.64'te bir seed sıfır sinyal,diğeri1/1; küçük sayılara
dayanarak güvenilir başarı iddia edilemez.

## Araştırma kararı

Kapasite küçültmenin BCE ve üst%10 seçiciliğinde küçük yararı var; sıralama,
sabit0.5 başarımı ve seed tutarlılığında genel üstünlük yok. Sonuç
**karışık** olarak saklanır; hidden128 referansı hemen değiştirilmez,
hidden64 tamamen faydasız diye de atılmaz. Final teste geçiş kararı yok.

Önceki sonuçlarla birlikte, LR/AP-seçimi/CNN/kapasite değişiklikleri tek başına
kararlı seçici sinyal sorununu çözmedi. Bu incelemede yeni mimari/ayar taraması
başlatılmadı. Sonraki adım konuşulurken mevcut güçlü/zayıf dönem bulguları
korunmalı; aynı teşhisleri veya bu114 eğitimi tekrar yapmak gerekmiyor.

Kontrol betiği verify.py; checks.json kaynak ZIP hashini saklar. Ham ZIP
reports/capacity-review-20261031/source.zip içinde Git dışında. Ayrıntılar
summary.csv,by_run.csv,by_fold.csv,epochs.csv; mevcut tek grafik comparison.png.
