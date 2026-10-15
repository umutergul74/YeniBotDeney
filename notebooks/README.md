# Notebook giriş noktaları

**Araştırmanın ana ekranı [deney defteridir](../research/INDEX.md).**
Bu notebooklar kayıt sisteminin yerine geçmez. Yeni öneri önce plan olarak
kaydedilir; her yeni deney için yeni notebook oluşturmak gerekmez.
Buradaki araştırma notebooku mevcut A–D/wavelet/loss protokolüne aittir;
eşik/bariyer teşhisleri henüz uygulanmadı veya çalıştırılmadı.

Aktif kullanıcı akışı yalnızca **workflows/** içindeki üç notebooktur:

| Notebook | Ne zaman? | Ne üretir? |
|---|---|---|
| [01 · Veri kurtarma](workflows/01_recover_data.ipynb) | Eski hazırlanmış tablolar eksikse | SHA doğrulanmış A ve B/C/D tabloları |
| [02 · Araştırma](workflows/02_research.ipynb) | Sabit protokolü yeni izole ortamda çalıştırmak için | Seçilen aşamanın model, checkpoint ve raporları |
| [03 · Arşiv denetimi](workflows/03_audit_archive.ipynb) | Tamamlanmış final dosyalarını doğrulamak için | Salt okunur denetim raporu |

Bunlar zorunlu bir 01 → 02 → 03 eğitim zinciri değildir. Kurtarma sonuçları
research workspace'e otomatik taşınmaz; araştırma kendi girdilerini doğrular.
Drive hesabı `icinbedava34@gmail.com`; eski `colab_v1` snapshot'ı gereklidir.
Bu sürüm sıfırdan yeni piyasa verisi indiren bir araştırma protokolü sunmaz.

02 içinde `PHASE`: basic → full; yalnızca gerekliyse wavelet → loss.
Bir oturum bir aşamadır. Aynı sürüm ve workspace ile aşama değiştirilebilir;
aynı workspace'e eşzamanlı iki oturum yazamaz. Eğitim varsayılan kapalıdır.
basic 114, full 342, wavelet 114, loss 456 fold/seed çalışması planlar.

## Eski 08, 09, 10 ne oldu?

- **08:** Wavelet filtre katkısını ölçer. Tarihsel BCE 0.595259; filtresiz
  kontrol 0.594507. Bu protokolde iyileşme göstermedi. Artık 02'de isteğe bağlı.
- **09:** Weighted BCE, focal ve Pearson yardımcı kayıplarını karşılaştırır.
  Tarihsel seçim saf BCE. Artık 02'de isteğe bağlı; mevcut motor wavelet
  kararını gerektirdiğinden doğrudan basic → loss sıçraması desteklenmez.
- **10:** Yeni final testi değildir. Mevcut dosya bütünlüğünün denetimidir;
  artık adı açıkça 03 · Arşiv denetimi.

Eski 00–05 ana projenin tarihsel akışıdır. 06–10 sabit v2.0.2 uyumluluk
girişleridir; eski oturum bağlantıları kırılmasın diye korunur. Yeni kullanıcı
bunlardan başlamaz. `archive/advisor_v1` özgün, değiştirilemez kanıttır.

## Çalıştırma ve sürüm

Yeni notebooklar `advisor-notebooks-v2.1.0` yayınını YeniBotDeney'den yükler.
Colab'da notebooku açın, ayarları okuyun ve hücreleri sırayla çalıştırın.
Mevcut v2.0.x çalışma alanına devam etmek için özgün sürümü kullanın.
Yeni yayında yeni WORKSPACE_ID gerekir. Python/bağımlılık/GPU kimliği uyuşmazsa
devam engellenir. Hash uyuşmazlığını dosyayı silerek çözmeyin.

`STATUS.md` son işlemin durumudur; bütün aşamaların tamamlandığını tek başına
kanıtlamaz. `reports/advisor_latest_review_bundle.zip` küçük inceleme paketidir;
tam model yedeği için workspace'in tamamını saklayın.

Geliştirici: notebookları elle düzenlemek yerine
`python scripts/build_advisor_notebooks_v2.py` ile üretin.
Üç giriş aynı ortam/komut şablonunu paylaşır; bilimsel kod notebooklara taşınmaz.
