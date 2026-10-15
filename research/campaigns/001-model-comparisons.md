# Kampanya 001 — tarihsel model karşılaştırmaları

Durum: tamamlanmış geçmişin kayıt aktarımı. Kaynak raporlar 3–4 Ekim 2026;
deftere aktarım 15 Ekim 2026. Deneyler bu aktarım sırasında çalıştırılmadı.

Öneri: temel fiyat/hacim → GRU/BCE; tüm girdiler → GRU/BCE, TCN/BCE,
TCN–GRU/BCE; validation kazananında wavelet açık/kapalı; ardından losslar.
Model ve epoch validation BCE ile; son sabit yöntem testte raporlanır.

Zincir: A → B/C/D → wavelet → dört alternatif loss → final raporu.
W_OFF ve L_BCE, A kontrolünün yeniden kullanım isimleridir; ayrıca yeniden
eğitilmiş bağımsız deneyler olarak sayılmazlar.

Karar: altı özellik + GRU + wavelet kapalı + saf BCE. Finalde BCE/AP
referanstan iyi, recall/F1 düşük ve seed duyarlı. Bu durum yeni mimari
aramasından önce teşhis sorularına yol açtı: [Kampanya 002](002-diagnostics.md).

Tarihsel kaynaklarda geçen “sonraki adım” ifadeleri yazıldıkları tarihe aittir;
bugünkü çalıştırma talimatları değildir. Sayısal ve kanıt bağlantılı kayıtlar
[deney defterinde](../INDEX.md).
