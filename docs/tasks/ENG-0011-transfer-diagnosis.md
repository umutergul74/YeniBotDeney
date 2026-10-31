# ENG-0011 — Yeni kanıttan aktarım teşhisi

- 31 Ekim2026; tamamlandı. Kullanıcı önceki işleri tekrarlamadan analizi sürdürmemizi istedi.
- Kapsam:research/analyses/cnn-gru-transfer-20261031; yeni deney kaydı/kaynak/INDEX ve bu görev. Önceki kullanıcı değişiklikleri korunur.
- Exp030/031/032 sonuçları okundu; önceki hesaplar tekrar çalıştırılmadı.
- Aynı ZIP hash'i kontrolüyle228 run için seçim–assessment aktarımı, iki mimarinin dönem korelasyonu ve best→last eğitim seyri hesaplandı. Tek grafik görsel olarak incelendi.
- Sonuç:[rapor](../../research/analyses/cnn-gru-transfer-20261031/REPORT.md). Kesin neden bulunmadı; yalnız hidden128→64 kapasite deneyi önerildi. Yeni eğitim/yöntem uygulanmadı.
- Üretim kodu değişmedi; tam test veya bağımsız kod incelemesi gerektiren davranış değişikliği yok. Model/epoch/eşik seçilmedi.
- Kaynaklar bağımlı tarihsel validation; eğitim ve validation kayıp ölçümleri farklı modlarda. Token kullanım ölçümü mevcut değil.
