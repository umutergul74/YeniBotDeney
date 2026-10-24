# B37 GRU: öğrenme hızı deneyi

Durum: kullanıcı onayladı; Colab notebook hazır, eğitim henüz başlamadı.
Yerelde RTX 3050 Ti var; karşılaştırma A100 gerektiriyor. Açık Colab oturumu yok.

Soru: 0.001 yerine 0.0001 öğrenme hızı genellemeyi iyileştiriyor mu, yoksa
aynı bozulmayı yalnız geciktiriyor mu? Önceki kayıt: exp-024 / exp-021.

- Kontrol: tamamlanan feature_comparison_v1/a100_001 B37 GRU sonuçları.
- Aday: aynı 37 özellik, GRU, 2/5 ATR, 10 saat; yalnız learning_rate=0.0001.
- 38 fold × seed 42/43/44 = 114 yeni eğitim. Kontrol yeniden eğitilmez.
- Veri/etiket/bölmeler, scaler, batch=256, epochs=100, patience=15,
  dropout=0.2, weight_decay=0.0001, BCE ve minimum validation BCE seçimi aynı.
- Eski veri salt okunur; yeni sonuçlar learning_rate_v1/b37_lr0001_a100_001.
- Eski motor hashleri, veri hash'i ve Python/torch/GPU ortamı eşleşmeden çalışmaz.
- Final test, kalibrasyon, scheduler, ensemble veya yeni eşik seçimi yok.

Rapor: tek iki panelli train/validation BCE ve validation AP grafiği;
summary.csv, paired.csv ve seed_summary.csv. Eşik 0.5'te precision/recall/F1
ve sinyal sayısı da tabloda. Ortalamalar eşit fold/seed ağırlıklıdır.
Her iki koşulda tüm eğitimlerin mevcut olduğu ortak epoch aralığı çizilir.

Değerlendirme: eşleşmiş 114 eğitimde BCE ve AP değişimleri, daha iyi/kötü
çift sayıları ve seed bazlı sonuçlar birlikte incelenir. Yalnız daha geç
epoch seçilmesi başarı değildir. Validation tekrar kullanıldığı için bağımsız
test iddiası yok. Patience düşük hızda sınırlayıcı olursa açıkça raporlanır;
sessizce değiştirilmez. Otomatik kazanan seçilmez.

Kullanım: notebooks/workflows/06_learning_rate.ipynb dosyasını **yeni Colab
oturumunda A100 ile**, icinbedava34@gmail.com Drive hesabıyla sırayla çalıştırın.
Rapor ve ağırlıklar Drive yeniden bağlanarak doğrulandıktan sonra oturum kapanır.

Doğrulama: kullanıcının minimum test isteği kapsamında yeni deney sarmalayıcısına
odaklı dört regresyon; notebook syntax/üretim eşleşmesi ve defter/diff kontrolü.
Eğitim motoru, veri/etiket/bölme kodu ve bağımlılık kilitleri değişmedi.
Yerel kontroller A100 eğitiminin başarıyla tamamlandığı anlamına gelmez.
