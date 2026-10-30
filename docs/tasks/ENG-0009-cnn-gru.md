# ENG-0009 — GRU ve CNN → GRU hazırlığı

- Durum: doğrulandı; 30 Ekim 2026.
- Yetki: kullanıcı, altı özellikli GRU kontrolüne karşı nedensel CNN→GRU deneyinin hazırlanmasını onayladı. Gerçek eğitim çalıştırılmadı.
- Başlangıç: 0bbce7a, codex/notebook-setup-separation.
- Kapsam: advisor_cnn_gru modülü/giriş betiği/testleri; checkpoint eğitim fonksiyonunda isteğe bağlı model kurucusu ve BCE-only seçim;06 notebook üreticisi ve ilgili test beklentileri; notebook README; yeni plan ve deney kaydı.
- Kabul: aynı veriler/bölmeler/özellikler/hyperparametreler; nedensel CNN; yalnız seçim BCE ile epoch; seçimden dondurulan eşikler; iki mimarinin ayrı imzaları;228 eğitim ve eksiksiz eşleşmiş rapor; kesintiden devam;A100/ortam/hash koruması.
- Kapsam dışı: eski model motoru, özellik/etiket üretimi, yeni veri, final test, gerçek eğitim. Önceden değişmiş/silinmiş kullanıcı dosyaları korunur.
- Kontrol: tam tests dizini bir kez çalıştırıldı:368 geçti,14 alt kontrol geçti;1 indeks kontrolü plan kaydı eklenmesiyle eşzamanlı okuma nedeniyle başarısız oldu (31/50 karşısında32/51 kayıt). İndeks üretimi tamamlandıktan sonra yalnız bu kontrol tekrarlandı:1 geçti. Günlükler reports/cnn-gru-20261030/tests.log ve ledger-recheck.log;1156.99 saniye. Mevcut yerel PyWavelets yolu yalnız test alt sürecine eklendi, paket kurulmadı. Model testleri sentetik girdiler/oyuncak model kullanır. Defter32 kayıt/51 olay geçerli; staged diff kontrolü geçti.
- Bağımsız inceleme: Sol/medium PASS; ek salt okunur inceleme özgün altı motor dosyasının önceki sabit sürümle aynı olduğunu doğruladı. Testler tekrarlanmadı.
- Sonuç:06 notebooku advisor-cnn-gru-v1.0.0 sürümüne hazır; gerçek A100 çalışması kullanıcı oturumunda yapılacak. Gerçek eğitim/Colab çalışması yerelde doğrulanmadı. Uzak CI sonucu yerel kontrol kanıtı değildir.
- Token kullanım ölçümü mevcut değil.
