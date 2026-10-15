# Genişletilmiş bariyer karşılaştırması — sonuç öncesi plan

Kullanıcı ek senaryoları denemeyi istedi. exp-013-barrier-expansion,
exp-012-barrier-diagnostics kaydının devamıdır; yeni eğitim veya final testi yok.

Kontroller: 2/5, 2/2, 3/2. Ek adaylar: **1/1, 1/2, 1.5/1.5, 1.5/2,
2/1, 2/3, 3/3**. Toplam 10 senaryo; sonuçlara göre liste genişletilmeyecek.
Dar/simetrik/asimetrik bariyerleri kapsayan küçük, önceden belirlenmiş tarama.

Önceki çalışmayla aynı ham 1h snapshot, hazırlanmış 33.551 timestamp ve
10 saat ufuk. ATR14 basit hareketli true range; giriş kapanış fiyatı.
Aynı mumda çift temas ihtiyatlı zarar-önce. Eksik ufuk veya hash uyuşmazlığında
durulur. Eski üç senaryonun sayıları birebir eşleşmeli. Girdi ve çıktı hashleri
kaydedilir; eski veri/etiket tablosu üzerine yazılmaz. Eylül 2026 okunmaz.

Rapor: üç olayın sayı/yüzdeleri; pozitif etiket oranı; belirsiz çift temas;
yıllara göre aynı ölçütler; timeout ve her etiketin sabit 10 saatlik brüt
getiri özeti. Masraf/funding/slippage yok; etiket getirileri modelin seçtiği
işlemlerin getirisi değildir. Etiketler gelecekteki fiyatlardan türediği için
koşullu getiri ayrışması öğrenilebilirlik veya bağımsız alpha kanıtı değildir.

Kullanıcıya tercih soruldu. Yanıt gelmezse dengeli değerlendirme varsayımı:
50/50'ye uzaklık, timeout yüzdesi ve çift-temas yüzdesi üç ayrı hedef olarak
raporlanır. Bir aday üçünde de daha kötü değil ve en az birinde kesin daha
iyiyse diğerini domine eder (Pareto). Ağırlıklı keyfi toplam skor yok.
Pareto adaylığı yalnızca etiket teşhisi içindir; sınıf dengesinin 50/50 olması
bir zorunluluk değildir ve model/strateji açısından üstünlük göstermez.
TP/SL oranı ve yıllık tutarlılık ayrıca yorumlanır. Kesin en iyi model hedefi
ilan edilmez; sonraki validation çalışması için gerekçeli kısa liste verilir.

Sentetik Pareto ve ilk temas monotonluğu kontrolleri; yeni bilimsel analiz
kodu nedeniyle tam CPU CI bir kez. Gerçek eğitim yok. Daha önce geçen
değişmemiş analiz tekrar çalıştırılmaz; eski üç bariyer yalnızca parite kontrolüdür.
