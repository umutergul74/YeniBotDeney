# 2/5 seçiminin geçmişi ve bariyer belirleme yaklaşımları

22 Ekim 2026. Kaynaklar bu tarihte incelendi. Bu belge yeni bariyer seçimi değildir.

## Depodaki gerekçe

`git log --all -G 'tp_multiplier|sl_multiplier' -- config.yaml configs/advisor_ablation.yaml`
ve ilgili commit içerikleri incelendi. İlk pipeline commit'i
`68aed99b802b8ba3519e1c902206930c1eaa24d4`, `config.yaml` içinde zaten
TP=2, SL=5, ufuk=10 içeriyor. `d39638b` aynı değerleri advisor protokolüne
taşıyor. İncelenen commit mesajlarında ve proje belgelerinde **2/5'i özel
olarak gerekçelendiren literatür atfı veya karşılaştırmalı seçim kanıtı bulunmadı**.
Bu, geçmişte hiç gerekçe olmadığı iddiası değil; erişilebilir kayıtta yok.
Dolayısıyla 2/5'i literatürce önerilmiş veya optimum bulunmuş bir oran diye
sunamayız. Bu çalışma açısından tarihsel başlangıç koşuludur.

## Kaynaklar ne söylüyor?

1. **Volatiliteye göre ölçekleme:** Triple-barrier yaklaşımı iki fiyat
   sınırı ve bir zaman sınırı kullanır; fiyat sınırlarını gözlemin volatilitesine
   göre ayarlamak sabit yüzde eşiklerinin sorunlarını azaltmayı amaçlar.
   [MLFinLab, Triple-Barrier and Meta-Labelling](https://random-docs.readthedocs.io/en/latest/implementations/tb_meta_labeling.html).
   Bizde ATR kullanımı bu ölçekleme ailesine girer; ATR ile günlük getiri
   standart sapması aynı ölçü değildir, katsayıları birebir taşınamaz.

2. **Kâr ve zarar katsayıları ayrı parametrelerdir:** MizarLabs uygulaması
   `profit_taking_factor`, `stop_loss_factor` ve `num_expiration_bars` değerlerini
   ayrı alır. Dokümantasyon evrensel bir 2/5 değeri önermiyor.
   [MizarLabs, TripleBarrierMethodLabeling](https://mizarlabs.readthedocs.io/en/latest/mizarlabs.transformers.targets.html).
   Simetri (1/1, 2/2) anlaşılır kontrol koşuludur; tek başına optimalite gerekçesi değildir.

3. **Veriye bakıp en iyi çıkış kuralını aramanın seçim yanlılığı vardır:**
   Carr ve López de Prado, geçmiş simülasyonlardan çıkış parametresi seçmenin
   aşırı uyuma katkısını tartışır; belirli bir Ornstein–Uhlenbeck fiyat süreci
   altında model tabanlı optimal çıkış koşullarını inceler.
   [Determining Optimal Trading Rules without Backtesting (2014)](https://arxiv.org/abs/1408.1159).
   Bu çalışma BTC için hazır ATR oranı vermez; varsayımlarını doğrulamadan
   sonucunu bizim probleme doğrudan uygulamak doğru olmaz.

Bu kaynaklardan çıkarımımız: evrensel tek oran aramak yerine **ufuk, hedeflenen
hareket ve risk büyüklüğüyle gerekçelendirilen sınırlı adayları**, görülmemiş
testi kullanmadan karşılaştırmak gerekir. Bu bir projeye yönelik yöntem
önerisidir; kaynakların belirli üç adayımızı önerdiği anlamına gelmez.

## Bu proje için nasıl ilerlenebilir?

- Bu incelemede ufuk 10 saat ve adaylar 2/5, 1/1, 2/2 sabit. Etiket
  oranlarının yanında seçilen sinyallerin getirisi, sayısı, seed/dönem
  kararlılığı ve tüm saatleri alma referansına katkısı raporlanır.
- Daha ileride yeni oran gerekirse, yalnız eğitim döneminde ATR ile
  normalize edilmiş 10 saatlik yukarı/aşağı hareket dağılımları aday
  büyüklüklerini gerekçelendirmek için incelenebilir. Bu inceleme henüz yapılmadı.
- En yüksek tek nokta yerine komşu eşiklerde ve farklı dönemlerde tutarlı
  bölgeler araştırılır. Bu raporda eşik seçilmez; örnek sayısı için de sonuçlara
  göre yeni kabul kuralı uydurulmaz.
- Seçim yapılacaksa kural validation aşamasında dondurulur; bağımsız test
  seçimi değerlendirir. Mevcut validation epoch seçiminde kullanıldığı için
  burada bulunan yüksek getiriler bağımsız başarı kanıtı değildir.

## Neden precision tek başına yeterli değil?

Bizim etiket 1 = önce TP. Etiket 0 = SL **veya** süre dolumu.
Süre dolumu pozitif getirili de olabilir. Dolayısıyla precision, pozitif
getirili işlem oranıyla aynı şey değildir.

Sadece iki sonuç (+2 veya −5 ATR) ve aynı ATR cinsinden ödeme varsayımında,
masrafsız başabaş TP olasılığı `5 / (2 + 5) = %71,43` olur; simetrik
1/1 veya 2/2 için %50. **Bizde üçüncü sonuç timeout olduğu ve yüzde
getiriler ATR/fiyata göre değiştiği için bu sayılar doğrudan eşik değildir.**
Üstelik model skoru kalibre edilmiş TP olasılığı sayılmaz.

Gerçek hesap, seçilmiş örneklerde gözlenen TP, SL ve timeout getirilerinin
birlikte ortalamasıdır. Timeout'u otomatik zarar veya sıfır saymak bu hesabı bozar.
