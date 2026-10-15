# Altı bariyer eğitim paketinin yöntem ve sonuç incelemesi

16 Ekim 2026. İncelenen kullanıcı paketi: `reports-20261015T205846Z-1-001.zip`.
Deney: exp-015-six-barrier-training. **Karar: teste geçilmemeli; bu çalışmanın
eğitim/kalibrasyon çıktıları ayrı keşif kanıtı olarak korunmalı.** Yeni eğitim,
yeni eşik seçimi veya Ekim test değerlendirmesi bu incelemede yapılmadı.

## 1. Temel yöntem sapması

Kullanıcının istediği sabit bariyer karşılaştırması yerine asistan önceki final
eğitim dönemini temel alan yeni tek ayrımlı bir protokol oluşturdu. Ayrıca
validation'ı epoch ve eşik seçimi için böldü, F1 maksimizasyonunu ve BCE-skill
aday sıralamasını kendisi ekledi. Bu kararlar kullanıcının özgün deney tasarımı
değildi. Ayrı plan yazılmış olması, eski deneyle karşılaştırılabilirliği sağlamaz.

| Özellik | Özgün geliştirme protokolü | Çalıştırılan altı adaylı protokol |
|---|---|---|
| Veri dönemi | 1 Mart 2022 04:00–28 Aralık 2025 02:00 UTC | 18 Aralık 2025–30 Ağustos 2026 |
| Ortak tablo | 33.551 saat | 6.144 saatlik fit kapsamı; aralarda boşluklar |
| Düzen | 38 yürüyen pencere, adım 720 saat | Tek sabit ayrım |
| Train | Her fold 5.040 satır / 4.977 dizi | 5.040 satır / 4.977 dizi |
| Validation | Her fold 1.080 satır / 1.017 dizi | Epoch: 552 / 489; eşik: 504 / 441 |
| Fold test bölümü | 720 satır / ayrı dizilemede 657 dizi | Bunun yerine planlanan 312 saatlik Ekim holdout |
| Bağlam | Bölüm içindeki ilk 63 satır | Testte bölüm öncesinden 63 satır eklenmesi |
| Seed kapsamı | 3 seed × 38 fold / aday | 3 seed × 1 ayrım / aday |
| Altı aday eğitim sayısı | 684 fold/seed eğitimi | 18 eğitim |

Train uzunluğunun aynı kalması yeterli değildir: tarihleri, rejimler, validation
uzunluğu, fold sayısı ve test bağlamı değişmiştir. Sonuçlar eski A/B/C/D veya
bariyer tanı metrikleriyle aynı kohort gibi karşılaştırılamaz. Eski kontroller
ile değişen bariyerlerin aynı timestamp/split/seed/ortamda olması gerekir.

Önemli ayrım: özgün `advisor.py` geliştirme yürütücüsü fold'un test bölümünü
sınır kontrolü için kullanır fakat bu bölümde tahmin/puanlama yapmaz;
`test_evaluations=0` kaydeder. 720/657 sayıları bölümün yapısını anlatır,
657 test tahmininin geçmişte gerçekten üretildiğini kanıtlamaz. Sonradan
yapılan Eylül final testi ayrı protokoldür. Bir sonraki plan bu iki kavramı
birbirine karıştırmamalıdır.

## 2. Pakette gerçekten ne var?

- Prepare, train ve freeze oturumları `complete`. Eğitim günlüğünde 18 ayrı
  seed koşusu ve 419 epoch satırı var. Son epoch ile seçilen epoch farkı tüm
  koşularda 15; patience ayarıyla tutarlı. Tüm modeller 100 epoch çalışmalı
  şeklinde bir gereklilik yoktur.
- Freeze kaydı altı adayın eşiklerini ve B11 seçimini içeriyor. Plan hash'i
  eşleşiyor. Freeze'deki 160 dosya hash'i envanterdeki karşılığıyla eşleşiyor.
- ZIP CRC kontrolleri geçti. Dış ve iç ZIP'teki 11 ortak üye byte olarak aynı.
  Envanterde bulunan ve pakette gerçekten yer alan iki artifact dosyası ayrıca
  hash ile doğrulandı: plan ve freeze.
- Her adayın 201 satırlık eşik tablosu var. Tablo maksimum ortalama F1 ve yüksek
  eşik tie-break kuralıyla yeniden kontrol edildi; kaydedilen eşiklerle eşleşti.
