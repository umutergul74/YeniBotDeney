# Altı özellik: GRU ve CNN → GRU

30 Ekim 2026 · Kullanıcı onaylı hazırlık; eğitim henüz yapılmadı.

Soru: Aynı altı özelliği önce yerel nedensel CNN ile işlemek GRU'ya göre
sonraki validation döneminde seçicilik ve seed/dönem kararlılığını artırıyor mu?

Kontrol özgün A6 GRU. Aday: sola iki sıfır dolgulu tek Conv1D(6→32, pencere3),
GELU, ardından özgün iki katmanlı GRU(hidden128, dropout0.2) ve aynı çıkış başlığı.
Pooling, attention, batch normalization, ek özellik veya kalibrasyon yok.
CNN gelecek barı göremez; dizinin64 zaman adımı korunur. Parametre sayıları eşit
değildir: deney bu somut mimari değişikliğini karşılaştırır, kapasiteyi ayırmaz.

İki model de sıfırdan ve ayrı ağırlıklarla eğitilir: 38 fold × seed42/43/44,
toplam228 eğitim. Mevcut altı özellik, prepared shared37 veri hash'i
ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653,
2/5 ATR,10 bar ve özgün train5040/4977 hedef korunur.
Validation1080:528 seçim +24 boşluk +528 değerlendirme; ayrı63 bağlam ile
her bölüm465 hedef. Önceki checkpoint deneyindeki bölüm ayrımı aynıdır.
Scaler yalnız train'de fit edilir. Aynı seed+fold kuralı kullanılır; farklı
mimariler aynı ağırlık başlangıcı veya aynı minibatch sırası garantisi vermez.

LR0.001, AdamW weight decay0.0001, BCE loss, batch256, seq64, grad clip1,
en çok100 epoch, seçim BCE patience15. Her mimari kendi BCE'siyle durur;
en iyi epoch dondurulduktan sonra değerlendirme yapılır. AP epoch seçimi yok.
0.50 referansı ve seçim skorlarında üst %5/%10 cutoff'ları değerlendirmeye
değişmeden uygulanır; gerçekleşen sinyal oranları eşit olmak zorunda değildir.

AP/BCE eşit run ortalaması; precision/recall/F1 toplam sayılardan.
Sinyal sayısı/oranı, sıfır sinyalli run, eşleşmiş fold/seed ve dönem grafiği
raporlanır. Genel ortalama yanında dönem/seed tutarlılığı ve benzer kapsamda
precision incelenir; otomatik kazanan veya sonradan eşik optimizasyonu yok.
Tarihsel validation önceden görülmüştür; final test değildir. Örtüşen dönemler
ve aynı tarihleri kullanan seedler bağımsız örnekler değildir.

Mevcut06 notebooku, yeni advisor-cnn-gru-v1.0.0 yayını. Kaynak
feature_comparison_v1/a100_001 salt okunur; çıktı cnn_gru_v1/a6_a100_001.
A100 ve kaynakla aynı izole paket kilidi. Tamamlanmış dosya hash uyuşmazlığında
üzerine yazılmaz. Kesinti sonrası optimizer/RNG/last.pt ile devam edilir.
Mimari kimliği run imzasına dahildir; GRU/CNN checkpointleri karışmaz.
Review ZIP tahminleri içerir, ağırlıklar runs altında kalır. Drive yeniden
bağlanıp hashler doğrulanınca otomatik kapanır. Hazırlık gerçek eğitim başlatmaz.
