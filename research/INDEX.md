# Deney defteri

Bu görünüm kayıtlı sonuçları listeler; analiz veya eğitim çalıştırmaz.
Kaynak: `events/` içindeki eklemeli kayıtlar. Rakamlar kaynak raporların yuvarlatılmış değerleridir.
Validation ve test ayrı kapsamdır; bu tablo otomatik bir başarı sıralaması değildir.

**18 deney/plan · 32 geçmiş kaydı**

| Kimlik | Soru / yöntem | Durum | Sonuç yorumu |
|---|---|---|---|
| [exp-001-a](#exp-001-a) | A · 6 temel özellik → GRU → BCE | completed | selected |
| [exp-002-b](#exp-002-b) | B · 34 mevcut girdi → GRU → BCE | completed | not_selected |
| [exp-003-c](#exp-003-c) | C · 34 mevcut girdi → TCN → BCE | completed | not_selected |
| [exp-004-d](#exp-004-d) | D · 34 mevcut girdi → TCN–GRU → BCE | completed | not_selected |
| [exp-005-wavelet](#exp-005-wavelet) | Seçilen A üzerinde nedensel wavelet | completed | not_selected |
| [exp-006-weighted-bce](#exp-006-weighted-bce) | A üzerinde ağırlıklı BCE | completed | not_selected |
| [exp-007-focal](#exp-007-focal) | A üzerinde focal loss | completed | not_selected |
| [exp-008-bce-pearson](#exp-008-bce-pearson) | A üzerinde BCE + Pearson | completed | not_selected |
| [exp-009-focal-pearson](#exp-009-focal-pearson) | A üzerinde focal + Pearson | completed | not_selected |
| [exp-010-final](#exp-010-final) | Donmuş A/W_OFF/BCE · Eylül 2026 final raporu | completed | mixed |
| [exp-011-threshold-diagnostics](#exp-011-threshold-diagnostics) | Plan · Validation eşik–performans teşhisi | completed | mixed |
| [exp-012-barrier-diagnostics](#exp-012-barrier-diagnostics) | Plan · ATR bariyerleri ve etiket dağılımı | completed | mixed |
| [exp-013-barrier-expansion](#exp-013-barrier-expansion) | Genişletilmiş 10 bariyer senaryosu · denge ve hedef teşhisi | completed | mixed |
| [exp-014-barrier-training](#exp-014-barrier-training) | Dört ATR bariyeri: GRU/BCE, ayrı epoch/eşik doğrulaması ve Ekim testi | abandoned | inconclusive |
| [exp-015-six-barrier-training](#exp-015-six-barrier-training) | Altı ATR bariyeri: B25/B11/B12/B152/B22/B32 · GRU/BCE | abandoned | mixed |
| [exp-016-selective-walk-forward](#exp-016-selective-walk-forward) | Özgün 38-fold kohortta altı bariyer · seçici sinyal incelemesi | completed | mixed |
| [exp-017-threshold-transfer](#exp-017-threshold-transfer) | Altı bariyer: validation eşik bölgeleri ve son model penceresine aktarım | completed | mixed |
| [exp-018-validation-stability](#exp-018-validation-stability) | Puan dağılımı, sıralama gücü ve dönem/seed kararlılığı teşhisi | completed | mixed |

## Kayıtlı sonuçlar · validation

legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-001-a | 0.594507 | 0.420872 | 0.410499 | 0.096839 | 0.142418 |
| exp-002-b | 0.612412 | 0.397423 | 0.447800 | 0.114900 | 0.159500 |
| exp-003-c | 0.607080 | 0.397981 | 0.379900 | 0.086900 | 0.121095 |
| exp-004-d | 0.605371 | 0.408339 | 0.377200 | 0.096400 | 0.132345 |
| exp-005-wavelet | 0.595259 | 0.419435 | 0.426119 | 0.088158 | 0.129448 |
| exp-006-weighted-bce | 0.647174 | 0.409225 | 0.405004 | 0.537246 | 0.451214 |
| exp-007-focal | 0.630117 | 0.402705 | 0.412398 | 0.303510 | 0.333079 |
| exp-008-bce-pearson | 0.597070 | 0.417264 | 0.426498 | 0.087385 | 0.132101 |
| exp-009-focal-pearson | 0.644000 | 0.377118 | 0.368402 | 0.151038 | 0.195846 |

## Kayıtlı sonuçlar · test

fixed-september-2026-720hours · Aynı 720 saat üzerinde 3 seed ortalaması; ensemble değil

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-010-final | 0.590713 | 0.443801 | 0.379590 | 0.101010 | 0.143704 |

## Kayıtlı sonuçlar · validation

legacy-development-matched-38fold-3seed · threshold 0.5

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-011-threshold-diagnostics | — | — | 0.410499 | 0.096839 | — |

## Kayıtlı sonuçlar · validation

legacy-development-matched-38fold-3seed · descriptive validation F1 maximum

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-011-threshold-diagnostics | — | — | 0.374879 | 0.783732 | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 2/5

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-012-barrier-diagnostics | — | — | — | — | — |
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 2/2

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-012-barrier-diagnostics | — | — | — | — | — |
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 3/2

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-012-barrier-diagnostics | — | — | — | — | — |
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 1/1

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 1/2

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 1.5/1.5

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 1.5/2

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 2/1

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 2/3

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · development

development-33551-common-timestamps · TP/SL 3/3

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-013-barrier-expansion | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B25; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.390023 | 1.000000 | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B11; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.512724 | 0.989583 | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B12; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.597732 | 1.000000 | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B152; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.460317 | 1.000000 | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B22; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.376803 | 0.997992 | — |

## Kayıtlı sonuçlar · validation

single-split-calibration-20260810-20260830-441hours · B32; mean of 3 seeds; threshold selected on same calibration

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-015-six-barrier-training | — | — | 0.242630 | 1.000000 | — |

## exp-001-a

**A · 6 temel özellik → GRU → BCE**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **selected**

Önceki kayıtlar: yok

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "BCE", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** A, ortak validation BCE ölçütünde seçildi. W_OFF ve L_BCE kontrolleri bu sonucu yeniden kullanır.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.420872 |
| BCE | 0.594507 |
| F1 | 0.142418 |
| accuracy | 0.687868 |
| precision | 0.410499 |
| rank_ic | 0.018313 |
| recall | 0.096839 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.
- A özellikleri B/C/D listesinin birebir altkümesi değildir; A karşılaştırması yalnızca özellik ekleme etkisini izole etmez.
- Mimari parametre bütçeleri eşitlenmedi.

**Kanıt kopyaları:**
- [docs/advisor-abcd-validation-review.md](sources/1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df.md) · SHA256 `1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df`

[Son kayıt](events/000001.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-002-b

**B · 34 mevcut girdi → GRU → BCE**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-001-a

**Yöntem:** {"architecture": "GRU", "feature_count": 34, "loss": "BCE", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** BCE bakımından A geçilmedi. F1 daha yüksek olsa da seçim ölçütü sonradan değiştirilmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.397423 |
| BCE | 0.612412 |
| F1 | 0.159500 |
| accuracy | 0.677700 |
| precision | 0.447800 |
| rank_ic | 0.001562 |
| recall | 0.114900 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.
- A özellikleri B/C/D listesinin birebir altkümesi değildir; A karşılaştırması yalnızca özellik ekleme etkisini izole etmez.
- Mimari parametre bütçeleri eşitlenmedi.

**Kanıt kopyaları:**
- [docs/advisor-abcd-validation-review.md](sources/1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df.md) · SHA256 `1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df`

[Son kayıt](events/000002.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-003-c

**C · 34 mevcut girdi → TCN → BCE**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-001-a

**Yöntem:** {"architecture": "TCN", "feature_count": 34, "loss": "BCE", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** A kontrolü validation BCE bakımından geçilmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.397981 |
| BCE | 0.607080 |
| F1 | 0.121095 |
| accuracy | 0.685800 |
| precision | 0.379900 |
| rank_ic | 0.007430 |
| recall | 0.086900 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.
- A özellikleri B/C/D listesinin birebir altkümesi değildir; A karşılaştırması yalnızca özellik ekleme etkisini izole etmez.
- Mimari parametre bütçeleri eşitlenmedi.

**Kanıt kopyaları:**
- [docs/advisor-abcd-validation-review.md](sources/1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df.md) · SHA256 `1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df`

[Son kayıt](events/000003.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-004-d

**D · 34 mevcut girdi → TCN–GRU → BCE**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-001-a

**Yöntem:** {"architecture": "TCN-GRU", "feature_count": 34, "loss": "BCE", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** 34 girdili adaylar arasında BCE daha iyi; A kontrolü geçilmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.408339 |
| BCE | 0.605371 |
| F1 | 0.132345 |
| accuracy | 0.685000 |
| precision | 0.377200 |
| rank_ic | 0.013251 |
| recall | 0.096400 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.
- A özellikleri B/C/D listesinin birebir altkümesi değildir; A karşılaştırması yalnızca özellik ekleme etkisini izole etmez.
- Mimari parametre bütçeleri eşitlenmedi.

**Kanıt kopyaları:**
- [docs/advisor-abcd-validation-review.md](sources/1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df.md) · SHA256 `1b65963eccac28992df095407cee783dd383427fd85694c90aa0a531255734df`

[Son kayıt](events/000004.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-005-wavelet

**Seçilen A üzerinde nedensel wavelet**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-001-a, exp-002-b, exp-003-c, exp-004-d

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "BCE", "seeds": [42, 43, 44], "wavelet": true}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** W_OFF/A seçildi; fark küçük, istatistiksel anlamlılık iddiası yok.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.419435 |
| BCE | 0.595259 |
| F1 | 0.129448 |
| accuracy | 0.687186 |
| precision | 0.426119 |
| rank_ic | 0.020638 |
| recall | 0.088158 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.

**Kanıt kopyaları:**
- [docs/advisor-wavelet-results.md](sources/4439279f6c030e012880fd56278f43849431b204d5ea4865da76ad021926d32d.md) · SHA256 `4439279f6c030e012880fd56278f43849431b204d5ea4865da76ad021926d32d`

[Son kayıt](events/000005.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-006-weighted-bce

**A üzerinde ağırlıklı BCE**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-005-wavelet

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "weighted-BCE", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** Recall/F1 yükseldi, BCE/AP kötüleşti; ortak seçim ölçütünde saf BCE seçildi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.409225 |
| BCE | 0.647174 |
| F1 | 0.451214 |
| accuracy | 0.607575 |
| precision | 0.405004 |
| rank_ic | 0.002063 |
| recall | 0.537246 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.

**Kanıt kopyaları:**
- [docs/advisor-loss-results.md](sources/be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6.md) · SHA256 `be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6`

[Son kayıt](events/000006.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-007-focal

**A üzerinde focal loss**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-005-wavelet

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "focal", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** Recall/F1 artışı BCE ölçütünde kontrolü geçirmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.402705 |
| BCE | 0.630117 |
| F1 | 0.333079 |
| accuracy | 0.654522 |
| precision | 0.412398 |
| rank_ic | 0.012364 |
| recall | 0.303510 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.

**Kanıt kopyaları:**
- [docs/advisor-loss-results.md](sources/be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6.md) · SHA256 `be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6`

[Son kayıt](events/000013.json) · revizyon 2 · Aktarım kontrolünde elle kopyalama hatası düzeltildi; docs/advisor-loss-results.md değerleri esas alındı. Eski aktarım revizyonu korunur; yeni analiz yok.

## exp-008-bce-pearson

**A üzerinde BCE + Pearson**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-005-wavelet

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "BCE+Pearson", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** BCE/AP bakımından saf BCE kontrolü geçilmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.417264 |
| BCE | 0.597070 |
| F1 | 0.132101 |
| accuracy | 0.688523 |
| precision | 0.426498 |
| rank_ic | 0.017330 |
| recall | 0.087385 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.

**Kanıt kopyaları:**
- [docs/advisor-loss-results.md](sources/be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6.md) · SHA256 `be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6`

[Son kayıt](events/000014.json) · revizyon 2 · Aktarım kontrolünde elle kopyalama hatası düzeltildi; docs/advisor-loss-results.md değerleri esas alındı. Eski aktarım revizyonu korunur; yeni analiz yok.

## exp-009-focal-pearson

**A üzerinde focal + Pearson**

Bu sabit protokolde aday validation BCE bakımından kontrolü iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-005-wavelet

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "focal+Pearson", "seeds": [42, 43, 44], "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "validation", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Epoch ve yöntem: minimum validation BCE; sınıflandırma eşiği 0.5.

**Karar / öğrenilen:** Saf BCE seçildi; Rank IC artışı seçim kuralını değiştirmedi.

**validation** · legacy-development-matched-38fold-3seed · Eşit ağırlıklı 114 fold/seed metrik ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.377118 |
| BCE | 0.644000 |
| F1 | 0.195846 |
| accuracy | 0.663372 |
| precision | 0.368402 |
| rank_ic | 0.018734 |
| recall | 0.151038 |

**Sınırlar / açık noktalar:**
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.
- 38 fold × 3 seed bağımsız 114 istatistiksel tekrar değildir.

**Kanıt kopyaları:**
- [docs/advisor-loss-results.md](sources/be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6.md) · SHA256 `be2cfa1f436ad500c3df5fa6b9f823558e021e410342a68dfd0e37a39000a2e6`

[Son kayıt](events/000009.json) · revizyon 1 · Tarihsel inceleme raporundan aktarım; yeniden çalışma yok.

## exp-010-final

**Donmuş A/W_OFF/BCE · Eylül 2026 final raporu**

Validation ile dondurulan yöntemin ayrılmış testte kayıtlı başarımı nedir?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-006-weighted-bce, exp-007-focal, exp-008-bce-pearson, exp-009-focal-pearson

**Yöntem:** {"architecture": "GRU", "feature_count": 6, "loss": "BCE", "seeds": [42, 43, 44], "threshold": 0.5, "wavelet": false}

**Veri kimliği:** {"evaluation_scope": "test-seen", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": null, "snapshot_id": "legacy-final-september-2026", "split_id": "fixed-final-september-2026-720hours"}

**Seçim kuralı:** Yöntem ve epoch validation ile seçildi; testte model/seed/eşik seçimi yok.

**Karar / öğrenilen:** BCE/AP train-frekans referansından iyi; recall/F1 düşük ve seed duyarlı. Yeni teşhis soruları doğdu; test üzerinden seçim yapılmaz.

**test** · fixed-september-2026-720hours · Aynı 720 saat üzerinde 3 seed ortalaması; ensemble değil

| Ölçüt | Kayıtlı değer |
|---|---:|
| AP | 0.443801 |
| BCE | 0.590713 |
| F1 | 0.143704 |
| accuracy | 0.669444 |
| precision | 0.379590 |
| rank_ic | 0.007261 |
| recall | 0.101010 |

**Sınırlar / açık noktalar:**
- Eylül 2026 görülmüş testtir; yeni seçim ve karşılaştırma için kullanılamaz.
- 3 seed bağımsız test dönemleri değildir; std güven aralığı değildir.
- Kaynak inceleme raporundan aktarım; metrikler yeniden hesaplanmadı.
- Ham veri/model hashleri bu kayıtta henüz bağlı değil; kaynak raporu doğrulamak ham artifact doğrulaması değildir.

**Kanıt kopyaları:**
- [docs/advisor-final-results.md](sources/68a9031401f5bce92cac1dd37752aac1c6451c2db6bccd9454b8ba2206c1361c.md) · SHA256 `68a9031401f5bce92cac1dd37752aac1c6451c2db6bccd9454b8ba2206c1361c`

[Son kayıt](events/000010.json) · revizyon 1 · Tarihsel final raporundan aktarım; yeni değerlendirme yok.

## exp-011-threshold-diagnostics

**Plan · Validation eşik–performans teşhisi**

Düşük recall/F1 sabit 0.5 eşik ve skor dağılımıyla nasıl ilişkili?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-010-final

**Yöntem:** {"aggregation": "114 fold/seed metric mean", "analysis": "precision/recall/F1 vs threshold", "threshold_grid": "0..1 step 0.005; p>=threshold", "training": false}

**Veri kimliği:** {"evaluation_scope": "development-validation-only; September 2026 excluded", "labels_id": "legacy-tp2-sl5-atr-h10", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "legacy-walk-forward-38fold-3seed"}

**Seçim kuralı:** Testte seçim yok. Betimsel teşhis; eşik/etiket kazananı henüz tanımlanmadı.

**Karar / öğrenilen:** 0.50 yalnızca %6.29 pozitif karar üretiyor. Betimsel validation F1 maksimumu 0.265; recall artışı precision ve karar sayısı maliyetiyle geliyor. Üretim eşiği seçilmedi.

**validation** · legacy-development-matched-38fold-3seed · threshold 0.5

| Ölçüt | Kayıtlı değer |
|---|---:|
| f1 | 0.142418 |
| positive_rate | 0.062913 |
| precision | 0.410499 |
| recall | 0.096839 |
| threshold | 0.500000 |

**validation** · legacy-development-matched-38fold-3seed · descriptive validation F1 maximum

| Ölçüt | Kayıtlı değer |
|---|---:|
| f1 | 0.503881 |
| positive_rate | 0.654539 |
| precision | 0.374879 |
| recall | 0.783732 |
| threshold | 0.265000 |

**Sınırlar / açık noktalar:**
- Betimsel geliştirme/validation analizi; bağımsız test performansı değildir.
- Yeni eğitim, inference veya Eylül 2026 testi yapılmadı.
- Çıktı envanteri yol hatası hesaplama tekrarlanmadan düzeltildi.

**Kanıt kopyaları:**
- [research/analyses/diagnostics-20261015/PLAN.md](sources/776f89062d53bd1477fe551a56eda7c122bcc9f4aab88c06463c78a0951d332b.md) · SHA256 `776f89062d53bd1477fe551a56eda7c122bcc9f4aab88c06463c78a0951d332b`
- [research/analyses/diagnostics-20261015/REPORT.md](sources/1d21019de2dc781c4e7c750d1d2146e194db48160361d62c74105dcdb074184e.md) · SHA256 `1d21019de2dc781c4e7c750d1d2146e194db48160361d62c74105dcdb074184e`
- [research/analyses/diagnostics-20261015/results/summary.json](sources/89f15242be426e4a050ed8f4cdaac39a9a2eb37155e2a23bde8875e9c36c6e9e.json) · SHA256 `89f15242be426e4a050ed8f4cdaac39a9a2eb37155e2a23bde8875e9c36c6e9e`
- [research/analyses/diagnostics-20261015/results/input_manifest.json](sources/a1185105da09f8a9e99ef8d529f1042ce00f7cb63d38a8f3013858d2222fa138.json) · SHA256 `a1185105da09f8a9e99ef8d529f1042ce00f7cb63d38a8f3013858d2222fa138`
- [research/analyses/diagnostics-20261015/results/output_manifest.json](sources/7b5d52c5f078ab619c3de3be963c04d8e4237e1489f5f4788f0c993ebd6c9aea.json) · SHA256 `7b5d52c5f078ab619c3de3be963c04d8e4237e1489f5f4788f0c993ebd6c9aea`

[Son kayıt](events/000017.json) · revizyon 3 · Kullanıcı isteğiyle hesaplandı; hash/parite kontrolleri geçti, grafikler ve rapor eklendi.

## exp-012-barrier-diagnostics

**Plan · ATR bariyerleri ve etiket dağılımı**

TP/SL seçimi ilk temas sınıflarını ve süre dolumu getirilerini nasıl etkiliyor?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-010-final

**Yöntem:** {"analysis": "first-touch counts and timeout return distribution", "horizon_hours": 10, "same_bar_rule": null, "tp_sl_atr": [[2, 5], [2, 2], [3, 2]], "training": false}

**Veri kimliği:** {"evaluation_scope": "development-validation-only; September 2026 excluded", "labels_id": "diagnostic-tp2sl5-tp2sl2-tp3sl2-h10", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "development-33551-common-timestamps"}

**Seçim kuralı:** Testte seçim yok. Betimsel teşhis; eşik/etiket kazananı henüz tanımlanmadı.

**Karar / öğrenilen:** 2/5 düzeninde %63.17 timeout. 2/2 ve 3/2 pozitif etiket oranını artırmadı. Pozitif getirili timeout da 0 etiketli; hedef getiri yönünden farklı. Bariyer seçilmedi.

**development** · development-33551-common-timestamps · TP/SL 2/5

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_assigned_stop | 22.000000 |
| n | 33551.000000 |
| positive_label_pct | 30.958839 |
| profit_first | 10387.000000 |
| profit_pct | 30.958839 |
| stop_first | 1971.000000 |
| stop_pct | 5.874639 |
| timeout | 21193.000000 |
| timeout_pct | 63.166523 |

**development** · development-33551-common-timestamps · TP/SL 2/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_assigned_stop | 122.000000 |
| n | 33551.000000 |
| positive_label_pct | 28.583351 |
| profit_first | 9590.000000 |
| profit_pct | 28.583351 |
| stop_first | 9872.000000 |
| stop_pct | 29.423862 |
| timeout | 14089.000000 |
| timeout_pct | 41.992787 |

**development** · development-33551-common-timestamps · TP/SL 3/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_assigned_stop | 62.000000 |
| n | 33551.000000 |
| positive_label_pct | 16.145569 |
| profit_first | 5417.000000 |
| profit_pct | 16.145569 |
| stop_first | 10309.000000 |
| stop_pct | 30.726357 |
| timeout | 17825.000000 |
| timeout_pct | 53.128074 |

**Sınırlar / açık noktalar:**
- Betimsel geliştirme/validation analizi; bağımsız test performansı değildir.
- Yeni eğitim, inference veya Eylül 2026 testi yapılmadı.
- Çıktı envanteri yol hatası hesaplama tekrarlanmadan düzeltildi.

**Kanıt kopyaları:**
- [research/analyses/diagnostics-20261015/PLAN.md](sources/776f89062d53bd1477fe551a56eda7c122bcc9f4aab88c06463c78a0951d332b.md) · SHA256 `776f89062d53bd1477fe551a56eda7c122bcc9f4aab88c06463c78a0951d332b`
- [research/analyses/diagnostics-20261015/REPORT.md](sources/1d21019de2dc781c4e7c750d1d2146e194db48160361d62c74105dcdb074184e.md) · SHA256 `1d21019de2dc781c4e7c750d1d2146e194db48160361d62c74105dcdb074184e`
- [research/analyses/diagnostics-20261015/results/summary.json](sources/89f15242be426e4a050ed8f4cdaac39a9a2eb37155e2a23bde8875e9c36c6e9e.json) · SHA256 `89f15242be426e4a050ed8f4cdaac39a9a2eb37155e2a23bde8875e9c36c6e9e`
- [research/analyses/diagnostics-20261015/results/input_manifest.json](sources/a1185105da09f8a9e99ef8d529f1042ce00f7cb63d38a8f3013858d2222fa138.json) · SHA256 `a1185105da09f8a9e99ef8d529f1042ce00f7cb63d38a8f3013858d2222fa138`
- [research/analyses/diagnostics-20261015/results/output_manifest.json](sources/7b5d52c5f078ab619c3de3be963c04d8e4237e1489f5f4788f0c993ebd6c9aea.json) · SHA256 `7b5d52c5f078ab619c3de3be963c04d8e4237e1489f5f4788f0c993ebd6c9aea`

[Son kayıt](events/000018.json) · revizyon 3 · Kullanıcı isteğiyle hesaplandı; hash/parite kontrolleri geçti, grafikler ve rapor eklendi.

## exp-013-barrier-expansion

**Genişletilmiş 10 bariyer senaryosu · denge ve hedef teşhisi**

Ek ATR bariyerleri sınıf dengesi, süre dolumu, temas belirsizliği ve brüt getiri bakımından hangi ödünleşimleri getiriyor?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-012-barrier-diagnostics

**Yöntem:** {"horizon_hours": 10, "same_bar_rule": "stop-first", "tp_sl_atr": [[2, 5], [2, 2], [3, 2], [1, 1], [1, 2], [1.5, 1.5], [1.5, 2], [2, 1], [2, 3], [3, 3]], "training": false}

**Veri kimliği:** {"evaluation_scope": "development-validation-only; September 2026 excluded", "labels_id": "barrier-expansion-10-scenarios-h10", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "development-33551-common-timestamps"}

**Seçim kuralı:** Kullanıcı dengeli değerlendirme istedi. Sınıf dengesine uzaklık, timeout ve çift temas için Pareto; getiri ve yıllık tutarlılık ayrı yorum. Nihai model/strateji kazananı seçilmez.

**Karar / öğrenilen:** Dengeli değerlendirmede sonraki validation için 1/1, 1/2, 1.5/2 kısa listesi; 2/5 kontrol korunur. Kesin model/strateji kazananı veya üretim bariyeri seçilmedi.

**development** · development-33551-common-timestamps · TP/SL 2/5

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.065572 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.551304 |
| positive_mean_fwd_pct | 1.342379 |
| profit_first | 10387.000000 |
| profit_first_pct | 30.958839 |
| stop_first | 1971.000000 |
| timeout | 21193.000000 |
| timeout_mean_fwd_pct | -0.338672 |
| timeout_pct | 63.166523 |

**development** · development-33551-common-timestamps · TP/SL 2/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.363626 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.501804 |
| positive_mean_fwd_pct | 1.376081 |
| profit_first | 9590.000000 |
| profit_first_pct | 28.583351 |
| stop_first | 9872.000000 |
| timeout | 14089.000000 |
| timeout_mean_fwd_pct | 0.042376 |
| timeout_pct | 41.992787 |

**development** · development-33551-common-timestamps · TP/SL 3/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.184793 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.320630 |
| positive_mean_fwd_pct | 1.881761 |
| profit_first | 5417.000000 |
| profit_first_pct | 16.145569 |
| stop_first | 10309.000000 |
| timeout | 17825.000000 |
| timeout_mean_fwd_pct | 0.229684 |
| timeout_pct | 53.128074 |

**development** · development-33551-common-timestamps · TP/SL 1/1

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 1.886680 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.547355 |
| positive_mean_fwd_pct | 0.757647 |
| profit_first | 14971.000000 |
| profit_first_pct | 44.621621 |
| stop_first | 15605.000000 |
| timeout | 2975.000000 |
| timeout_mean_fwd_pct | 0.029221 |
| timeout_pct | 8.867098 |

**development** · development-33551-common-timestamps · TP/SL 1/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.718309 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.796463 |
| positive_mean_fwd_pct | 0.732198 |
| profit_first | 18248.000000 |
| profit_first_pct | 54.388841 |
| stop_first | 8089.000000 |
| timeout | 7214.000000 |
| timeout_mean_fwd_pct | -0.242804 |
| timeout_pct | 21.501595 |

**development** · development-33551-common-timestamps · TP/SL 1.5/1.5

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.774940 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.568726 |
| positive_mean_fwd_pct | 1.069700 |
| profit_first | 12362.000000 |
| profit_first_pct | 36.845400 |
| stop_first | 12610.000000 |
| timeout | 8579.000000 |
| timeout_mean_fwd_pct | 0.030045 |
| timeout_pct | 25.570028 |

**development** · development-33551-common-timestamps · TP/SL 1.5/2

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.518613 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.630169 |
| positive_mean_fwd_pct | 1.062722 |
| profit_first | 13182.000000 |
| profit_first_pct | 39.289440 |
| stop_first | 9270.000000 |
| timeout | 11099.000000 |
| timeout_mean_fwd_pct | -0.087425 |
| timeout_pct | 33.080981 |

**development** · development-33551-common-timestamps · TP/SL 2/1

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.795803 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.377861 |
| positive_mean_fwd_pct | 1.410914 |
| profit_first | 7743.000000 |
| profit_first_pct | 23.078299 |
| stop_first | 18560.000000 |
| timeout | 7248.000000 |
| timeout_mean_fwd_pct | 0.324661 |
| timeout_pct | 21.602933 |

**development** · development-33551-common-timestamps · TP/SL 2/3

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.184793 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.537840 |
| positive_mean_fwd_pct | 1.357423 |
| profit_first | 10140.000000 |
| profit_first_pct | 30.222646 |
| stop_first | 5422.000000 |
| timeout | 17989.000000 |
| timeout_mean_fwd_pct | -0.133501 |
| timeout_pct | 53.616882 |

**development** · development-33551-common-timestamps · TP/SL 3/3

| Ölçüt | Kayıtlı değer |
|---|---:|
| both_same_bar_pct | 0.110280 |
| n | 33551.000000 |
| negative_mean_fwd_pct | -0.339493 |
| positive_mean_fwd_pct | 1.859565 |
| profit_first | 5713.000000 |
| profit_first_pct | 17.027808 |
| stop_first | 5677.000000 |
| timeout | 22161.000000 |
| timeout_mean_fwd_pct | 0.052411 |
| timeout_pct | 66.051683 |

**Sınırlar / açık noktalar:**
- Betimsel geliştirme analizi; gelecekteki fiyatlardan türeyen etiketler için koşullu getiri bağımsız model becerisi değildir.
- Aynı saatlik mumda temas sırası bilinmiyor; zarar önce kuralı.
- Masraf/funding/slippage yok.

**Kanıt kopyaları:**
- [research/analyses/barrier-expansion-20261015/PLAN.md](sources/2604a9073883e1e754fb01cf3ecb82b720236bf044f74924f7efff74a9cc7c88.md) · SHA256 `2604a9073883e1e754fb01cf3ecb82b720236bf044f74924f7efff74a9cc7c88`
- [research/analyses/barrier-expansion-20261015/REPORT.md](sources/ea918d84ac163c10d04dd7e96bc817a6f112afd6ea8977ddc4a8eae460ae8cd2.md) · SHA256 `ea918d84ac163c10d04dd7e96bc817a6f112afd6ea8977ddc4a8eae460ae8cd2`
- [research/analyses/barrier-expansion-20261015/results/barrier_comparison.csv](sources/bf6f678dec468cb689d05acaac7277e7469b93b6f53ce8526c7b8b8de0a9f2a6.csv) · SHA256 `bf6f678dec468cb689d05acaac7277e7469b93b6f53ce8526c7b8b8de0a9f2a6`
- [research/analyses/barrier-expansion-20261015/results/barrier_by_year.csv](sources/dbd668b80f6cebea4e837d88e389e08d69fcbaf38f29a9662c5b831d51dfd411.csv) · SHA256 `dbd668b80f6cebea4e837d88e389e08d69fcbaf38f29a9662c5b831d51dfd411`
- [research/analyses/barrier-expansion-20261015/results/manifest.json](sources/378cbdf4aefe09cc4e48a72ab800a61d3558cd250b8ff029cb8ace72a1e7d0ee.json) · SHA256 `378cbdf4aefe09cc4e48a72ab800a61d3558cd250b8ff029cb8ace72a1e7d0ee`
- [research/analyses/barrier-expansion-20261015/results/output_manifest.json](sources/2dd82d3a29953679f99ef36b7b7dac82026568dd341b0ad05cf79b0899a80d10.json) · SHA256 `2dd82d3a29953679f99ef36b7b7dac82026568dd341b0ad05cf79b0899a80d10`

[Son kayıt](events/000020.json) · revizyon 2 · 10 senaryo ortak veri üzerinde hesaplandı; önceki üç senaryo paritesi geçti. Kullanıcının dengeli değerlendirme tercihine göre adaylar raporlandı.

## exp-014-barrier-training

**Dört ATR bariyeri: GRU/BCE, ayrı epoch/eşik doğrulaması ve Ekim testi**

2/5, 1/1, 1/2, 1.5/2 hedefleriyle aynı GRU için öğrenme ve eşik başarımı nasıl değişiyor?

Kampanya: `campaign-002` · Durum: **abandoned** · Sonuç: **inconclusive**

Önceki kayıtlar: exp-013-barrier-expansion

**Yöntem:** {"architecture": "GRU", "horizon_hours": 10, "loss": "BCE", "same_bar_rule": "stop-first", "seeds": [42, 43, 44], "tp_sl_atr": [[2, 5], [1, 1], [1, 2], [1.5, 2]], "training_runs": 12}

**Veri kimliği:** {"evaluation_scope": "planned; no new training or test executed", "labels_id": "barriers-four-h10", "raw_sha256": "f3a29be9f7a935ca144fe70a701b41072f30a1b2432b177faa309a8c37b404c6", "snapshot_id": "legacy-final-fit-raw", "split_id": "fixed-train-20251218-20260715-val-20260717-20260808-cal-20260810-20260830-test-20261002-20261014"}

**Seçim kuralı:** Epoch: validation BCE. Threshold: mean calibration F1, ties highest threshold. Candidate: calibration BCE skill, ties ID. Test cannot select.

**Karar / öğrenilen:** Yeni yürütmeler için altı adaylı exp-015-six-barrier-training planıyla değiştirildi. Eski plan/kanıtlar ve varsa Colab checkpointleri korunur; önceki eğitim yürütme durumu teyit edilmedi. Kullanıcı Ekim testinin çalıştırılmadığını doğruladı.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- 13-day single holdout, overlapping labels, no trading costs.
- Previously seen August is development only; September excluded from evaluation.
- Different label targets; no absolute strategy winner claim.

**Kanıt kopyaları:**
- [research/analyses/barrier-training-20261015/PLAN.md](sources/712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32.md) · SHA256 `712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32`

[Son kayıt](events/000022.json) · revizyon 2 · Kullanıcı test görülmeden 2/2 ve 3/2 eklenmesini istedi; önceki dört adaylı plan korundu.

## exp-015-six-barrier-training

**Altı ATR bariyeri: B25/B11/B12/B152/B22/B32 · GRU/BCE**

Aynı GRU üzerinde önceki dört adayla 2/2 ve 3/2 bariyerlerinin doğrulama/test sonuçları nasıl karşılaştırılıyor?

Kampanya: `campaign-002` · Durum: **abandoned** · Sonuç: **mixed**

Önceki kayıtlar: exp-014-barrier-training

**Yöntem:** {"architecture": "GRU", "horizon_hours": 10, "loss": "BCE", "same_bar_rule": "stop-first", "seeds": [42, 43, 44], "tp_sl_atr": [[2, 5], [1, 1], [1, 2], [1.5, 2], [2, 2], [3, 2]], "training_runs": 18}

**Veri kimliği:** {"evaluation_scope": "Actual: single temporal split in 2025–2026; calibration only, 441 unique hours per seed. Not comparable to original 38-fold cohort.", "labels_id": "barriers-six-h10", "raw_sha256": "f3a29be9f7a935ca144fe70a701b41072f30a1b2432b177faa309a8c37b404c6", "snapshot_id": "legacy-final-fit-raw", "split_id": "fixed-train-20251218-20260715-val-20260717-20260808-cal-20260810-20260830-test-20261002-20261014"}

**Seçim kuralı:** Epoch: validation BCE. Threshold: mean calibration F1, ties highest threshold. Candidate: calibration BCE skill, ties ID. Test cannot select.

**Karar / öğrenilen:** Eğitim/kalibrasyon kanıtları korunuyor; test aşaması yürütülmeden bu protokol bırakıldı. Kullanıcı özgün veri/split düzeninde seçici sinyal hedefiyle devam edilmesini istedi; yeni kimlik exp-016-selective-walk-forward.

**validation** · single-split-calibration-20260810-20260830-441hours · B25; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.561175 |
| ap | 0.476936 |
| ap_lift | 1.222842 |
| bce | 0.733768 |
| bce_reference | 0.682598 |
| bce_skill | -0.074964 |
| f1 | 0.561175 |
| f1_at_05 | 0.325332 |
| f1_gain | -0.000000 |
| positive_rate | 0.390023 |
| precision | 0.390023 |
| precision_at_05 | 0.461294 |
| predicted_positive_rate | 1.000000 |
| predicted_positive_rate_at_05 | 0.215420 |
| recall | 1.000000 |
| recall_at_05 | 0.253876 |
| threshold | 0.010000 |
| train_prevalence | 0.311433 |

**validation** · single-split-calibration-20260810-20260830-441hours · B11; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.673684 |
| ap | 0.490875 |
| ap_lift | 0.966410 |
| bce | 0.709722 |
| bce_reference | 0.703215 |
| bce_skill | -0.009254 |
| f1 | 0.675463 |
| f1_at_05 | 0.199734 |
| f1_gain | 0.001779 |
| positive_rate | 0.507937 |
| precision | 0.512724 |
| precision_at_05 | 0.424309 |
| predicted_positive_rate | 0.980348 |
| predicted_positive_rate_at_05 | 0.163265 |
| recall | 0.989583 |
| recall_at_05 | 0.136905 |
| threshold | 0.255000 |
| train_prevalence | 0.436809 |

**validation** · single-split-calibration-20260810-20260830-441hours · B12; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.745377 |
| ap | 0.600563 |
| ap_lift | 1.010871 |
| bce | 0.698364 |
| bce_reference | 0.681120 |
| bce_skill | -0.025318 |
| f1 | 0.748222 |
| f1_at_05 | 0.672698 |
| f1_gain | 0.002845 |
| positive_rate | 0.594104 |
| precision | 0.597732 |
| precision_at_05 | 0.600282 |
| predicted_positive_rate | 0.993953 |
| predicted_positive_rate_at_05 | 0.758881 |
| recall | 1.000000 |
| recall_at_05 | 0.767176 |
| threshold | 0.200000 |
| train_prevalence | 0.540687 |

**validation** · single-split-calibration-20260810-20260830-441hours · B152; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.630435 |
| ap | 0.444820 |
| ap_lift | 0.966333 |
| bce | 0.720912 |
| bce_reference | 0.699447 |
| bce_skill | -0.030689 |
| f1 | 0.630435 |
| f1_at_05 | 0.266331 |
| f1_gain | 0.000000 |
| positive_rate | 0.460317 |
| precision | 0.460317 |
| precision_at_05 | 0.390760 |
| predicted_positive_rate | 1.000000 |
| predicted_positive_rate_at_05 | 0.239607 |
| recall | 1.000000 |
| recall_at_05 | 0.206897 |
| threshold | 0.130000 |
| train_prevalence | 0.392606 |

**validation** · single-split-calibration-20260810-20260830-441hours · B22; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.546952 |
| ap | 0.411127 |
| ap_lift | 1.092212 |
| bce | 0.765239 |
| bce_reference | 0.678971 |
| bce_skill | -0.127057 |
| f1 | 0.547056 |
| f1_at_05 | 0.319777 |
| f1_gain | 0.000104 |
| positive_rate | 0.376417 |
| precision | 0.376803 |
| precision_at_05 | 0.454243 |
| predicted_positive_rate | 0.996977 |
| predicted_positive_rate_at_05 | 0.202570 |
| recall | 0.997992 |
| recall_at_05 | 0.248996 |
| threshold | 0.020000 |
| train_prevalence | 0.291340 |

**validation** · single-split-calibration-20260810-20260830-441hours · B32; mean of 3 seeds; threshold selected on same calibration

| Ölçüt | Kayıtlı değer |
|---|---:|
| all_positive_f1 | 0.390511 |
| ap | 0.262851 |
| ap_lift | 1.083338 |
| bce | 0.681339 |
| bce_reference | 0.576978 |
| bce_skill | -0.180876 |
| f1 | 0.390511 |
| f1_at_05 | 0.044983 |
| f1_gain | -0.000000 |
| positive_rate | 0.242630 |
| precision | 0.242630 |
| precision_at_05 | 0.283066 |
| predicted_positive_rate | 1.000000 |
| predicted_positive_rate_at_05 | 0.024943 |
| recall | 1.000000 |
| recall_at_05 | 0.024922 |
| threshold | 0.000000 |
| train_prevalence | 0.159534 |

**Sınırlar / açık noktalar:**
- 13-day single holdout, overlapping labels, no trading costs.
- Previously seen August is development only; September excluded from evaluation.
- Different label targets; no absolute strategy winner claim.
- Protocol deviated from intended fixed historical dataset and walk-forward splits; F1 objective was introduced by assistant, not defined by user.
- Package lacks row-level predictions/checkpoints; aggregate consistency and logs only.
- All candidates have negative calibration BCE skill; automatic B11 selection lacks a reject-all gate.

**Kanıt kopyaları:**
- [research/analyses/barrier-training-20261015/PLAN.md](sources/712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32.md) · SHA256 `712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32`
- [research/analyses/six-barrier-training-20261015/PLAN.md](sources/aff1479c2d0ba1ddd54a430e1a185fff9c9606d2be0645e1f6456e5ea376e144.md) · SHA256 `aff1479c2d0ba1ddd54a430e1a185fff9c9606d2be0645e1f6456e5ea376e144`
- [research/analyses/six-barrier-review-20261016/REPORT.md](sources/1fd8ac1f809f907b849f5462065a73bd043375c4698108deb38b4e304ace6247.md) · SHA256 `1fd8ac1f809f907b849f5462065a73bd043375c4698108deb38b4e304ace6247`
- [reports/six-barrier-review-20261016/audit.json](sources/d07b2284d80162d613088d74130c0c629396700ae4c17b9e4b34474083af6a6d.json) · SHA256 `d07b2284d80162d613088d74130c0c629396700ae4c17b9e4b34474083af6a6d`
- [reports/six-barrier-review-20261016/review_metrics.csv](sources/7f08af8108431662623764fa671eb6c3deffbb7657f6ca503b37eae934c41b58.csv) · SHA256 `7f08af8108431662623764fa671eb6c3deffbb7657f6ca503b37eae934c41b58`
- [reports/six-barrier-review-20261016/epochs_from_log.csv](sources/73d6f4cc6cbf414c0d767088a2e0939a74687812073a37f1774470ea3c24d82a.csv) · SHA256 `73d6f4cc6cbf414c0d767088a2e0939a74687812073a37f1774470ea3c24d82a`
- [reports/six-barrier-review-20261016/received/artifacts/plan.json](sources/dcd7c6f4bc15838bd82d4bc08babc20ba00f596dd152a99fc482c6154e0d6afb.json) · SHA256 `dcd7c6f4bc15838bd82d4bc08babc20ba00f596dd152a99fc482c6154e0d6afb`
- [reports/six-barrier-review-20261016/received/artifacts/freeze.json](sources/5ee50ec8a18785d95e7408caa4bd2e34764b88b0d09bc37247541ac69fd0c739.json) · SHA256 `5ee50ec8a18785d95e7408caa4bd2e34764b88b0d09bc37247541ac69fd0c739`
- [reports/six-barrier-review-20261016/received/reports/calibration_comparison.csv](sources/e4b5a088a66b6f6b7b61ff8f926ac2bdbf1c61828db2388de1c8b94e10ae812b.csv) · SHA256 `e4b5a088a66b6f6b7b61ff8f926ac2bdbf1c61828db2388de1c8b94e10ae812b`
- [reports/six-barrier-review-20261016/received/reports/B11_thresholds.csv](sources/19eb00af5f68a128bca78b955695f6ca5e99e0c4dd267f9549866a4ab05f9649.csv) · SHA256 `19eb00af5f68a128bca78b955695f6ca5e99e0c4dd267f9549866a4ab05f9649`
- [reports/six-barrier-review-20261016/received/reports/B12_thresholds.csv](sources/aa9da425e64c95b0c6cc30ddf81128e4a0c4018cf6be550b38de1c08a7dea858.csv) · SHA256 `aa9da425e64c95b0c6cc30ddf81128e4a0c4018cf6be550b38de1c08a7dea858`
- [reports/six-barrier-review-20261016/received/reports/B152_thresholds.csv](sources/299d1de9649a6c01f249a0e20aff1a0433d22b083c00a2bddf4315f53e2eb602.csv) · SHA256 `299d1de9649a6c01f249a0e20aff1a0433d22b083c00a2bddf4315f53e2eb602`
- [reports/six-barrier-review-20261016/received/reports/B22_thresholds.csv](sources/20ba2c857cef8364444a38a17719f380b530eef404bf1b7144c33ea6446de517.csv) · SHA256 `20ba2c857cef8364444a38a17719f380b530eef404bf1b7144c33ea6446de517`
- [reports/six-barrier-review-20261016/received/reports/B25_thresholds.csv](sources/e7b0f6f4015857651e33292deb92392f9085db5c345b0c24394283f8188f38ba.csv) · SHA256 `e7b0f6f4015857651e33292deb92392f9085db5c345b0c24394283f8188f38ba`
- [reports/six-barrier-review-20261016/received/reports/B32_thresholds.csv](sources/bd2f3b33b05356231b5ce1390179f81fc513e83c63218ef06e4e4b9a1a839ea2.csv) · SHA256 `bd2f3b33b05356231b5ce1390179f81fc513e83c63218ef06e4e4b9a1a839ea2`

[Son kayıt](events/000025.json) · revizyon 3 · Özgün kohorttan sapan çalışmanın testi yapılmayacak; sonuçlar silinmedi.

## exp-016-selective-walk-forward

**Özgün 38-fold kohortta altı bariyer · seçici sinyal incelemesi**

Sabit tarih/split/özellik/model altında hangi bariyerler precision, recall, sinyal sayısı ve dönem tutarlılığında seçicilik sağlıyor?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-015-six-barrier-training

**Yöntem:** {"architecture": "GRU", "automatic_threshold_selection": false, "candidates": ["B25", "B11", "B12", "B152", "B22", "B32"], "folds": 38, "hardware_profile": "selective-a100", "horizon_hours": 10, "loss": "BCE", "precision_scenarios": [0.6, 0.65, 0.7], "purge_embargo": [24, 24], "same_bar_rule": "stop-first", "seeds": [42, 43, 44], "sequence_length": 64, "step_bars": 720, "train_validation_test_bars": [5040, 1080, 720], "training_gpu": "NVIDIA A100-SXM4-40GB", "training_runs": 684}

**Veri kimliği:** {"evaluation_scope": "Historical validation diagnostics completed; 684 fold/seed results reviewed, no test evaluation.", "labels_id": "six-barriers-h10-tp-positive-sl-timeout-negative", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original-33551-hours-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Epoch minimum validation BCE. User explicitly chose descriptive precision 60/65/70 comparison without locking a target or threshold. No automatic winner; report support, recall and fold/seed stability.

**Karar / öğrenilen:** Recovery completed by user in Colab. Review ZIP verified: 2052 hashes, 684 prediction metric recalculations and epoch selections agree. B12 shows selective precision potential but temporal/seed instability and macro-vs-pooled differences remain. No threshold/barrier winner selected. Existing all-fold-nonempty scenario filter is not a user-approved acceptance rule; empty precision scenario files must not be interpreted as absence of any high-precision thresholds.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Validation used for epoch choice and diagnostics is optimistic.
- Overlapping folds/seeds are not independent samples.
- Negative label includes timeout; not a pure TP-vs-SL classifier.
- Precision acceptance and signal-support criteria not yet locked.
- B32 seed44 fold34 weights unavailable; fold35 history reconstructed; fold36 resumed; fold37 retrained.
- Raw prepared frames and model weights excluded from reviewed ZIP; not independently audited here.

**Kanıt kopyaları:**
- [research/analyses/selective-walkforward-20261016/PLAN.md](sources/f210515ad627820b44b0b146997bcac1e2460aee8a2f78a8ab94796c012a0bbf.md) · SHA256 `f210515ad627820b44b0b146997bcac1e2460aee8a2f78a8ab94796c012a0bbf`
- [research/analyses/selective-walkforward-20261016/PLAN.md](sources/93673fead076cdcc2cbf9a6ecadddb80e6b8accb843776aee4ccbb805e0902c0.md) · SHA256 `93673fead076cdcc2cbf9a6ecadddb80e6b8accb843776aee4ccbb805e0902c0`
- [research/analyses/selective-walkforward-20261016/A100.md](sources/103885ed998545f5f86522ee6d5d7eef48c74fba4bf85b2232575f4400077c94.md) · SHA256 `103885ed998545f5f86522ee6d5d7eef48c74fba4bf85b2232575f4400077c94`
- [research/analyses/drive-recovery-20261017/REPORT.md](sources/c4091d209690f73e94381e31af60ee0921ea6e2f9203bfbb7e3d16fb3d5ee08c.md) · SHA256 `c4091d209690f73e94381e31af60ee0921ea6e2f9203bfbb7e3d16fb3d5ee08c`
- [research/analyses/drive-recovery-20261017/inventory.json](sources/d35c27f02eb1a199809f5571227a63b041e787d7c2a0f65c2837caa3b7955e78.json) · SHA256 `d35c27f02eb1a199809f5571227a63b041e787d7c2a0f65c2837caa3b7955e78`
- [research/analyses/selective-review-20261017/REPORT.md](sources/02a66f64fa51b6222473ad45304468581aa6ec149bba926e86d482269aa7e462.md) · SHA256 `02a66f64fa51b6222473ad45304468581aa6ec149bba926e86d482269aa7e462`

[Son kayıt](events/000030.json) · revizyon 5 · User completed recovery; inspect validation evidence and preserve findings without new training or test evaluation.

## exp-017-threshold-transfer

**Altı bariyer: validation eşik bölgeleri ve son model penceresine aktarım**

Genel validation eşik bölgeleri son fold modellerine taşınabiliyor mu?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-016-selective-walk-forward

**Yöntem:** {"changed_factor": "descriptive aggregation and threshold-neighborhood analysis only", "neighborhood": [-0.01, -0.005, 0, 0.005, 0.01], "new_training": false, "precision_goals": [0.6, 0.65, 0.7], "seeds": [42, 43, 44], "source_commit": "4bac0822b73d7050ab4718ab9ac1e7596d8a90c4", "source_zip_sha256": "76d09912ab27349d003041a4f2356fbe989cbd76601feaa4793d8e342ca16eff", "test_evaluations": 0}

**Veri kimliği:** {"evaluation_scope": "historical validation only; all38 and last37 reported separately; no October data accessed", "labels_id": "six-barriers-h10-tp-positive-sl-timeout-negative", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original-33551-hours-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Descriptive: each seed pooled precision reaches goal at all five adjacent thresholds; show lowest eligible center and support. No minimum-support acceptance rule invented. No deployment threshold or test winner selected.

**Karar / öğrenilen:** Validation threshold comparison completed. Propose common latest historical fold37 (not performance-selected) for existing-model transfer test; 18 best-epoch identities documented, weights not verified from ZIP. High-precision all-fold regions do not transfer reliably to last-fold models. Test lock not created; 0.40/0.50 reference and descriptive scenario comparison remain available.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Epoch selection and threshold diagnostics reuse validation.
- Overlapping folds/seeds are not independent.
- Sparse regions are not accepted policies; no primary precision/support target locked.
- Historical models end validation in November 2025; October 2026 transfer includes model ageing.
- Raw checkpoint weights not present in review ZIP.

**Kanıt kopyaları:**
- [research/analyses/threshold-transfer-20261017/REPORT.md](sources/e3a4801d3ca3c553ec655d75170c40afc3ffcd5c0bbb799a910d6d27f3aed7f6.md) · SHA256 `e3a4801d3ca3c553ec655d75170c40afc3ffcd5c0bbb799a910d6d27f3aed7f6`
- [research/analyses/threshold-transfer-20261017/threshold_comparison.csv](sources/c6a2f64aaaefc32c4dc3fe035dc27fc058bc3a059e725fa0fbef55d71905e8fd.csv) · SHA256 `c6a2f64aaaefc32c4dc3fe035dc27fc058bc3a059e725fa0fbef55d71905e8fd`
- [research/analyses/threshold-transfer-20261017/descriptive_regions.csv](sources/8e86b55942c478b796fd59f9e687203342a3a94941309ff684abbc2192daae0b.csv) · SHA256 `8e86b55942c478b796fd59f9e687203342a3a94941309ff684abbc2192daae0b`
- [research/analyses/threshold-transfer-20261017/proposed_models.csv](sources/a42021346786b69300f04f24d85542302a11a56dbbdcdad0d728433479ff0036.csv) · SHA256 `a42021346786b69300f04f24d85542302a11a56dbbdcdad0d728433479ff0036`

[Son kayıt](events/000031.json) · revizyon 1 · Authorized validation-only threshold comparison; preserve model-transfer limitations before test.

## exp-018-validation-stability

**Puan dağılımı, sıralama gücü ve dönem/seed kararlılığı teşhisi**

Son dönemde sinyal kaybı puan ölçeğinden mi, ayırt etme kaybından mı; yüksek precision dönemlerde tekrarlanıyor mu?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-017-threshold-transfer

**Yöntem:** {"analysis": "score distributions, AP/prevalence, ROC AUC, BCE skill, top102 ranking, seed rank agreement, fixed-threshold recurrence", "folds": 38, "new_training": false, "precision_goals": [0.6, 0.65, 0.7], "seeds": [42, 43, 44], "source_zip_sha256": "76d09912ab27349d003041a4f2356fbe989cbd76601feaa4793d8e342ca16eff", "support_sensitivity": [1, 10, 30, 100], "test_evaluations": 0, "thresholds": [0.4, 0.5, 0.575, 0.62, 0.64, 0.705, 0.755]}

**Veri kimliği:** {"evaluation_scope": "historical validation only; no September or October evaluation", "labels_id": "six-barriers-h10-tp-positive-sl-timeout-negative", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original-33551-hours-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** No model/threshold selected. Previously discussed thresholds only. Support sensitivity is descriptive, not a new acceptance constraint. Top102 ranking is retrospective diagnostic, not a live strategy.

**Karar / öğrenilen:** B12 last-fold scores narrow and all maxima stay below .70; seed43 also has weak ranking (AUC .4642) while seeds42/44 retain top-tail discrimination. B11 last-fold degrades across all seeds; other barriers do not uniformly degrade. B12 all-three-seed recurrence with >=30 signals is 15/38 at .575/60%, 2/38 at .705/65%, 0/38 at .755/70%. Keep final test closed pending a justified model/policy; no automatic retraining.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Same validation used for epoch choice and diagnostics; optimistic.
- Overlapping windows, labels and seeds are not independent; no confidence intervals or significance claim.
- No raw-feature or checkpoint analysis; causal explanation not established.
- High precision with small support is not acceptance evidence.
- AP/BCE compare different targets across barriers; no automatic winner.

**Kanıt kopyaları:**
- [research/analyses/stability-20261017/REPORT.md](sources/c94f3e9be2616f7230e097de9352479033f8b810022fa45dc4c862ae0c956d14.md) · SHA256 `c94f3e9be2616f7230e097de9352479033f8b810022fa45dc4c862ae0c956d14`
- [research/analyses/stability-20261017/PROVENANCE.md](sources/4939e78d970a206240eb50221e4cef7acfaa3c0ce5b4004a842ce2abe0464009.md) · SHA256 `4939e78d970a206240eb50221e4cef7acfaa3c0ce5b4004a842ce2abe0464009`
- [research/analyses/stability-20261017/fold_seed_diagnostics.csv](sources/e3780d896d2e424762d832a89017275e7ce3e54fdbb0c36e4355f42c876d0f36.csv) · SHA256 `e3780d896d2e424762d832a89017275e7ce3e54fdbb0c36e4355f42c876d0f36`
- [research/analyses/stability-20261017/threshold_stability.csv](sources/7f8cfe0e5bd18ff1158e795212c76edc41fdcbddc4ceb5bfa9e9406e4a198c99.csv) · SHA256 `7f8cfe0e5bd18ff1158e795212c76edc41fdcbddc4ceb5bfa9e9406e4a198c99`
- [reports/stability-20261017/analysis-source.txt](sources/28891434c59711511f4d6df50d0d2ab087127b3e54d3381436003e17caf7d7cc.txt) · SHA256 `28891434c59711511f4d6df50d0d2ab087127b3e54d3381436003e17caf7d7cc`

[Son kayıt](events/000032.json) · revizyon 1 · Authorized diagnosis of validation score shift, discrimination and threshold recurrence; no training or test.