- Test tahminleri/test tamamlanma kaydı yok; freeze `test_evaluations=0`.
  Kullanıcı da testi çalıştırmadığını bildirdi. Bu, bütün Drive'ın bağımsız
  denetlendiği anlamına gelmez.
- İç ZIP'te bundle oturumu `running`: ZIP oluşturulurken oturum henüz kapanmadığı
  için bu durum paketlenmiş. Tek başına eğitim hatası veya bozuk ZIP kanıtı değil.

**Eksikler:** ham veri, model ağırlıkları, scaler değerleri, satır bazlı
validation/calibration tahminleri, `history.csv` ve seed bazlı metrik dosyalarının
kendisi pakette yok. Envanterde hashlerinin bulunması bu dosyaların byte
doğrulamasını sağlamaz. Bu nedenle bağımsız tahminden metrik hesaplama, seed
dağılımı, reliability/Brier/ECE, zaman blokları ve gerçek net getiri analizi
henüz yapılamaz. Aggregate tablolardan bunlar uydurulmadı.

## 3. F1 eşiklerinin gerçekte yaptığı

Aşağıdaki değerler yalnızca 10–30 Ağustos kalibrasyonundan, aday başına aynı
441 zaman damgası üzerinde üç seed ortalamasıdır. 1.323 bağımsız saat değildir.
Precision/recall/F1 ayrı ayrı seed ortalamalarıdır; ortalama P/R'den F1
yeniden hesaplanmamalıdır.

| Bariyer | Eşik | Pozitif karar % | Precision % | Recall % | F1 | Hep-pozitif F1 | F1 farkı |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2/5 | 0,010 | 100,00 | 39,00 | 100,00 | 0,56117 | 0,56117 | ≈0 |
| 1/1 | 0,255 | 98,03 | 51,27 | 98,96 | 0,67546 | 0,67368 | +0,00178 |
| 1/2 | 0,200 | 99,40 | 59,77 | 100,00 | 0,74822 | 0,74538 | +0,00284 |
| 1,5/2 | 0,130 | 100,00 | 46,03 | 100,00 | 0,63043 | 0,63043 | ≈0 |
| 2/2 | 0,020 | 99,70 | 37,68 | 99,80 | 0,54706 | 0,54695 | +0,00010 |
| 3/2 | 0,000 | 100,00 | 24,26 | 100,00 | 0,39051 | 0,39051 | ≈0 |

Pozitif etiket oranı p ise hep-pozitif kararın precision=p, recall=1,
F1=2p/(1+p). B12'nin p≈0,5941 değeri model olmadan bile F1≈0,7454 verir.
Yuvarlama/float hassasiyetinden gelen 10^-8 farklar anlamlı iyileşme değildir.

F1'i yükseltmek tek başına yanlış bir matematik işlemi değildir. Ancak F1
yanlış alarm maliyetini, işlem sayısını, sermaye kullanımını, getiriyi ve gerçek
negatifleri doğrudan temsil etmez. Bu görevde F1 maksimizasyonu seçici bir
karar mekanizması üretmemiştir. Yüksek recall kendi başına kötü değildir;
sorun bunun neredeyse her saate pozitif diyerek elde edilmesi ve referansa
ek katkının yok denecek kadar az olmasıdır.

## 4. Sorun yalnızca eşik değil

| Bariyer | Eğitim pozitif % | Kalibrasyon pozitif % | AP | AP / pozitif oranı | BCE | Referans BCE | BCE skill % |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2/5 | 31,14 | 39,00 | 0,47694 | 1,223 | 0,73377 | 0,68260 | −7,50 |
| 1/1 | 43,68 | 50,79 | 0,49088 | 0,966 | 0,70972 | 0,70321 | −0,93 |
| 1/2 | 54,07 | 59,41 | 0,60056 | 1,011 | 0,69836 | 0,68112 | −2,53 |
| 1,5/2 | 39,26 | 46,03 | 0,44482 | 0,966 | 0,72091 | 0,69945 | −3,07 |
| 2/2 | 29,13 | 37,64 | 0,41113 | 1,092 | 0,76524 | 0,67897 | −12,71 |
| 3/2 | 15,95 | 24,26 | 0,26285 | 1,083 | 0,68134 | 0,57698 | −18,09 |

