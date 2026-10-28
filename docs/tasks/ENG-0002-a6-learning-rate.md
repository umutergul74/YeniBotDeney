# ENG-0002 — mevcut öğrenme hızı notebookunda A6

- Tarih: 2026-10-28. Yetki: kullanıcı A6/0.0001 deneyini onayladı;
  mevcut notebookun uyarlanmasını ve düşük test/token kapsamını istedi.
- Kaynak: b5a382204ee7a95497da784d1ae0722eeb322e56, codex/notebook-setup-separation.
- Kabul: A6 yönlendirmesi; ayrı workspace; eski B37 varsayılan CLI ve v1.0.0
  korunur; bilimsel ayarlar yalnız learning_rate farkını taşır; yeni notebook yok.
- Kapsam: yenibot/experiment/advisor_learning_rate.py,
  scripts/build_advisor_learning_rate_notebook.py,
  notebooks/workflows/06_learning_rate.ipynb, tests/test_advisor_learning_rate.py,
  bu görev kaydı ve exp-027 araştırma kayıtları/INDEX.
- Kapsam dışı: mevcut kullanıcı Engineering OS değişiklikleri, eski kanıtlar,
  eğitim motoru, etiket/bölme/bağımlılıklar, yerel eğitim, final test.
- Kontrol: yalnız tests/test_advisor_learning_rate.py; 7 passed in 64.46s; reports/a6-learning-rate-checks.log. Notebook syntax ve üretim eşleşmesi dahil.
- Bağımsız inceleme: Sol/medium PASS; rapor başlığı değişken çakışması giderildi.
- Defter: 27 kayıt/44 event doğrulandı; scoped diff kontrolü geçti. Colab eğitimi ve uzak CI çalıştırılmadı.
- Yayın: advisor-learning-rate-v1.1.0; eski v1.0.0 korunur.
- Kullanım telemetrisi: görev token sayıları mevcut değil.
