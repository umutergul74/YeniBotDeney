# Kampanya 002 — düşük recall/F1 teşhisi

**Ek çalışma:** Kullanıcının isteğiyle exp-013 kaydında 7 yeni bariyer eklendi.
[10 senaryolu karşılaştırma](../analyses/barrier-expansion-20261015/REPORT.md).
1/1, 1/2 ve 1.5/2 sonraki validation için aday; yeni eğitim veya kesin seçim yok.

**Durum: 15 Ekim 2026 kullanıcı isteğiyle iki analiz tamamlandı.**
[Grafikler, tablolar ve sonuç raporu](../analyses/diagnostics-20261015/REPORT.md).
Aşağıdaki metin özgün öneri/plan bağlamıdır; güncel yürütme ve kararlar deney
defterindeki eklemeli revizyonlardadır. Yeni eşik veya bariyer seçilmedi.

Kullanıcının ilettiği ikinci araştırma
önerisidir. Yeni özellik veya mimari denemeden önce nedenleri anlamayı hedefler.

## exp-011-threshold-diagnostics

Sabit mevcut modelin validation tahminlerinde farklı eşikler için precision,
recall ve F1 tabloları/eğrileri. Test sonucuna göre eşik seçilmez.

Çalıştırmadan önce kesinleşecekler: kullanılacak validation tahmin manifesti
ve hashleri, fold/seed eşleştirmesi, eşik ızgarası, toplulaştırma, varsa eşik
seçim amacı ve eşitlik çözümü. Şimdilik hiçbir eşik önerilmedi/seçilmedi.
Çıktı sözleşmesi: threshold_metrics.csv, threshold_curves.png, analysis_plan,
girdi envanteri ve yorum. Eğitim gerekmez; analiz daha sonra açık istekle yapılır.

## exp-012-barrier-diagnostics

Aynı ham geliştirme snapshot'ında 10 saat ufukla TP/SL ATR çarpanları:
2/5 (mevcut), 2/2, 3/2. Her kombinasyonda kâr ilk, zarar ilk ve süre dolumu
sayı/yüzdeleri; süre dolan örneklerin gerçekleşen getiri dağılımı.

Çalıştırmadan önce kesinleşecekler: veri aralığı/hash, ATR tanımı ve nedenselliği,
aynı bar içinde iki bariyere temas kuralı, eksik/son ufku tamamlanmayan satırlar,
yüzde paydası, getiri tanımı ve masrafların dahil olup olmadığı. Aynı uygun
timestamp evreniyle karşılaştırılmalı; dışlanan örnekler ayrıca raporlanmalı.
Etiketler yeni ayrı sürümlere yazılmalı; mevcut 2/5 tablo/manifesti ezilmemeli.
Çıktı sözleşmesi: barrier_counts.csv, timeout_returns_summary.csv,
timeout_returns_distribution.png, label manifests ve yorum.

Bu betimsel analiz bir model başarım karşılaştırması değildir. Yeni bariyer
kazananı veya yeni nihai test dönemi burada seçilmedi. Eylül 2026 kapsam dışı.
İki teşhis aynı sorudan doğar; aralarında zorunlu hesaplama bağımlılığı yoktur.