Referans, eğitim dizi etiketlerinin pozitif oranını bütün kalibrasyon saatlerine
sabit olasılık olarak verir. Altı modelin ortalama BCE'si de bu referanstan kötü.
BCE ve AP eşik değişince düzelmez; skorların kendisinin değerlendirmesidir.
B25'te sıralama katkısı olabileceği halde olasılık kaybının kötü olması mümkündür.
Bu tablo tek başına sorunun kalibrasyon mu, rejim farkı mı, aşırı uyum mu olduğunu
ayırt etmez. Kalibrasyon işlemi otomatik çözüm olarak başlatılmamalıdır.

B12 en yüksek ham AP/F1'e sahiptir ama hedefi zaten daha yüksek pozitif oranlıdır;
AP lift'i yalnızca 1,011'dir. B11 otomatik seçilmiştir çünkü BCE skill'i diğer
adaylardan daha az negatiftir; **referansı geçtiği için değil**. Seçim kodunda
başarılı aday yoksa 'hiçbirini seçme' durumu bulunmaması ayrı bir yöntem açığıdır.
Bu aday seçimi bu incelemede geçersiz bir başarı kararı olarak işaretlenmiştir.
Farklı hedefler üzerinde normalize skill bile işlem kârlılığı sıralaması değildir.

## 5. 0,5 eşiği sorunu çözüyor mu?

Yalnızca mevcut eşik tablolarından okunan sabit referans; yeni eşik seçimi değil:

| Bariyer | Precision % | Recall % | F1 | Pozitif karar % |
|---|---:|---:|---:|---:|
| 2/5 | 46,13 | 25,39 | 0,32533 | 21,54 |
| 1/1 | 42,43 | 13,69 | 0,19973 | 16,33 |
| 1/2 | 60,03 | 76,72 | 0,67270 | 75,89 |
| 1,5/2 | 39,08 | 20,69 | 0,26633 | 23,96 |
| 2/2 | 45,42 | 24,90 | 0,31978 | 20,26 |
| 3/2 | 28,31 | 2,49 | 0,04498 | 2,49 |

0,5 tarihsel karşılaştırma için tutulabilir; optimal işlem eşiği olduğu söylenemez.
Eşiği yükseltmek precision'ı her adayda monoton artırmaz. Örneğin mevcut tabloda
B12'nin yaklaşık %10 karar oranındaki precision'ı %52,60; taban pozitif oranı
%59,41. B11'de bu örnek %37,17'dir, tabanı %50,79. Bunlar seçilmiş yeni politikalar
değil, daha az sinyalin otomatik olarak daha kaliteli sinyal olmadığını gösteren
betimsel örneklerdir. Seed ortalamaları tek bir birleşik confusion matrix değildir.

## 6. Eğitim davranışı

Günlükte aday adı yazmıyor. Aşağıdaki eşleme planın aday sırası ve kodun
ardışık yürütmesinden çıkarıldı; seed başına metric/history dosyalarıyla
doğrulanması gereken bir sınırlamadır. BCE değerleri logda 6 ondalığa yuvarlıdır.

| Aday | Seed 42/43/44 seçilen epoch | Toplam epochlar | En iyi validation BCE aralığı |
|---|---|---|---|
| B25 | 5 / 5 / 12 | 20 / 20 / 27 | 0,61832–0,62335 |
| B11 | 5 / 3 / 2 | 20 / 18 / 17 | 0,68147–0,68659 |
| B12 | 10 / 7 / 6 | 25 / 22 / 21 | 0,65738–0,66364 |
| B152 | 8 / 3 / 2 | 23 / 18 / 17 | 0,66369–0,66936 |
| B22 | 13 / 11 / 10 | 28 / 26 / 25 | 0,59222–0,59875 |
| B32 | 18 / 17 / 12 | 33 / 32 / 27 | 0,34677–0,37895 |

Train BCE düşerken geç epochlarda validation BCE'nin kötüleşmesi aşırı uyumla
tutarlı. Örneğin B25 seed44'te en iyi validation 0,61832 iken son epoch
validation 1,02903; son train BCE 0,27389. Kod best_state'i kullandığı için
son epoch'un kötü olması tek başına yanlış checkpoint seçildiğini göstermez.
Erken durma çalışmış görünür; başka dönemdeki kalibrasyon başarısını garanti etmez.

## 7. Eşik neye göre belirlenmeli?

Önce amaç tanımlanmalı; bu rapor yeni bir otomatik seçim ölçütü dayatmıyor.

