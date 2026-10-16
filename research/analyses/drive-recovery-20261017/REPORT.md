# Drive aktarım denetimi — 17 Ekim 2026

Hesap: icinbedava34@gmail.com. Çalışma: selective_a100_v11_001.
Drive connector üzerinden altı aday, 18 seed ve 684 fold klasörünün doğrudan
çocukları okundu. Listeleme hatası yok. [Tam envanter](../../sources/d35c27f02eb1a199809f5571227a63b041e787d7c2a0f65c2837caa3b7955e78.json) tüm gözlemleri saklar.
Bu bulut metadata denetimidir; dosyaların bilimsel doğruluğu veya checkpoint
okunabilirliği henüz kanıtlanmış değildir. Notebook ayrıca içerik denetimi yapar.

| Aday | Dört temel dosyası bulunan fold/seed | Eksik |
|---|---:|---:|
| B25 | 114 | 0 |
| B11 | 114 | 0 |
| B12 | 114 | 0 |
| B152 | 114 | 0 |
| B22 | 114 | 0 |
| B32 | 110 | 4 |

Temel dosyalar: last.pt, validation_predictions.parquet,
validation_metrics.json, history.csv. Toplam 680 tam; 681 rapora dosya olarak hazır.
B32 seed 44: fold 34 ağırlıksız; fold 35 geçmişsiz; fold 36 sadece checkpoint;
fold 37 boş. reports klasörü ve kullanıcının belirttiği ZIP listelenemedi.
Durum kayıtları tamamlandı dese de bazı özetler eski kalmıştı.

## Neden ve düzeltme

Önceki otomatik runtime.unassign öncesinde Drive flush yoktu. Bu, gözlenen
kısmi aktarım ile uyumludur; eski runtime logları olmadan kesin kök neden
kanıtlanamaz. Kullanıcı eski runtime'ın otomatik kapandığını doğruladı.

4. notebook varsayılan olarak kurtarma denetimi yapar; ALLOW_REPAIR=False.
Denetim sonrası kullanıcı ALLOW_REPAIR=True ile 6. hücreden devam eder.
Özgün research release v1.1.0, commit ve ortam kimliği korunur. Kurtarma
aracı ayrı hashli launcher olarak kullanılır; bilimsel motor değişmez.
Beklenmeyen başka eksik veya bozuk içerik varsa durur. Aynı workspace'e
başka runtime yazmamalıdır. Kullanıcı eski runtime'ın kapandığını doğrulamıştır.

- 34 yeniden eğitilmez; mevcut validation kanıtları korunur, eksik ağırlık raporlanır.
- 35 geçmişi uygun checkpointten yeniden çıkarılır; eğitim yok.
- 36 kayıtlı checkpointten sürdürülür; eski checkpoint ezilmez, son sürüm recovery altında kalır.
- 37 yeniden eğitilir; yeniden oluşturulan sonuç olduğu açıkça kaydedilir.
- Hiçbir mevcut fold dosyası ezilmez. Bozuk/yarım mevcut dosya varsa durur.
- Eski özetler kopyalanıp korunur; özetler doğrulanmış foldlardan yeniden yazılır.
- Tahmin/eşik raporu yalnızca tüm 684 foldun gerekli içerikleri doğrulanınca oluşur.
- Son aşama tüm workspace dosyalarının hashlerini alır, flush/unmount yapar,
  yeniden mount eder ve dosyaları karşılaştırır. Farkta runtime kapanmaz.
  Bu kontrol çok sayıdaki checkpoint nedeniyle zaman alabilir.

Bu değişiklik sırasında gerçek eğitim veya kurtarma çalıştırılmadı.
Yeni test, eşik seçimi veya model karşılaştırması yapılmadı.
