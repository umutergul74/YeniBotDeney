# GRU kapasitesi: yalnız hidden128 → hidden64

31 Ekim2026 · exp034 · Kullanıcı onaylı hazırlık; henüz eğitilmedi.

Soru: Daha az GRU gizli birimi, aynı bilgi ve eğitim koşullarında sonraki
validation dönemine aktarımı ve seçici sinyal kararlılığını iyileştirir mi?
Exp033'teki aşırı uyumla uyumlu gözlemi sınar; kesin neden veya başarı iddiası yok.

Tek değişiklik model.gru_hidden128→64. GRU katman2, fusion_hidden128,
dropout0.2, altı özellik, seq64, LR0.001, AdamW/weight decay0.0001,
batch256, BCE loss, grad clip1, max100 epoch ve seçim BCE patience15 sabit.
Hidden boyutu değişince GRU/head bağlantısının doğal parametre boyutları da
değişir; ek yöntem uygulanmaz. Aynı seed+fold kullanılır, mimariler arasında
aynı başlangıç ağırlığı/minibatch sırası garanti edilmez.

Özgün veri hash'i ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653,
2/5 ATR ve10 bar korunur. Train5040/4977 hedef; validation528 seçim+24 boşluk+
528 değerlendirme, ayrı63 bağlamla465 hedef/bölüm.38 fold,seed42/43/44.
Scaler yalnız train fit; epoch ve cutoff seçim bölümünden; değerlendirmede
ayar seçilmez. Sabit0.5 ve seçim skorlarının üst%5/%10 cutoffları aynı.
Tarihsel validation görülmüştür, final test yok; dönem/seedler bağımlıdır.

Kontrol yeniden eğitilmez. cnn_gru_v1/a6_a100_001 içindeki114 GRU128 sonucu
salt okunur kullanılır. Beklenen kaynak commit dafcb21aa65883c7dc5c53d77a934e0cce565f55;
tasarım, protokol, GPU/ortam, ortak eğitim kodu,114 completion imzası ve
ağırlıklar dahil kayıtlı hashler doğrulanır. Tarih/etiket/frame konumları
eğitim öncesinde aynı dondurulmuş veriden karşılaştırılır. Kaynak değişirse
durur; otomatik düzeltme/yeniden eğitim yapılmaz.

Yeni çıktı gru_capacity_v1/hidden64_a100_001; yalnız114 yeni eğitim.
Yeni çalışma kimliği ve kontrol kanıt envanteri saklanır. Kesilen aday
optimizer/RNG/last.pt ile sürer. Kaynak ağırlıklar eski workspace'te kalır;
capacity_review.zip eski kontrolün ağırlık dışı kanıtlarını da içerir.

Rapor: iki adayın aynı465 assessment hedefinde AP/BCE eşit run ortalamaları;
precision/recall/F1 toplam sayılardan, sinyal sayısı/oranı,sinyalsiz run,
eşleşmiş fold/seed ve tek dönem grafiği. Aynı eşik kuralı aynı gerçekleşen
kapsam demek değildir. Karar yalnız ortalamaya değil dönem/seed tutarlılığına
ve sinyal kapsamına dayanır; otomatik kazanan/sonradan eşik araması yok.

Mevcut06 notebooku advisor-gru-capacity-v1.0.0 yayınına bağlanır. Yeni A100
oturumu ve icinbedava34@gmail.com; hücreler sırayla. Kurulum Agg kullanır;
rapor sonrası Drive yeniden bağlanır ve hash kontrolü geçerse runtime kapanır.