**Araştırma sınıflandırma amacı:** Sabit 0,5 sonuçları ve eşikten bağımsız AP/BCE
referansları raporlanır. Precision–recall ve pozitif karar oranı birlikte
incelenir. Seçim gerekiyorsa önceden tanımlanmış minimum precision, yeterli
örnek/sinyal sayısı ve dönem/seed tutarlılığı koşulları altında recall veya
başka açık bir fayda hedefi optimize edilebilir. Minimum precision değerini
sonuçları gördükten sonra uygun görünecek şekilde seçmemeliyiz. F0.5 veya
balanced accuracy'ye körlemesine geçmek de aynı amaç tanımı sorununu çözmez.

**İşlem stratejisi amacı:** Yanlış pozitif/negatiflerin maliyeti ve uygulama
kuralları gerekir: giriş zamanı, ücret/slippage/funding, pozisyon çakışmaları,
sermaye ve işlem sıklığı, timeout getirileri, risk sınırları. Eşik bunlarla
tanımlı net faydaya göre yalnızca geliştirme verisinde belirlenebilir. Sadece
SL/(TP+SL) formülünü eşik yapmak doğru değildir: burada negatif sınıf hem
SL hem timeout içerir; kayıp sabit değildir, olasılıkların kalibrasyonu da
kanıtlanmamıştır. Bu ZIP bu analizi yapmak için yeterli değildir.

Her iki amaçta da 'hiçbir aday/politika yeterli değil' sonucu mümkün olmalı.
Başarı şartları kullanıcıyla netleşmeden yeni eşik veya kazanan kilitlenmez.

## 8. Doğru devam sırası — henüz yürütülmedi

1. Bu 18 eğitimi silmeden, 'özgün kohorttan farklı, keşif amaçlı' olarak arşivle.
   Mevcut freeze dosyasını yeniden yazma; test hücresini çalıştırma.
2. Sabit karşılaştırma sözleşmesine geri dön: 33.551 ortak timestamp; 38 fold;
   train/validation/test bölüm uzunlukları 5040/1080/720; adım 720;
   purge/embargo 24/24; seq64, seed42/43/44. Altı bariyer için yalnızca
   etiket parametreleri değişsin; aynı ortamda 2/5 kontrolü de bulunsun.
3. Yeni eğitimden önce veri/split/özellik/seed kimliklerinin eşitliğini kaydet.
   Mevcut modeller bu 38-fold deneyinin yerine kullanılamaz.
4. Validation'ı sessizce ikiye bölme. Epoch seçimi özgün BCE kuralıyla kalır.
   Eşik amaç ve kısıtları önce belirlenir. Aynı validation üzerinde seçilen
   eşik metriği iyimser seçim sonucu olarak etiketlenir; bağımsız performans
   sayılmaz. Daha güçlü iç ayrım istenirse ayrı açık protokol gerekir.
5. 720 saatlik fold bölümleri yürüyen düzende sonraki foldların train/validation
   kapsamına girebilir; topluca tamamen görülmemiş final holdout sayılmaz.
   Ekim tek-final testini ayrıca ve aynı bağlam kuralı açıkça belirtilerek ele al.
   Bu incelemede Ekim'e dokunulmadı ve yeni test dönemi seçilmedi.
6. Validation analizi ve kullanıcıyla yöntem kararı tamamlandıktan sonra
   yeni model/eşik kilidi ve en son bağımsız test.

Bu tur yalnızca paket ve yöntem incelemesidir; eğitim motoru veya notebook
değiştirilmedi. Eski sürüm hâlâ eski planı yürütür; bu nedenle yeniden eğitim
veya test için şu an kullanılması önerilmiyor.

## Kanıt ve yöntem kaynakları

Kaynak ZIP SHA256: `8468a33af3fbfdf724ffe94cbfd3b7d9690bb2430d7f5697afb32473ed37cab1`.
İç ZIP SHA256: `873dc529182fd86ab529f61ff6bc0ddd5a8234b49cac9674daa0691e27fca659`.
Yerel byte-koruyan kopya, salt-okunur inceleme scripti, audit.json, türetilmiş
tablolar ve grafik `reports/six-barrier-review-20261016/` içinde.
Özgün config: `configs/advisor_ablation.yaml`; yürütülmüş plan: paketin
`artifacts/plan.json` üyesi. Küçük kaynak kanıtları deney defterine hashli alınır.

- [scikit-learn: karar eşiği ve amaç metriği](https://scikit-learn.org/stable/modules/classification_threshold.html)
- [scikit-learn: precision–recall ve sınıf oranı referansı](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)
- [Lipton vd.: F1 maksimizasyonunda hep-pozitif davranışı](https://arxiv.org/abs/1402.1892)
