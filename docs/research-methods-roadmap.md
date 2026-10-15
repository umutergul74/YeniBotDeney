# Yöntem ve geliştirme kararı — 15 Ekim 2026

**Öncelik düzeltmesi:** Kullanıcının açıkladığı araştırma sırası gereği önce
[Kampanya 002'deki teşhis soruları](../research/campaigns/002-diagnostics.md)
plan olarak kaydedildi. Aşağıdaki yeni model/özellik önerileri bekleyen fikirlerdir;
aktif veya çalıştırılmasına karar verilmiş deneyler değildir. Yeni deney başlamadı.

## Şu an uygulanmış olanlar

Donmuş motor 741d1d4: nedensel özellikler, train-only ölçekleme, purge/embargo,
38 fold × 3 seed, validation BCE ile epoch/yöntem seçimi, hashli veri ve
checkpointler. Yeni arayüz bunları değiştirmez. Paket kilidi korunur; sırf
yeni sürüm çıktı diye paket yükseltilmez. v2.1.0 notebook düzeni sürümüdür,
yeni bir bilimsel model veya performans iyileştirmesi iddiası değildir.

08/09 deneyleri araştırma sorusu yanıtladı, zorunlu operasyon adımı değildir.
Tarihsel veride wavelet ve karmaşık losslar ortak seçim ölçütünde kazanmadı.
Eylül 2026 finali görülmüştür; yeni bir yöntemin başarısını orada seçemeyiz.

## Bir sonraki bilimsel protokol için öncelik sırası

Bu bölüm öneridir; henüz uygulanmış veya doğrulanmış sonuç değildir.

1. **Hipotez ve bütçe:** önce tahmin hedefi, tek ana ölçüt, aday listesi,
   eğitim bütçesi ve durdurma koşulu kaydedilsin. Daha fazla model denemek
   otomatik olarak daha iyi kanıt sağlamaz.
2. **Basit referanslar:** mevcut train-frekans referansına ek olarak düzenlileştirilmiş
   lojistik regresyon ve tek küçük ağaç tabanlı aday aynı nedensel özellikler,
   dönemler ve bütçeyle karşılaştırılsın. Bu bir üstünlük varsayımı değildir.
3. **Seçim ile değerlendirmeyi ayırma:** aday araması genişlerse zaman sıralı
   iç/dış validation düzeni tasarlansın. Standart rastgele K-fold kullanılmasın.
   scikit-learn'in nested CV örneği seçim yanlılığını açıklar; örnekteki rastgele
   bölme bu finansal seriye aynen uygulanmaz.
   [Kaynak](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html).
4. **Zaman sınırları:** hedef ufkuna göre purge ve embargo korunsun.
   `TimeSeriesSplit(gap=...)` zaman sırasını ve boşluğu destekler, fakat
   projedeki etiket ufku/embargo sözleşmesinin yerine tek başına geçmez.
   [Kaynak](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html).
5. **Belirsizlik ve kullanım amacı:** aynı foldlarda eşleştirilmiş farklar,
   dönem/seed tutarlılığı ve zaman bağımlılığını gözeten belirsizlik analizi
   planlansın. F1, sıralama ve olasılık kalibrasyonu farklı sorulardır;
   sonuç görüldükten sonra ana ölçüt değiştirilmesin.
6. **Yeni dokunulmamış dönem:** nihai aday ve eşik önceden dondurulduktan
   sonra ayrı protokolde değerlendirilsin. Tarih burada otomatik seçilmez.

Transformer, daha karmaşık loss veya otomatik geniş arama şu anda öncelik
değil: mevcut kanıt bunların bu veri için daha etkili olduğunu göstermiyor.
Önce basit adayların adil karşılaştırılması ve genelleme ölçümü gerekir.

## Tekrar üretim sınırı

Sabit seed tek başına farklı platform/sürüm/GPU'larda aynı sonucu garanti etmez.
Bu yüzden kod, paket ve çalışma ortamı birlikte kaydedilir; farklı ortam
eski sonuçla sessizce birleştirilmez.
[PyTorch tekrar üretilebilirlik notu](https://docs.pytorch.org/docs/stable/notes/randomness.html).

Kaynaklar 15 Ekim 2026'da kontrol edildi. Güncellik, doğrulanmamış yeni bir
yöntemi donmuş protokole sessizce eklemek anlamına gelmez.
