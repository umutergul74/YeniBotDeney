# Bariyerlerin ekonomik incelemesi — önceden belirlenen kapsam

22 Ekim 2026. B25 (2/5), B11 (1/1), B22 (2/2); mevcut A6 GRU,
38 fold ve seed 42/43/44. Yeni eğitim, final test, eşik veya kazanan seçimi yok.

- Kaynak: 17 Ekim review ZIP; SHA256
  `76d09912ab27349d003041a4f2356fbe989cbd76601feaa4793d8e342ca16eff`.
- Model tahminleri yalnız validation. Etiket/getiri kaynağı daha önce aynı
  33.551 saat üzerinde doğrulanmış bariyer tabloları; mevcut manifest ile kontrol.
- Brüt bariyer çıkış getirisi: sinyal mumunun kapanışından giriş; ilk TP/SL
  temasında tam bariyer fiyatından çıkış; aynı mumda çift temasta SL önce;
  temas yoksa 10. saat kapanışında çıkış. Komisyon, slippage, funding yok.
- Ayrı ölçü: bariyere bakmadan 10. saat kapanış getirisi. İkisi karıştırılmaz.
- Eşikler 0–1, adım 0,01; tabloda 0/0,30/0,40/0,50/0,60/0,70.
  Ham skor eşikleri kalibre edilmiş olasılık değildir.
- Her fold/seed için sinyal sayısı, ortalama/medyan getiri, pozitif getiri
  oranı, TP/SL/timeout oranları ve tüm örnekleri alma referansına fark hesaplanır.
- Fold örtüşmesini ana görünümde gider: her seed ve timestamp için en yüksek
  fold numaralı validation tahminini kullan (sonuca/skora göre seçim yok).
  Seedler ayrı tutulur; ana tabloda üç seed ortalaması ve aralığı gösterilir.
  Ayrıca orijinal 114 fold/seed grubu ayrı CSV ile korunur.
- Sıfır sinyalde getiri ve kazanma oranı tanımsız/NaN; sıfır başarı sayılmaz.
- Bunlar örtüşen saatlik varsayımsal sinyallerdir; portföy backtesti, birikimli
  getiri veya bağımsız işlem sayısı değildir. Pozisyon çakışması modellenmez.
- Validation epoch seçiminde kullanılmıştır; bu keşif analizi bağımsız başarı
  kanıtı değildir. Dönem ve seed değişkenliği ayrıca raporlanır.
- Kontroller: kaynak hashleri, 342 tahmin dosyası, aynı zaman/etiket/getiri
  eşleşmeleri, beklenen 1017 satır, altı girdi ve ortak model protokolü,
  0,50 sinyal sayısı/TP parity, bariyer getirisinin formülle kontrolü,
  küçük yapay örneklerde metrik ve sıfır-sinyal kontrolü. Motor/veri/etiket
  değiştirilmediği için bütün eğitim test paketi tekrar çalıştırılmaz.
