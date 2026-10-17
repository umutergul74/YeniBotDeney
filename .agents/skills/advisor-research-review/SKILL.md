---
name: advisor-research-review
description: Advisor araştırma deposunda deney planlama, validation sonuçlarını karşılaştırma ve model sorunlarının nedenini inceleme. Basit notebook veya belge düzeltmelerinde bilimsel analiz başlatmaz.
---

# Advisor deney incelemesi

Depo kökündeki [AGENTS.md](../../../AGENTS.md) kurallarını uygula.
[Araştırma düzeni](../../../research/README.md) ve
[deney defterinden](../../../research/INDEX.md) ilgili deneyi bul;
yalnızca soruyu yanıtlamak için gereken raporları ve kodu oku.

## İncele

- Soruyu bir cümlede belirt: neyi değiştirmek veya açıklamak istiyoruz?
  Mevcut kontrolü, değişecek tek unsuru ve başarı/başarısızlık ölçütünü ayır.
- Karşılaştırmadan önce veri/özellik/etiket kimliği, zaman bölmeleri, seed/fold
  kapsamı, seçilen epoch ve tahmin dosyalarını doğrula. Eksik kanıtı belirt;
  sırf rapor eksik diye tamamlanmış eğitimleri yeniden başlatma.
- Farklı bariyerler farklı hedeflerdir. Sınıf oranı, süre dolumu ve örnek sayısı
  değişimini göster; farklı hedeflerin BCE/F1 değerlerini tek başına kazanan
  seçmek için kullanma. Aynı örneklerde ve aynı toplulaştırmayla karşılaştır.
- Precision/recall/F1 yanında eşik ve sinyal sayısını göster. AP ve BCE tek
  eşikteki kararın değil, skorların ölçütleridir. Sıfır sinyalde precision'ı
  başarı gibi sunma; küçük örneklerin belirsizliğini belirt.
- Ham sigmoid skoru kalibre edilmiş olasılık sayma. Kalibrasyon ve eşik
  seçimini testten uzak tut. Validation içinde öğrenilen bir dönüşüm/eşiği
  aynı örneklerde değerlendirmek bağımsız doğrulama değildir. Zaman sırasını
  ve etiket ufkunu koru; daha önce epoch seçiminde kullanılan bölümü de belirt.
- Genel ortalamanın yanında dönem ve seed farklarına bak. Eşik, skor dağılımı
  ve sıralama becerisini ayır; eşiği düşürmeyi model kalitesinin çözümü sayma.
  F1, %60/%65/%70 precision veya başka bir hedefi kendiliğinden seçim kuralı yapma.

## Sonuçlandır

Gözlemi, olası açıklamayı ve doğrulanmış nedeni ayrı yaz. Eski `yeniBot`
çalışmaları yalnızca fikir kaynağıdır; farklı model/veri/protokoldeki sonucu
burada kanıt sayma ve o projenin dosyalarını bu görevin parçası olarak değiştirme.

Kısa bir tablo veya grafikle hangi koşulda ne bulunduğunu, neyin eksik kaldığını
ve sonraki tek kontrollü adımı açıkla. Çözüm doğrulanmadıysa bunu söyle.
Yeni deneyi çalıştırmadan önce mevcut kullanıcı isteğinin bunu kapsadığını
kontrol et; yalnızca öneri olan adımı yapılmış gibi sunma.

Yeni sonuç ve kararları önceki deneye bağlı, kanıt konumu belli kayıtlarla
koru. Bir raporun tamamlanması modelin başarılı veya final teste hazır olduğu
anlamına gelmez. Nihai testten önce model, eşik ve raporlama kuralları sabitlensin.
