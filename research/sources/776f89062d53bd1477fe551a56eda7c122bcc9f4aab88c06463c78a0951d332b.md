# Eşik ve bariyer teşhisi — analiz öncesi plan

Kullanıcı 15 Ekim 2026'da iki analizin yürütülmesini istedi. Plan sonuçlar
hesaplanmadan yazıldı. Kayıtlar: exp-011 ve exp-012. Eğitim/inference yok.

## Kaynak ve kapsam

- A_81029f6d6d48: 38 fold × seed 42/43/44; yalnızca validation_predictions.
- Girdi hashleri özgün review_manifest ile eşleşecek; 0.5 metrikleri kayıtlı
  validation metrikleriyle uyuşacak. Saat/etiketler hazırlanmış tabloya bağlanacak.
- Hazırlanmış A tablosu: f6346a93ee4b97125d00e8d26223ba11a141806cdff675934e033a00940977a8.
- Ham 1h: a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c.
- Bariyer evreni: 2022-03-01 04:00–2025-12-28 02:00 UTC, 33.551 saat.
  Son 10 saatlik hedef için ham verinin 2025-12-28 12:00'a kadarki kısmı gerekir.
- Eylül 2026 ve final_test_v1 okunmaz. Model yüklenmez, yeni eğitim yapılmaz.

## Eşik analizi

0–1 dahil 0.005 adımlı 201 eşik, p >= eşik pozitif. Sıfır pozitif tahminde
precision/F1=0. Ana metrik: 114 fold/seed'e eşit ağırlıkla precision, recall,
F1 ortalaması; ek olarak seed ortalamaları ve pooled sayılar raporlanır.
Örtüşen foldlar ve aynı saatlerin üç seedde bulunması bağımsız örnek sayılmaz.
Pooled sonuçlar ana fold ortalamasının yerine geçmez.

Grafikte 0.5 ve en yüksek ortalama validation F1 veren ızgara noktası gösterilir.
Eşit maksimumda yüksek eşik seçilir. Bu betimsel validation optimumudur;
deployment eşiği seçimi veya bağımsız test başarımı iddiası değildir. Model/epoch
zaten aynı validation ile seçildiğinden bu optimum iyimser olabilir.
0.2, 0.3, 0.4, 0.5 ve optimum açıklama tablosunda verilir.

## Bariyer analizi

TP/SL = 2/5, 2/2, 3/2 ATR; ufuk 10 saat. Giriş ilgili mumun kapanışı,
ATR(14) geçmiş/mevcut true range'in basit hareketli ortalaması; geleceğe bakmaz.
Kontrol ATR/OHLC ve 2/5 etiket/çıkış getirileri özgün tabloyla eşleşmeli.
Sabit motorun Python etiketleme döngüsü kullanılır; kod/ayarlar değiştirilmez.
Aynı mumda iki temas zarar-önce kategorisindedir; sayısı ayrıca verilir.
Üç senaryonun paydası aynı uygun timestamp listesi; eksik ufuk/ATR varsa durulur.

Kâr-önce, zarar-önce (belirsiz çift temas dahil), süre dolumu sayıları/yüzdeleri;
ayrıca timeout getirilerinde ortalama, medyan, yüzde 5/25/75/95, min/max ve
pozitif oranı. Timeout getirisi close(t+10)/close(t)-1; masraf/funding/slippage
yok. Pozitif getirili timeout yine mevcut ikili etikette 0'dır.
Etiket dağılımı teşhisidir; yeni bariyer kazananı veya strateji kârlılığı seçilmez.

## Saklama ve doğrulama

Girdiler salt okunur; yeni çıktı klasörü mevcutsa üzerine yazılmaz. Kaynak,
script ve paket sürümleri manifestte; rapor/CSV/PNG Git'te, ayrıntılı fold ve
satır çıktıları ayrı output klasöründe hash envanteriyle saklanır.
Sentetik eşik ve ilk-temas uç durumları test edilir. Yeni bilimsel analiz kodu
için kapsam politikasına uygun tam CPU CI bir kez çalıştırılır; gerçek eğitim yok.
