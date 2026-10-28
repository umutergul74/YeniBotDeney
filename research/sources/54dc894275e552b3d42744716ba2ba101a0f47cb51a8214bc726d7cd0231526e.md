# A6 GRU: düşük öğrenme hızı

Kullanıcı onayı: A6'yı 0.0001 öğrenme hızıyla dene; yeni notebook oluşturma.
Mevcut 06_learning_rate.ipynb uyarlanır. B37 v1.0.0 ve sonuçları korunur;
A6 için yeni v1.1.0 sürümü ve learning_rate_v1/a6_lr0001_a100_001 kullanılır.

Tek değişken learning_rate: 0.001 → 0.0001. A6'nın aynı altı girdisi,
GRU, 64 bar, 2/5 ATR/10 saat, train/validation bölmeleri, batch256,
patience15, maksimum100 epoch, dropout0.2, seed42/43/44 ve minimum
validation BCE seçimi korunur. 38 fold ×3 seed =114 yeni eğitim;
tamamlanan A6 kontrolü ve B37 deneyleri yeniden eğitilmez.

Amaç: 6/37 özellik ×0.001/0.0001 karşılaştırmasındaki eksik hücreyi tamamlamak.
Mevcut notebook tek grafik ve eşleşmiş validation tablolarını üretir.
Seçilmiş BCE/AP, seed/dönem değişkenliği ve sinyal sayıları birlikte incelenir;
yalnız daha geç epoch başarı sayılmaz. Eşik0.5 betimsel referans olarak kalır.
Final test veya otomatik eşik seçimi yok. Validation tekrar kullanılır;
fold/seedler bağımsız örnek değildir.

Durum: notebook hazır; eğitim kullanıcı tarafından Colab A100'de çalıştırılacak.
Yeni oturum, icinbedava34@gmail.com; sırayla hücreler. Drive doğrulamasından
sonra otomatik kapanış korunur. Eski B37 notebookunu devam ettirmek isteyen
v1.0.0 sürümünü kullanmalıdır; eski çalışma klasörüne yeni sürüm yazılmaz.
