# Seçici sinyal · özgün kohortta altı bariyer

exp-016-selective-walk-forward; ebeveyn exp-015-six-barrier-training.
16 Ekim 2026. Kullanıcı seçici sinyal modelini önceliklendirdi; işlem masrafları
ve strateji sonraki aşamadır. Bu plan, veri dönemini değiştiren tek ayrımlı
çalışmanın yerine geçer; eski sonuçlar ve yayınlar korunur.

## Değişmeyecek karşılaştırma sözleşmesi

- 1 Mart 2022 04:00–28 Aralık 2025 02:00 UTC: 33.551 ortak saat.
- Özgün sabit market_snapshot_v1; 1h SHA
  `a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c`,
  4h SHA `ba379bf5995c19096c1f8f37e4b8a75b9fc29377cf595d1346efae38ce5f9bdb`.
- 38 fold; train5040 / validation1080 / test-bölümü720; adım720;
  purge24 / embargo24. Seq64 → train4977 / validation1017 / test-bölümü657.
- Validation bölünmez. Epoch seçimi özgün validation BCE. Fold test bölümleri
  bu geliştirme yürütücüsünde puanlanmaz; Eylül/Ekim final testi de yapılmaz.
- Aynı altı temel özellik, GRU, BCE, wavelet kapalı, seed42/43/44 ve özgün
  hiperparametreler. Scaler yalnızca her fold'un train verisinde fit.
- B25=2/5, B11=1/1, B12=1/2, B152=1.5/2, B22=2/2, B32=3/2 ATR.
  Adaylar arasında yalnızca etiket bariyerleri değişir. Tüm adayların timestamp
  ve aktif özellikleri aynı hash'e sahip olmalıdır. Kaynak feature config eski
  A manifestiyle karşılaştırılır; fark varsa durur.
- Her aday 114 eğitim, toplam 684 fold/seed eğitimi. Eski 18 model bu kohortun
  yerine kullanılamaz. Bir aday tamamlanınca raporu incelenebilir; ayrı aday
  oturumları aynı yeni workspace ve kod sürümüyle ardışık yürütülür.

## Hedefin anlamı

Soru: 'Önümüzdeki 10 bar içinde TP'ye SL'den önce ulaşılacak mı?'
TP önce=1; SL önce, aynı mumda çift temas ve timeout=0. Bu 'tam 10. barın
sonunda fiyat yukarıda mı?' veya timeout dışlanmış TP-vs-SL problemi değildir.
Negatif sinyal SL garantisi değildir. Yeni üç sınıflı hedef ayrı deney gerekir;
bu çalışma hedef tanımını sessizce değiştirmez.

## Eşik ve başarı değerlendirmesi

F1 maksimizasyonu ve otomatik BCE-skill kazanan seçimi kaldırılır. Bu sürüm
hiçbir deployment eşiği, model kazananı veya test kilidi üretmez.

Kullanıcıya precision hedefi soruldu. Yanıtla kilitlenene kadar %60/%65/%70
yalnızca betimsel karşılaştırma senaryolarıdır; başarı garantisi veya kabul
edilmiş performans şartı değildir. Her 0–1/.005 eşikte:

- Fold/seed bazında precision, recall, F1 (raporlama için), TP/FP/FN,
  pozitif karar sayısı/oranı; seçilen SL, timeout ve çift temas sayıları.
- Fold/seed eşit ağırlıklı ortalamaları; precision alt yüzde10 ve minimum;
  minimum/medyan sinyal sayısı; hiç sinyal vermeyen fold/seed oranı.
- Her precision hedefini sağlayan fold/seed oranı (sinyalsızlar başarılı sayılmaz).
  Genel senaryo tablosu ortalama precision hedefini ve tüm fold/seedlerde en
  az bir sinyal olmasını gösterir; bu yeterli örnek/güven koşulu değildir.
  Birkaç örnekten doğan yüksek precision başarı olarak ilan edilmez.
- Seed bazında ayrı tablolar, validation başlangıç/bitiş tarihleri; sabit
  0,5 eşik karşılaştırması; AP, pozitif oranı, train-prior BCE referansı ve skill.

Sinyal yoksa precision tanımsızdır (NaN), 1 yapılmaz. Sinyal veren dönemlerin
precision ortalaması bütün dönemlerin başarısı gibi sunulmaz. Eşik artırmanın
precision'ı monoton yükseltmesi beklenmez. Hiçbir hedef sağlanmaması geçerli bir
sonuçtur; otomatik olarak en az kötü aday seçilmez.

Epoch seçimiyle eşik incelemesi aynı validation üzerinde olduğu için sonuçlar
iyimser geliştirme sonuçlarıdır. Kullanıcının sabit bölümleri değiştirilmez;
ayrı iç doğrulama istenirse yeni protokol gerekir. Örtüşen fold/seed tahminleri
bağımsız örnek değildir; tablo toplamı bağımsız saat sayısı diye raporlanmaz.
Farklı bariyer hedeflerinin ham AP/BCE/F1'i mutlak üstünlük sıralaması değildir.

## İş akışı ve kayıt

Aynı 04 notebook girişinin yeni sürümü: `advisor-selective-v1.0.0`.
Workspace: `selective_walkforward_v1_001`, Drive `selective_research_v1/`.
Komutlar: prepare → train → report → bundle. Test/freeze komutu yok.
Özgün advisor eğitim/özellik/etiket motoru değiştirilmez; yeni host adapter
`yenibot/experiment/advisor_selective.py` içindedir. İzole T4 ortamı korunur.

Önceki ZIP'teki kanıt eksikliğini gidermek için yeni inceleme paketi satır bazlı
validation tahminlerini, her fold/seed'in history/metrics dosyalarını, kaynak/ortam
kimliğini, raporları ve envanteri içerir. Ham veri ve model ağırlıkları ZIP'e
konmaz; tüm workspace ayrıca yedeklenir. Tamamlanmamış çalışmalar raporda tam
başarı gibi görünmez; tamamlanmış aday kapsamı açıkça belirtilir.

Bu plan kayıt tarihinde gerçek Colab eğitimi çalıştırılmadı. Testler sentetik
veriyle protokol/rapor kontrolleridir; gerçek model başarısı değildir. Bilimsel
split/label sözleşmesi değiştiğinden tam CI grubu bir kez çalıştırılır.
