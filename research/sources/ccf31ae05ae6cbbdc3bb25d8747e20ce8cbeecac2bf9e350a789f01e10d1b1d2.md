# A6: BCE ve AP checkpoint seçimi

29 Ekim 2026 · exp-031 · Kullanıcı onaylı yeni deney, Colab çalışması bekleniyor.

Soru: Aynı eğitim akışında seçim bölümünde minimum BCE veya maksimum AP ile
seçilen ağırlıklar, sonraki değerlendirme bölümünde seçicilik ve dönem
kararlılığı açısından farklı mı? Bu, AP erken durdurma deneyi değildir.

## Sabit koşullar

A6 GRU, özgün altı özellik; LR0.001, AdamW/weight decay0.0001,
batch256, seq64, dropout0.2, iki GRU katmanı/hidden128, BCE loss,
gradient clip1, en çok100 epoch. Veri/özellik üretimi değişmez:
shared37.parquet SHA256 ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653.
2/5 ATR,10 bar; seed42/43/44,38 fold, train5040 satır/4977 hedef.
Scaler yalnız train'de fit edilir. A100 ve eski çalışmayla aynı Python,
Torch/CUDA/cuDNN ve bilimsel paket sürümleri gerekir.

## Bilerek değişen bölüm

Özgün1080 validation satırı, zaman sırasıyla:

| Bölüm | Satır | Tahmin hedefi | Kullanım |
|---|---:|---:|---|
| Seçim | 528 | 465 | BCE/AP checkpoint ve skor eşiği |
| Boşluk | 24 | 0 | 10 bar etiket ufkunu ayırmak |
| Değerlendirme | 528 | 465 | İki seçilmiş checkpointi karşılaştırmak |

İki bölüm kendi ilk63 bağlam satırını kullanır; aralarındaki bağlam da
örtüşmez. Özgün train-validation boşluğu24 ve dış fold takvimi korunur.
Eski1017 validation hedefiyle sayısal sonuçlar doğrudan aynı-kohort
iyileştirme diye kıyaslanamaz. Kontrol de yeni bölümde yeniden eğitilir.

Her fold/seed için **bir ortak eğitim**, seçim BCE'sinde patience15.
Strict iyileşmede kayıt; eşitlikte önceki epoch korunur. AP'ye göre ayrı
durdurma veya eğitim yok. Bu bütçe içinde en iyi BCE ve AP ağırlığı ayrı
saklanır. İki epoch aynıysa bu geçerli bir sonuçtur, zorla ayrılmaz.
Toplam114 eğitim akışı,228 checkpoint; eski sonuçların üstüne yazılmaz.

İki seçimin epochları dondurulmadan değerlendirme DataLoader'ı oluşturulmaz.
Değerlendirme metrikleri eğitime/erken durdurmaya geri beslenmez. Final test
komutu yok. Validation tarihleri daha önce görüldü; bu çalışma tarihsel
veride kontrollü karşılaştırma, küresel anlamda görülmemiş final test değildir.
Foldlar örtüşür; sonraki fold train'i önceki dönemleri içerebilir.

## Eşik ve raporlama kuralları

- Sabit0.5 referansı.
- Her seçilmiş checkpointin **seçim** skorlarında en üst %5 ve %10 örneğe
  karşılık gelen cutoff: sıralı skorlarda ceil(n×oran) sayısı; cutoff'a eşit
  skorların hepsi sinyal. Etiketle eşik optimize edilmez.
- Bu eşikler değiştirilmeden değerlendirmeye uygulanır. Değerlendirmedeki
  gerçekleşen sinyal oranları farklı olabilir; eşitmiş gibi sunulmaz.
- Precision,recall,F1,sinyal sayısı/oranı,sinyalsiz run,BCE,AP;
  eşleşmiş fold/seed tabloları ve top-%5 seçim eşiğinin dönem grafiği.
- Precision/recall/F1 toplam TP/FP/FN üzerinden, BCE/AP eşit run ortalaması.
  Sinyal yoksa precision boş; bağımsız işlem sayısı veya otomatik kazanan yok.
- Değerlendirme sonuçlarıyla yeni eşik aranmaz. İyileşme için tek ortalama
  yerine seed/dönem tutarlılığı ve gerçekleşen kapsam birlikte incelenir.

## Kullanım ve koruma

Mevcut `notebooks/workflows/06_learning_rate.ipynb` yeniden kullanılır;
başlığı artık checkpoint seçimi. Eski LR notebooku sabit
advisor-learning-rate-v1.1.0 etiketinde korunur.
Yeni yayın: advisor-checkpoint-selection-v1.0.0.
Kaynak Drive: feature_comparison_v1/a100_001.
Yeni çıktı: checkpoint_selection_v1/a6_bce_ap_a100_001.

Yeni Colab A100 oturumunda1–12 hücreyi sırayla çalıştırın. Prepare sadece
kaynak ve sınırları doğrular; train hücresi114 eğitimi başlatır. Kesilirse
aynı sürüm/workspace ile devam eder. Aynı workspace'e eşzamanlı iki oturum yazmasın.
last.pt optimizer/RNG ve her iki en iyi ağırlığı saklar. Model/seed/fold,
veri, kaynak ve ortam kimliği uyuşmazsa durur. Tamamlanmış dosyaların hash'i
uyuşmazsa otomatik yeniden eğitim/üzerine yazma yapılmaz.

Seçim/değerlendirme tahminleri, iki seçilmiş checkpoint ve history ayrı
saklanır. Bütün epoch ağırlıkları saklanmaz. Review ZIP tahminleri içerir,
ağırlıkları içermez. Rapor tamamlandıktan sonra Drive yeniden bağlanır,
dosya hash'leri doğrulanır; ancak bundan sonra runtime.unassign() çağrılır.

Deney henüz çalıştırılmadı; başarı veya sonuç iddiası yok.
