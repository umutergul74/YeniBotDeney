# A6 / B37 / C37 / D37 — özellik kapsamı düzeltmesi

18 Ekim 2026. Kullanıcı dört yapıyı seçti. Durum: Colab çalıştırmasına hazırlanıyor;
yeni bilimsel eğitim veya validation sonucu henüz yok.

## Soru ve tasarım

A'nın üç volatilite kanalının B/C/D'de olmaması özellik genişletmesi yorumunu
bozuyordu. Bu kanalların eklenmesi A'nın mutlaka kaybedeceği veya diğerlerinin
iyileşeceği anlamına gelmez; eski sonuçlar yanlış metrik olarak silinmez.

| Yeni yapı | Girdiler | Mimari |
|---|---|---|
| A | Özgün6 | GRU |
| B | Özgün34 +3 volatilite =37 | GRU |
| C | Aynı37 | TCN |
| D | Aynı37 | Paralel TCN+GRU |

Eklenenler: `realized_vol_14`, `gk_vol_14`, `atr_14_pct`. Ham fiyat birimindeki
ATR doğrudan eklenmiyor; A'nın özgün normalize volatilite kanalları korunuyor.
A'nın altı girdisi37'nin birebir altkümesidir; B/C/D'de aynı sıra kullanılır.

- A–B: GRU sabitken özellik genişletmesi etkisi.
- B–C–D:37 girdi sabitken mimari karşılaştırması.
- A–C/D: iki unsur değişir; saf mimari sonucu çıkarılmaz.
- Parametre bütçeleri eşitlenmez. Özellik sayısı GRU giriş parametresini de
  değiştirir; sonuç sabitlenmiş bu uygulamalar içindir, evrensel mimari üstünlüğü değil.

## Sabit tutulanlar

33551 saat, 2022-03-01 04:00–2025-12-28 02:00 UTC; özgün38 fold,
train5040/validation1080/test-bölümü720, adım720, purge24/embargo24, seq64.
Seed42/43/44. **Yalnız 2/5 ATR, ufuk10**, BCE, wavelet kapalı.
Optimizer, mimari boyutları, batch, patience ve min-validation-BCE epoch seçimi
`configs/advisor_ablation.yaml` ile aynıdır. Fold test bölümü puanlanmaz.

Dört yapı A100 üzerinde aynı yeni ortamda yeniden çalıştırılır:456 fold/seed.
Eski A/T4 sonucu yeni A100 deneyine eşleşmiş kontrol olarak eklenmez. Altı
bariyer çalışması ayrı kalır; bu çalışmada bariyer araması yoktur.

## Veri ve doğrulama

Yerel hazırlanmış özgün tablolar SHA256 ile doğrulandı:

- A: `f6346a93ee4b97125d00e8d26223ba11a141806cdff675934e033a00940977a8`
- Full: `ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653`

Tablolarda timestamp, etiket, ileri getiri ve altı temel özellik birebir eşit.
37 özellik full tabloda zaten mevcut. Yeni özellik hesabı veya satır eleme yok.
Colab hazırlığı mevcut recovery yordamıyla ham/OI snapshot'ından aynı full
hash'i doğrular; eksik veya uyuşmayan veride durur. Eski `colab_v1` yazılmaz.
A/B/C/D yeni workspace'te aynı prepared dosyasını kullanır.

## Sonuçları nasıl değerlendireceğiz?

Ana ölçüt eşit fold/seed validation BCE ortalaması; AP, 0,50 precision/recall/F1,
sinyal oranı ve 201 eşik eğrisi birlikte raporlanır. Fold/seed dosyaları korunur.
Eşik kazananı otomatik seçilmez. Aynı validation epoch seçimi ve raporlamada
kullanıldığı için bağımsız başarı iddiası yapılmaz; seed/foldlar örtüşür.
A–B ve B–C–D sonuçları ayrı yorumlanır. Bilimsel üstünlük henüz bilinmiyor.
Düzeltmenin başarılı olması eşit girdili karşılaştırmanın yürütülmesidir;
B/C/D'nin A'yı geçmesi zorunlu değildir.

## Çalıştırma

[05_feature_comparison.ipynb](../../../notebooks/workflows/05_feature_comparison.ipynb)
A100 ile sırayla çalıştırılır. Yeni workspace:
`MyDrive/yeniBot/advisor_experiments/feature_comparison_v1/a100_001`.
Drive hesabı: `icinbedava34@gmail.com`. `ALLOW_TRAINING=True` dört yapıyı eğitir;
False hazırlık/rapor için kullanılabilir, train hücresi bu durumda durur.
Tek workspace'e aynı anda tek oturum yazmalıdır.

Kesinti sonrası aynı sürüm ve workspace ile devam edilir; tamamlanan foldlar
tekrar eğitilmez. Rapor tüm456 sonuç tamamlanmadan üretilmez. ZIP tahminleri ve
raporları içerir; ağırlıklar runs altında korunur. Son hücre Drive'ı yeniden
bağlayıp dosya hashlerini doğrular; ancak sonra `runtime.unassign()` çalışır.
Test komutu yoktur. Eski02/04 notebooklarının anlamı değiştirilmedi.
