# 1/2 bariyerini ekonomik validation incelemesine ekleme

23 Ekim 2026. Önceki exp-022 çalışmasının kapsam genişletmesi.
B25, B11, B22 yanına B12 (TP 1 ATR / SL 2 ATR) eklenir.
Modelin skoru >= eşik olan örneklerin getirisi hesaplanır; yalnız doğru
pozitifler seçilmez. TP, SL ve timeout sonuçlarının tümü hesaba katılır.

22 Ekim analizinin veri, eşik, çıkış ve toplulaştırma kuralları aynen korunur.
Yeni eğitim, etiketleme veya final test yoktur. Eşik/kazanan seçilmez.
Yeni dated klasör eski raporu korur. Kontrol kapsamı: B12'nin 114 validation
dosyasının hash/zaman/etiket/getiri/protokol eşleşmeleri, 0.50 sinyal sayısı,
küçük metrik kontrolleri; eski üç adayın tablolarının birebir korunması.
Motor veya notebook değişmez; tüm regresyon paketi tekrar çalıştırılmaz.

Önceki plan: ../barrier-economics-20261022/PLAN.md
