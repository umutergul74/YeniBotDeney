# A6: AP checkpoint seçimi sorunu çözdü mü?

30 Ekim 2026 · exp-031 · Sonuç: **Hayır; bu deney kapsamında BCE kontrolü korunmalı.**

## Kapsam ve eksiksizlik

Drive hesabı icinbedava34@gmail.com doğrulandı. [Kaynak ZIP](https://drive.google.com/file/d/1tHHtkdx-sC3B1Njg8dROIEESGSe3PUh_/view),
çalışma `checkpoint_selection_v1/a6_bce_ap_a100_001`, commit
`2f7e2908c585a05ed616b28e42e23839def5a8f7`, NVIDIA A100-SXM4-40GB.
38 fold × 3 seed = 114 ortak eğitim akışı ve 228 checkpointin tahminleri mevcut.
798 ağırlık dışı dosyanın SHA256'sı completion kayıtlarıyla eşleşti.
684 eşik satırında eşikler selection tahminlerinden yeniden hesaplandı;
sinyal/TP/pozitif/örnek sayıları, AP ve BCE assessment tahminlerinden doğrulandı.
Seçilen epochlar history minimum BCE/maksimum AP ile eşleşiyor.
İki yöntemin assessment tarihleri ve etiketleri aynı; bölüm başına 465 hedef.
Sınır denetimleri geçti, kayıtlarda final test değerlendirme sayısı sıfır.

Review ZIP ağırlıkları içermez: 228 `.pt` dosyasının Drive üzerindeki içeriği
bu incelemede ayrıca indirilip doğrulanmadı. Eğitim/rapor eksikliği görülmedi;
mevcut kanıta göre tekrar eğitim gerekmiyor. Drive remount doğrulamasının
notebook çıktısı ZIP içinde bulunmadığından burada ayrıca teyit edilmedi.

Sabit koşullar [önceden kaydedilen planda](../checkpoint-selection-20261029/PLAN.md).
A6, LR0.001, 2/5 ATR ve 10 bar korundu. Validation seçim/değerlendirme olarak
ayrıldı. Bu yeni 465 hedeflik bölüm, eski 1017 hedefli validation ortalamalarıyla
doğrudan aynı-kohort karşılaştırması değildir. AP erken durdurma denenmedi;
iki checkpoint ortak BCE-patience15 eğitim yolu içinden seçildi.

## Ne bulduk?

| Ölçüt | Minimum BCE checkpoint | Maksimum AP checkpoint |
|---|---:|---:|
| Seçim bölümünde ortalama AP | 0.43788 | 0.46566 |
| Sonraki bölümde ortalama AP | 0.40410 | 0.40335 |
| Sonraki bölümde ortalama BCE, düşük iyi | 0.61186 | 0.64343 |
| Seçilen epoch ortalaması / medyanı | 5.92 / 5 | 7.91 / 7 |

AP seçimi seçim bölümünde +0.02778 AP sağlıyor; sonraki bölümde avantaj
yok (-0.00075). BCE +0.03157 kötüleşiyor. 114 eşleşmede assessment AP,
AP seçimiyle 38 kez yükseldi, 50 kez düştü, 26 kez eşit kaldı.
BCE ise 62 kez kötüleşti, 26 kez iyileşti, 26 kez eşit kaldı.
26 çalışmada aynı epoch seçildi; AP 54 çalışmada daha geç epoch seçti.
BCE seçiminin 42/114'ü ilk üç epochta. Erken epoch olgusu sürüyor fakat
AP'yi yükseltmek için daha geç checkpoint seçmek genel çözüm olmadı.

| Eşik kuralı | BCE precision | AP precision | BCE recall | AP recall | BCE sinyal | AP sinyal |
|---|---:|---:|---:|---:|---:|---:|
| Sabit 0.50 | %41.91 | %39.50 | %10.20 | %16.36 | 3982 | 6778 |
| Seçim skorlarında üst %5 eşiği | %41.15 | %41.22 | %8.59 | %9.11 | 3414 | 3617 |
| Seçim skorlarında üst %10 eşiği | %42.12 | %40.64 | %15.06 | %15.39 | 5853 | 6196 |

Üst %5/%10, precision hedefi değildir. Selection bölümündeki skor dağılımından
alınan sabit cutoff sonraki bölüme uygulanır. Sonraki bölümde gerçek sinyal
oranı üst %5 kuralında BCE için %6.44, AP için %6.82; üst %10 kuralında
%11.04 ve %11.69 oldu. Aynı sinyal sayısıyla karşılaştırma değildir.
Sabit 0.5'te F1 %16.41'den %23.13'e yükselse de precision düşüyor;
daha fazla sinyal ve recall, seçici sinyal kalitesinin iyileştiğini göstermez.
Pozitif etiket oranı %30.87. Precision, TP-first etiketini yakalamayı ölçer;
SL ve timeout ayrımını veya ekonomik getiriyi tek başına açıklamaz.

Sayılar 53,010 model-örnek değerlendirmesi üzerinden toplanmıştır;
seedler aynı tarihleri tekrar değerlendirir, bunlar bağımsız işlemler değildir.
Precision/recall/F1 toplam sayılardan, AP/BCE eşit run ortalamalarından gelir.

## Kararlılık ve açıklama

| Seed | BCE seçimi: assessment AP | AP seçimi: assessment AP |
|---|---:|---:|
| 42 | 0.40027 | 0.40607 |
| 43 | 0.40849 | 0.40321 |
| 44 | 0.40354 | 0.40078 |

İyileşme seedler arasında tutarlı değil. Son fold, üst %5 kuralında AP
seçimiyle seed42'de 1/1, seed43'te 3/3 doğru sinyal, seed44'te sıfır sinyal
veriyor. Toplam 4/4 üzerinden görünen %100 precision güvenilir bir başarı
kanıtı değil. BCE tarafı aynı fold'da 4/17. Model/sinyal sayısı kararlılığı
sorunu çözülmedi. Dönem grafiği `comparison.png`, sayılar `by_fold.csv`.

**Doğrulanmış gözlem:** seçim AP artışı sonraki döneme taşınmıyor; BCE
seçiminden vazgeçmek genel sıralama veya seçicilik iyileşmesi sağlamıyor.
**Olası açıklama:** 465 hedefli, zaman bağımlı seçim bölümünde AP'nin epochlar
arasında oynak olması ve dönem değişimi seçim avantajını kırılgan yapabilir.
Bu deney tek başına asıl nedeni, veri hatasını veya bütün model ailesinin
yetersizliğini kanıtlamaz. Daha kötü BCE de tek başına kalibrasyon bozukluğunun
ayrı bir teşhisi değildir.

## Karar ve sonraki adım

AP checkpoint seçimini iyileştirme olarak benimsemiyoruz; BCE kontrolü korunur.
Final test açılmadı. Önerilen sonraki adım yeni eğitimden önce mevcut history
ve tahminlerden başarısız dönemleri incelemek: train–selection kaybı ayrışması,
seçim–assessment etiket/skor dağılımı ve seed farkları aynı dönemlerde örtüşüyor
mu? Bu inceleme bir neden hipotezi daraltmalı; sonra yalnız bir kontrollü
değişiklik önerilmeli. Bu raporda yeni eşik veya model yöntemi seçilmedi.

## Tekrarlanabilir kontrol

`reports/checkpoint-review-20261030/verify.py` ile mevcut tahminler denetlendi;
kalıcı kopya `verify.py`. Girdi ZIP'i `reports/checkpoint-review-20261030/source.zip`
ve açılmış dosyaları `source/` altında Git dışında saklanır. `checks.json`
kaynak hashini ve kontrol kapsamını içerir. Üretim kodu değiştirilmedi,
pytest veya gerçek eğitim çalıştırılmadı.
