# Tamamlanmış A6/B37/C37/D37 sonuçlarının Drive incelemesi

24 Ekim 2026. Kullanıcı düzeltmesi üzerine Drive raporları okundu.
Önceki yanıtta bu karşılaştırmayı hâlâ yapılacak iş olarak sunmak yanlıştı;
yerel deney defterindeki planned durumu güncel değildi.

## Kaynak ve kontrol sınırı

Hesap `icinbedava34@gmail.com` olarak doğrulandı. Kaynak:
[feature_comparison_v1/a100_001/reports/explained_v1](https://drive.google.com/drive/folders/1sPnnsWA70j1aWu54OWtatrp0oB3dtcIc).
Üç CSV 22 Ekim'de oluşturulmuş; bu klasörde metin kopyaları ve Drive
kimlikleri saklandı. 456 satırda her model için 38 fold × 3 seed eksiksiz.
BCE/AP ortalamaları özet CSV ile eşleşiyor. Eşleşmiş farklar 684 satır.
Bu, rapor incelemesidir; model ağırlıkları, 456 ham tahmin dosyası ve bütün
eğitim geçmişleri yeniden denetlenmedi. Eğitim veya final test çalıştırılmadı.

## Genel sonuç

| Model | Ortalama validation BCE ↓ | Ortalama AP ↑ | Sayım bazlı F1, eşik 0,50 |
|---|---:|---:|---:|
| A: 6 özellik GRU | 0,594332 | 0,421212 | 0,154688 |
| B: 37 özellik GRU | 0,609470 | 0,404929 | 0,214006 |
| C: 37 özellik TCN | 0,602906 | 0,409587 | 0,190636 |
| D: 37 özellik paralel TCN+GRU | 0,601671 | 0,411476 | 0,177774 |

BCE/AP fold/seed eşit ortalamalarıdır; F1 toplam TP/FP/FN'den hesaplanır.
Eski raporun fold F1 ortalamasıyla aynı toplulaştırma değildir. Görülmüş
validation üzerinde seçim sonrası tanımlayıcı sonuçlardır; anlamlılık testi yok.

A'nın BCE/AP üstünlüğü üç seed'in ayrı dönem ortalamalarında da korunuyor.
B−A karşılaştırmasında BCE 114 grubun 93'ünde kötüleşiyor, 21'inde iyileşiyor.
37 girdide C, B'den 79/114; D ise 84/114 grupta daha düşük BCE veriyor.
Bu nedenle sonuç tam eşitlik değil: **özellik kapsamını düzeltmek ve mevcut
TCN/hibrit yapılarını kullanmak genel BCE/AP'de A'yı aşan bir çözüm getirmedi**.
A'nın nihai olarak yeterli veya her dönemde en iyi olduğu sonucu çıkmaz.

## Son dönemde farklı bir işaret var

Son fold AP, seed 42 / 43 / 44:

| A | B | C | D |
|---|---|---|---|
| 0,3383 / 0,3202 / 0,3724 | 0,4023 / 0,3753 / 0,4048 | 0,3781 / 0,3653 / 0,4123 | 0,3940 / 0,3820 / 0,4027 |

37 özellikli modeller bu foldda her seed'de A'dan daha yüksek AP gösteriyor.
Bu tek dönemden seçim yapılmaz; fakat “ek özelliklerin hiçbir faydası yok”
demek de doğru değildir. Genel ortalama ile dönem davranışı ayrılmalıdır.

B/C/D'nin ortalama seçilen epoch'u sırasıyla 1,37 / 1,50 / 1,48; A'da 4,44.
Erken epoch seçimi bir teşhis ipucudur, tek başına overfitting veya optimizer
hatası kanıtı değildir. Eğitim eğrileri incelenmeden nedeni kesinleştirilemez.

## Güncellenmiş öneri — uygulanmış deney değil

Bu dört yapıyı yeniden eğitmeyi önermiyoruz. Yeni geniş mimari taraması
yerine önce mevcut eğitim/validation eğrilerinde erken kötüleşmenin hangi
dönemlerde ortaya çıktığı incelenebilir. Ardından kullanıcı onayıyla GRU ve
diğer koşullar sabitken özellik gruplarının kontrollü ekleme/çıkarma etkisi
araştırılabilir. 6→37 toplu değişim hangi grubun yardımcı/hangi grubun zararlı
olduğunu ayıramaz. İyi girdileri belirlemenin de kararlılığı garanti ettiği
iddia edilmez; özellik ve mimari etkileri etkileşebilir.

Yeni özellik, eğitim ayarı, mimari, eşik, değerlendirme yöntemi veya deney
eklenmedi. Kullanıcının açık onayı olmadan öneriler uygulanmayacak.
