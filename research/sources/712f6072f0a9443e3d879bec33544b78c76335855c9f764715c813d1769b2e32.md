# Dört bariyer için model ve eşik deneyi

Durum: planlandı; Colab notebooku hazırlanıyor. Yeni model eğitimi veya test yapılmadı.
Kimlik: exp-014-barrier-training. Ebeveyn: exp-013-barrier-expansion.
Kullanıcı 15 Ekim 2026'da eğitimi ve uygun yeni test dönemi seçimini yetkilendirdi.

## Dönem kararı

Eylül 2026 eski final testidir. Sonucu yeni araştırmayı yönlendirdiğinden yeni
adaylar için bağımsız final test olarak tekrar kullanılmaz. Ağustos eski epoch
seçiminde kullanılmıştır; geliştirme verisi olarak açıkça yeniden kullanılır.
Yeni test: **2 Ekim 00:00–14 Ekim 23:00 UTC**, 312 tahmin saati. Kullanıcı
Ekim'in daha önce analiz edilmediğini bildirdi. Bu beyan tüm geçmiş etkinliklerin
bağımsız denetimi değildir. Ekim 1'in ilk 10 saati eski Eylül etiketlerinin
kuyruğunda bulunduğundan 1 Ekim dışarıda bırakılır. Test etiketi için son gereken
mum 15 Ekim 09:00 UTC; kapanışından önce test engellenir.

## Sabit karşılaştırma

| Rol | UTC tarihleri | Ham bölüm satırı | 64 saat dizi sonrası tahmin |
|---|---|---:|---:|
| Eğitim | 18 Aralık 2025–15 Temmuz 2026 | 5040 | 4977 |
| Epoch doğrulaması | 17 Temmuz–8 Ağustos 2026 | 552 | 489 |
| Eşik doğrulaması (kalibrasyon) | 10–30 Ağustos 2026 | 504 | 441 |
| Test | 2–14 Ekim 2026 | 312 + 63 bağlam | 312 |

İlk üç bölüm arasında 24 boş saat; etiket ufku 10 saat. Test bağlamı yalnızca
geçmiş özellikler içindir. Eylül tahmin/karşılaştırma verisi değildir; Ekim
özellikleri için geçmiş mumların okunması testte yeniden seçim anlamına gelmez.

Adaylar: B25=2/5 kontrol, B11=1/1, B12=1/2, B152=1.5/2 ATR. TP önce=1,
SL/timeout=0; aynı mumda iki temas varsa SL önce. Aynı saatler, aynı altı temel
özellik, aynı GRU ve BCE; wavelet kapalı; seed 42/43/44. Mimarinin ve eğitim
ayarlarının kaynağı mevcut advisor_ablation.yaml. Scaler yalnızca eğitimde fit.
Toplam 12 eğitim, üst sınır 100 epoch, patience 15. Bu yeni tek ayrımlı
çalışmadır; eski 38-fold metrikleriyle aynı kapsam gibi birleştirilmez.

## Seçim ve kilit

1. Her seed için en düşük epoch-doğrulama BCE checkpoint'i tutulur.
2. Ayrı kalibrasyon bölümünde 201 eşik (0–1, adım .005) denenir. Aday başına
   üç seed'in eşit ağırlıklı ortalama F1'ini en yüksek yapan ortak eşik seçilir.
   Eşitlikte yüksek eşik; testte seed veya eşik seçilmez.
3. Geçici aday sıralaması: kalibrasyonda ortalama BCE skill =
   1 − BCE / sabit eğitim pozitif oranı referansının BCE'si. Eşitlik aday ID'siyle
   çözülür. Precision, recall, AP, F1, pozitif karar oranı ve hep-pozitif F1
   birlikte raporlanır. Farklı etiket hedefleri nedeniyle skill sırası da mutlak
   ekonomik üstünlük kanıtı değildir; kalibrasyonda seçilen değerler iyimserdir.
4. Tüm modeller, scalerlar, veri, kod/ortam kimliği ve eşikler hash ile kilitlenir.
   Train+validation refit yapılmaz. Kilitten sonra test indirme ve puanlama açılır.
5. Dört adayın test sonuçları aynı tabloda raporlanır; test kazananı seçilmez.
   Sonraki değişiklikler yeni deney ve yeni bağımsız test gerektirir.

## Kanıt ve yürütme

Colab T4, izole kilitli Python ortamı; yeni `barrier_research_v1/WORKSPACE_ID`.
Girdi eski `colab_v1/final_test_v1/inputs/fit_raw/btc_1h.parquet`:
SHA256 `f3a29be9f7a935ca144fe70a701b41072f30a1b2432b177faa309a8c37b404c6`.
Yerel arşivde Ekim'in yalnızca ilk 10 saati var; canlı Drive içeriği doğrulanmadı.
Eksik test saatleri yeni workspace'e kilitten sonra indirilir; eski veriler ezilmez.

Notebook: `notebooks/workflows/04_barrier_study.ipynb`. Ayrı bilimsel akış olduğu
için tek giriş; her aday için yeni notebook oluşturulmaz. Eski 02, önceki
A–D/wavelet/loss protokolüne ait kalır.

Çıktılar: seed bazlı epoch geçmişi/checkpoint/tahmin/metrik; kalibrasyon eşik
eğrileri; kalibrasyon ve test CSV/PNG/Markdown tabloları; model/eşik kilidi;
dosya envanteri ve küçük inceleme ZIP'i. Modeller için tüm workspace yedeklenir.
Başarısız/kesilen işlemlerin session kayıtları ve checkpointleri korunur.
Gerçek Colab yürütme kanıtı gelince bu planın kaydına yeni event eklenir;
hazırlanmış notebook, tamamlanmış model deneyi olarak kaydedilmez.

## Sınırlar

13 gün tek piyasa dönemi ve örtüşen 10 saatlik etiketler: 312 bağımsız örnek
iddiası yoktur. Üç seed bağımsız piyasa dönemi değildir. Masraf, funding,
slippage ve portföy simülasyonu yoktur. Eski veriyi içeren geliştirme seçimi
tamamen görülmemiş değildir. Daha uzun dönem dayanıklılığı ayrı deneydir.

Yöntem dayanağı: [scikit-learn test verisinin seçimden ayrılması](https://scikit-learn.org/stable/common_pitfalls.html)
ve [eşik seçimi](https://scikit-learn.org/stable/modules/classification_threshold.html).
