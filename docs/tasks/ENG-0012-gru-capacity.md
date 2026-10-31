# ENG-0012 — GRU kapasite deneyi hazırlığı

- 31 Ekim2026; durum:doğrulandı. Yetki:kullanıcı hidden128→64 deneyini hazırlamamızı istedi.
- Kapsam:advisor_capacity modülü/giriş/test; advisor_cnn_gru raporuna dış kontrol kaynakları;06 üretici/notebook ve test beklentileri; README, plan/ledger ve bu görev.
- Kabul:yalnız hidden boyutu değişir;114 eski kontrol doğrulanarak salt okunur kullanılır,114 yeni aday; aynı veri/split/epoch/eşik kuralları, bağımsız workspace, kesintiden devam.
- Sınır:gerçek eğitim veya final test çalıştırılmayacak; eski motor ve kullanıcı değişiklikleri korunur.
- Kontrol:kimlik/artifact sözleşmesi nedeniyle tam tests dizini bir kez çalıştırıldı:373 test ve14 alt kontrol geçti (1064 saniye). Günlük/XML:reports/gru-capacity-20261031/tests.log ve tests.xml. Mevcut PyWavelets yolu yalnız test alt sürecine eklendi; global paket değişmedi. OMP/MKL thread sayısı4, Agg backend kullanıldı. Gerçek araştırma eğitimi başlatılmadı.
- Bağımsız Sol/medium incelemesi PASS:tek ayar değişikliği, kontrol imzaları/hashleri, salt okunur kaynak, veri hizası, kesintiden devam ve rapor kanıtı denetlendi; testler tekrarlanmadı.
- Deney defteri34 kayıt/54 olay geçerli; notebook derleme/yeniden üretim ve ilgili eski akış regresyonları tam suite içinde geçti.
- Yayın:advisor-gru-capacity-v1.0.0; gerçek Colab/A100 eğitimi kullanıcı oturumunda yapılacak. Uzak CI sonucu ayrıca doğrulanmadı.
- Token kullanım ölçümü mevcut değil.
