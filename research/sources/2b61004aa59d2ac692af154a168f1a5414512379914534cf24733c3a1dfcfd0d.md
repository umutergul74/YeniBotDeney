# Özgün iki sorunun tamamlanması

Kullanıcı isteği: özgün A/B/C/D validation eşik eğrileri ve altı bariyerin
etiket/timeout dağılımları; sonradan yapılan eğitimlerin durumunu ayrı açıkla.

- A/B/C/D için arşivdeki 38 fold × 3 seed tahminleri; eşik 0–1, adım 0,005.
- Eşit fold/seed ortalaması; sıfır sinyalde precision=0 eski rapor uyumu için,
  ayrıca sinyalsiz grup sayısı ve sinyal üreten grupların precision ortalaması.
- 0,50 eski sonuçlarla doğrulanacak. Eşik seçimi veya F1 optimizasyonu yok.
- Altı mevcut bariyer: 2/5, 1/1, 1/2, 1.5/2, 2/2, 3/2; aynı 33.551 saat.
  Eski hashli etiket çıktıları yeniden kullanılacak; yeni etiket üretilmeyecek.
- Timeout getirilerinin yüzdelikleri ve ampirik dağılım grafikleri çıkarılacak.
- Test dosyası okuma, yeni model/özellik, eğitim veya kalibrasyon yok.
- Eğitim/epoch seçimi validation kullandığı için eğriler bağımsız performans değil.
