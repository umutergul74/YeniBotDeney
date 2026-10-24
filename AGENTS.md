# Advisor araştırma ortamı

Bu depo `../yeniBot` projesinden bağımsız bir deney laboratuvarıdır. Amaç,
seçici sinyal üreten modelleri adım adım karşılaştırmak ve bütün deneylerden
öğrenilenleri korumaktır. Eski projenin kuralları buraya otomatik taşınmaz.

## Çalışma biçimi

- Önce `git status` ve ilgili dosyaları incele; kullanıcı değişikliklerini koru.
- Araştırmaya `research/README.md` ve `research/INDEX.md` üzerinden başla.
  Deney incelemesinde [yerel skill](.agents/skills/advisor-research-review/SKILL.md)
  kullan; notebook numaralarını araştırma geçmişi yerine koyma.
- İstenen işi en küçük anlaşılır değişiklikle tamamla. Gereksiz notebook,
  yapılandırma, bağımlılık veya süreç ekleme. Varsayılan tek ajanla çalış.
- Kullanıcının verdiği yetki kapsamında ilerle; aynı izni tekrar isteme.
  Yalnızca önerilmiş bir deney veya notebook düzenlemesi, yeni eğitim ya da
  final test çalıştırma izni değildir.

## Araştırma ve kayıt

- Kullanıcının açıkça istediği deney koşulları dışında sonuçları etkileyen
  özellik veya yöntem ekleme. Veri filtreleme, ön işleme, etiketleme, mimari,
  loss, kalibrasyon, ensemble, eşik/seçim kuralı ve sonuç toplulaştırma
  değişiklikleri buna dahildir. Ortak kodun varsayılanları da ek yöntemleri
  kendiliğinden etkinleştirmemeli. Yeni bir değişiklik gerekliyse gerekçesini
  ve beklenen etkisini sun; kullanıcı açıkça onaylamadan uygulama.
  Mevcut açık onayı tekrar isteme. Sonucu etkileyen hata bulunduğunda bunu
  bildir; yöntem değişikliği veya eski sonuçların üzerine yazma yoluyla gizleme.
- Veri, etiket, zaman bölmeleri ve seçim kurallarını sessizce değiştirme.
  Yeni yöntem veya koşul için yeni deney/run kimliği aç; eski deneye bağla.
- Başarılı, başarısız, yarım ve terk edilmiş deneyleri koru. Soru, koşullar,
  kanıt, sonuç ve karar kaydedilsin. `research/events/` ve `research/sources/`
  yayımlanmış kayıtlarına dokunma; düzeltmeleri yeni kayıt olarak ekle.
- Scaler train üzerinde öğrenilir. Model/epoch/eşik seçimi validation ile
  yapılır. Final test yalnızca önceden sabitlenmiş seçimi değerlendirir.
- Görülmüş Eylül 2026 final testinde yeni karşılaştırma, eğitim veya seçim
  yapma; yalnızca mevcut kanıtları raporla. Diğer dönemlerin uygunluğunu da
  kullanım geçmişinden doğrula; tarihe bakarak görülmemiş sayma.
- Başlangıç motorunu (`741d1d4`), eski `colab_v1` ve `evidence/` kanıtlarını
  koru. Uyuşmayan veri, checkpoint, kilit veya manifestin üstüne yazma.

## Kod, doğrulama ve Git

- Notebooklar ince kalsın; yeni notebook altyapısı
  `yenibot/experiment/advisor_*.py` altında olsun. Orkestrasyon değişikliğinde
  `docs/advisor-notebooks-v2.md` oku; çalışmanın kendi sürüm/ortam kilidini esas al.
- Mevcut ortamı kullan; global paket güncelleme. Araştırma alt süreçlerine
  host Python paketlerini karıştırma. Doğrulama için gerçek eğitim başlatma.
- Kontrolden önce değişen davranışı ve en küçük yararlı kontrol kapsamını belirt.
  `docs/test-budget.md` ve `scripts/advisor_test_scope.py` kurallarını izle:
  belge değişikliğinde diff/link/biçim kontrolü; küçük kod düzeltmesinde ilgili
  regresyonlar. Bilimsel veri/etiket/bölme, sabit artifact sözleşmesi, bağımlılık
  veya geniş kapsam değişikliğinde tam kontrolleri uygula. Geçen kontrolleri
  gerekçesiz tekrarlama; eşikleri veya testleri gevşetme.
- Göreve ait commit/push yetkisi vardır. Dondurulmuş release etiketlerini taşıma;
  main veya advisor baseline'a birleştirme ayrıca açık istek gerektirir.
- Drive/Colab için `icinbedava34@gmail.com` kullan; bağlayıcı kimliğini mümkünse
  doğrula. Veri, model, sır veya büyük ZIP dosyalarını Git'e ekleme.
