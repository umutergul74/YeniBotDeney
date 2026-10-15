# Altı bariyer · karşılaştırma kapsamının genişletilmesi

Kimlik: exp-015-six-barrier-training. Ebeveyn: exp-014-barrier-training.
Durum: planlandı; yeni model/test sonucu yok. Kullanıcı 15 Ekim 2026'da
2/2 ve 3/2 adaylarını da istedi ve Ekim testini henüz çalıştırmadığını doğruladı.

Bu plan [önceki dört adaylı planı](../barrier-training-20261015/PLAN.md) yeni
yürütmeler için genişletir. Eski plan, Git yayını ve varsa çalışma dosyaları
korunur. Önceki Colab eğitimlerinin çalıştırılıp çalıştırılmadığı teyit edilmedi;
eski sonuçların tamamlandığı veya hiç eğitim olmadığı iddia edilmez.

| Kod | Kar / zarar, ATR |
|---|---|
| B25 | 2 / 5 (kontrol) |
| B11 | 1 / 1 |
| B12 | 1 / 2 |
| B152 | 1.5 / 2 |
| B22 | 2 / 2 |
| B32 | 3 / 2 |

Her aday aynı altı temel özellik, GRU, BCE ve seed 42/43/44 ile çalışır:
toplam **18 eğitim**. 10 saat etiket ufku, aynı mumda çift temasta zarar önce,
timeout=0 kuralları ve tüm hiperparametreler önceki planla aynıdır.

## Bölümler ve seçim

- Eğitim: 18 Aralık 2025–15 Temmuz 2026; scaler yalnızca burada fit edilir.
- Epoch doğrulaması: 17 Temmuz–8 Ağustos 2026, en düşük validation BCE.
- Eşik doğrulaması: 10–30 Ağustos 2026; 201 eşik, üç seed ortalama F1,
  eşitlikte yüksek eşik. Aday başına bir ortak eşik.
- Test: 2 Ekim 00:00–14 Ekim 23:00 UTC, 312 saat. Eylül tekrar test edilmez.

Önceki planın 24 saat bölüm boşlukları ve dizi bağlamı aynen korunur. Altı
adayın bütün 18 eğitimi tamamlanmadan kalibrasyon/son kilit açılmaz. Aday
sıralaması kalibrasyon BCE skill, eşitlikte ID. Testten önce tüm modeller,
scalerlar ve eşikler kilitlenir; refit yok. Altı aday testte yan yana raporlanır;
testte eşik, model veya seed seçilmez. Etiketler farklı olduğundan ham F1/AP/BCE
tek başına mutlak üstünlük kanıtı değildir. 13 gün, örtüşen etiketler ve üç seed
uzun dönem bağımsız başarı kanıtı değildir. İşlem masrafları modellenmez.

## Yürütme ve korunacak kanıt

Notebook aynı `04_barrier_study.ipynb`; yeni yayın `advisor-barriers-v1.1.0`,
yeni varsayılan workspace `barriers_october_v11_001`. Eski v1.0.0 notebookuna
sadece B22/B32 yazmak çalışmaz; eski yayındaki CLI bu kodları kabul etmez.
Yeni sürümde aday listesi varsayılan olarak altısını içerir. Eğitim için altküme
seçilebilir; kalibrasyon ve final kilidi yine bütün kohortu gerektirir.

Ham veri, sabit SHA, izole T4 ortamı, kesintiden devam, değişmez dosyalar,
model/eşik kilidi, inceleme ZIP'i ve tam workspace yedeği kuralları önceki planla
aynıdır. Grafikler altı adayı gösterir; rapor tabloları altısını içerir.
Eski çalışma alanına yeni kaynak koduyla devam edilmez; yeni run kimliği gerekir.
Çalıştırma kanıtları gelince yeni defter event'iyle sonuçlar eklenir.
