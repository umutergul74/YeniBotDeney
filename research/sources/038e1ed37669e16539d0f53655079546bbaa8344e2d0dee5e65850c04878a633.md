# Erken en iyi epoch: mevcut eğitimlerin teşhisi

Soru: A6/B37/C37/D37 karşılaştırmasında minimum validation BCE neden ilk
epoch'larda görülüyor; sonraki eğitim train BCE, validation BCE ve AP'yi
nasıl değiştiriyor?

Kontrol: exp-021'in mevcut 38 fold × 3 seed × 4 model çıktıları.
Yeni eğitim, test, özellik, eşik veya seçim kuralı yok. Arşiv salt okunur.

- 456 geçmişin bütünlüğü, epoch sırası, minimum BCE seçimi, patience ve
  kayıtlı özetlerle uyumu kontrol edilir. Kaynak motor hashleri doğrulanır.
- İlk → seçilen → son epoch karşılaştırılır; seçilen minimumdan son epoch'a
  BCE artışı tek başına kanıt sayılmaz. İlk → sabit ortak epoch karşılaştırması
  ve AP değişimi de incelenir.
- Tüm eğitimlerin mevcut olduğu ortak epoch aralığı kullanılır; geç epoch'larda
  yalnız uzun süren eğitimlerin kalmasından kaynaklanan yanlılık önlenir.
- Model, fold ve seed ayrımları korunur. Örtüşen validation pencereleri ve
  seedler bağımsız örnek kabul edilmez; anlamlılık iddiası yapılmaz.
- Train BCE güncelleme sırasında/dropout açık; validation BCE epoch sonunda
  eval modunda ölçülür. İkisinin mutlak farkı saf genelleme açığı değildir.
- Gözlem, olası neden ve doğrulanmamış çözüm ayrı raporlanır.

Doğrulama kapsamı: girdi/çıktı hashleri, arşiv CRC, sayısal tutarlılık,
grafik kontrolü, araştırma defteri ve diff. Eğitim motoru değişmediği için
geniş ML test paketi çalıştırılmaz.
