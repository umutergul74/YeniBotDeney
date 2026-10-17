# Neden analizi ve sınırlı çözüm yoklaması — önceden yazılan plan

exp-019-root-cause-probes; ebeveyn exp-018-validation-stability.

Kullanıcı neden ve çözüm analizi ile ../yeniBot projesinden fikir alınmasını istedi.
Dış proje salt okunur; yerel değişiklikleri ve farklı protokolü korunur.

Hipotezler ve karşı kanıt:
- H1: sigmoid puan ölçeği sorunu. Erken validation üzerinde öğrenilen kalibrasyon,
  geç validation BCE/Brier'ını iyileştirmezse yalnızca kalibrasyon çözümü desteklenmez.
- H2: seed oynaklığı. Aynı fold üç seed eşit ortalaması, eşleşmiş tek seed ortalamasına
  göre AP/AUC/BCE ve kötü dönemleri iyileştirmiyorsa ensemble çözümü desteklenmez.
- H3: mutlak eşik aktarımı. Erken validation puanlarının %90 kantilinden sabitlenen
  eşik sonraki bölümde sinyal kaybını azaltabilir; precision'ın korunması ayrıca ölçülür.
- H4: epoch seçimi/separation çatışması. Geç epoch geçmişlerinde daha yüksek AP ama
  kötü BCE bulunması hipotezi destekler; aynı validation'da AP maksimumunu seçerek
  yeni model başarısı ilan edilmez. Checkpointler değiştirilmez.
- H5: girdi dağılımı değişimi. Yalnızca orijinal eğitimle hash kimliği eşleşen girdiler
  kullanılabilir; farklı yerel snapshot'tan neden sonucu çıkarılmaz.

Yoklama: her fold'un mevcut 1017 validation tahmininin ilk500 satırı post-processing
fit/quantile kaynağı; sonraki10 satır etiket olgunlaşması boşluğu; son507 satır
karşılaştırma. Bu eski train/validation sınırını veya epoch seçimini değiştirmez.
ÖNEMLİ: model epoch'u tüm validation ile seçildiğinden son507 bağımsız holdout DEĞİL;
bu sonuç yalnızca mekanizma araştırmasıdır, kabul/test sonucu değildir.

Kanallar: seed42/43/44 ve eşit aritmetik seed ortalaması; foldlar karıştırılmaz.
Dönüşümler: raw, eski projedeki pozitif eğimli sigmoid (sklearn LogisticRegression
C=1 raw-score input), isotonic. Negatif sigmoid katsayısıyla sıralama ters çevrilmez;
bu durumda erken bölüm pozitif oranı sabit fallback olarak kaydedilir.
Sabit raporlama eşikleri0.5/0.7 ve erken bölümden q90. Yeni threshold taraması yok.
Hedef metrikler AP/AUC, BCE, Brier, erken pozitif oranı referansı, sinyal sayısı/precision.
Kalibrasyon 500 satırla özellikle isotonic için az veri; 10 saatlik etiketler bağımlı.

Ekim/Eylül test verileri açılmaz. GRU yeniden eğitilmez. En iyi seed/fold seçilmez.
Kalibrasyon/ensemble başarısı gösterilmeden dondurulmuş yürütücüye eklenmez.

## Ek hipotez — hesaplamadan önce, 17 Ekim

Eski projenin `holdout._aggregate_holdout_predictions` yöntemi aynı zamanda farklı
eğitim pencerelerinin puanlarını ortalıyor. H6: aynı dönem seed ortalaması yerine
komşu iki eğitim penceresinin ortalaması kararlılığa yardımcı olabilir. Mevcut
tahminlerde yalnızca iki komşu fold'un ortak297 validation saati kullanılacak;
aynı saatlerde eski3 seed ortalaması, yeni3 seed ortalaması ve altı modelin eşit
ortalaması karşılaştırılacak. 37 çift × 6 bariyer. Daha sonraki fold'ların geçmiş
saatlere tahmini eklenmeyecek. Her iki eğitim penceresi bu ortak saatlerden önce
biter; buna rağmen epoch seçiminde ilgili validation kullanılmış olduğundan bu
yoklama da bağımsız OOS sayılmaz. Eski projenin36-model yapısının doğrulaması değil.
