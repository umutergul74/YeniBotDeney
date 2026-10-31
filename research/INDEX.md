# Deney defteri

Bu görünüm kayıtlı sonuçları listeler; analiz veya eğitim çalıştırmaz.
Kaynak: `events/` içindeki eklemeli kayıtlar. Rakamlar kaynak raporların yuvarlatılmış değerleridir.
Validation ve test ayrı kapsamdır; bu tablo otomatik bir başarı sıralaması değildir.

**33 deney/plan · 53 geçmiş kaydı**

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
| [exp-019-root-cause-probes](#exp-019-root-cause-probes) | Eski proje incelemesi ve validation üzerinde neden/çözüm yoklaması | completed | mixed |
| [exp-020-original-questions-recap](#exp-020-original-questions-recap) | Özgün A/B/C/D eşik eğrileri ve altı bariyer dağılımı | completed | mixed |
| [exp-021-feature-comparison](#exp-021-feature-comparison) | A6 / B37 / C37 / D37: eksik volatilite kanallarını koruyan karşılaştırma | completed | mixed |
| [exp-022-barrier-economics](#exp-022-barrier-economics) | 2/5, 1/1 ve 2/2: validation sinyallerinin brüt getirileri | completed | mixed |
| [exp-023-barrier-economics-b12](#exp-023-barrier-economics-b12) | Pozitif model sinyallerinin getirileri: 1/2 bariyeri eklendi | completed | mixed |
| [exp-024-early-epoch-diagnostics](#exp-024-early-epoch-diagnostics) | A6/B37/C37/D37: erken epoch seçimi ve eğitim eğrilerinin neden analizi | completed | mixed |
| [exp-025-b37-learning-rate](#exp-025-b37-learning-rate) | B37 GRU: yalnız öğrenme hızı 0.001 → 0.0001 | completed | mixed |
| [exp-026-learning-rate-thresholds](#exp-026-learning-rate-thresholds) | B37 öğrenme hızları: validation eşik ve sinyal kapsamı | completed | mixed |
| [exp-027-a6-learning-rate](#exp-027-a6-learning-rate) | A6 GRU: öğrenme hızı 0.0001 ile eksik kontrol | completed | mixed |
| [exp-028-a6-thresholds](#exp-028-a6-thresholds) | A6 öğrenme hızları: eşik, eşit kapsam ve dönem kararlılığı | completed | mixed |
| [exp-029-a6-period-diagnosis](#exp-029-a6-period-diagnosis) | A6 fold28/37: train-validation dağılım ve etiket ilişkisi | completed | mixed |
| [exp-030-comprehensive-diagnosis](#exp-030-comprehensive-diagnosis) | 684 eğitim: epoch, eşik, dönem ve 37 girdi teşhisi | completed | mixed |
| [exp-031-checkpoint-selection](#exp-031-checkpoint-selection) | A6: seÃ§im ve deÄŸerlendirme ayrÄ±mÄ±yla BCE/AP checkpoint karÅŸÄ±laÅŸtÄ±rmasÄ± | completed | not_selected |
| [exp-032-cnn-gru](#exp-032-cnn-gru) | AltÄ± Ã¶zellik: GRU ve nedensel CNN ardÄ±ndan GRU | completed | not_selected |
| [exp-033-transfer-diagnosis](#exp-033-transfer-diagnosis) | GRU ve CNN-GRU seçimden değerlendirmeye aktarım teşhisi | completed | inconclusive |

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

## Kayıtlı sonuçlar · validation

A original38fold x3seed · equal fold/seed mean; fixed threshold0.5

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-020-original-questions-recap | — | — | 0.410499 | 0.096839 | — |

## Kayıtlı sonuçlar · validation

A; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-021-feature-comparison | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-021-feature-comparison | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

C; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-021-feature-comparison | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

D; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-021-feature-comparison | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B11; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-022-barrier-economics | — | — | — | — | — |
| exp-023-barrier-economics-b12 | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B22; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-022-barrier-economics | — | — | — | — | — |
| exp-023-barrier-economics-b12 | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B25; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-022-barrier-economics | — | — | — | — | — |
| exp-023-barrier-economics-b12 | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B12; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-023-barrier-economics-b12 | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

A; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-024-early-epoch-diagnostics | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

B; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-024-early-epoch-diagnostics | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

C; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-024-early-epoch-diagnostics | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

D; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-024-early-epoch-diagnostics | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

control · equal fold/seed means; 114 paired runs

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-025-b37-learning-rate | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

candidate · equal fold/seed means; 114 paired runs

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-025-b37-learning-rate | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

candidate threshold0.465; descriptive matched coverage · pooled fold/seed counts

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-026-learning-rate-thresholds | — | — | 0.446694 | 0.144691 | — |

## Kayıtlı sonuçlar · validation

A6 lr0.0001; 114 fold-seed runs · equal-run BCE/AP; pooled confusion counts at threshold0.5

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-027-a6-learning-rate | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

top51 per run; 114 runs each · equal-run precision; same count per run

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-028-a6-thresholds | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

fold28 versus fold37; candidate LR0.0001 · three-seed mean; feature shift mean over six inputs

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-029-a6-period-diagnosis | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

six conditions, 38 folds, 3 seeds · equal run means; counts not independent

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-030-comprehensive-diagnosis | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

114 matched A6 trajectories, 465 assessment targets each · Equal-run BCE/AP means; audit counts

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-031-checkpoint-selection | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

228 run, mimari başına114; bölüm başına465 assessment hedefi · AP/BCE eşit run ortalaması; precision toplam TP/sinyal

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-032-cnn-gru | — | — | — | — | — |

## Kayıtlı sonuçlar · validation

Exp032 aynı228 run; seçim/assessment465 hedef · 38 fold, her fold üç seed ortalaması

Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.

| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|
| exp-033-transfer-diagnosis | — | — | — | — | — |

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

## exp-019-root-cause-probes

**Eski proje incelemesi ve validation üzerinde neden/çözüm yoklaması**

Kalibrasyon, seed ortalaması ve geçmiş puan kantili istikrarsızlığın hangi bölümünü açıklıyor?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-018-validation-stability

**Yöntem:** {"adjacent_window_probe": "37 pairs x6 candidates,297 shared validation hours, old/new/mean comparisons", "assessment_rows": 507, "calibration_rows": 500, "changed_factor": "diagnostic-only post-processing probes; original GRU untouched", "channels": ["seed42", "seed43", "seed44", "equal_seed_mean"], "input_fingerprint": "03e1adfe0f87ffd151b1850cd71b1dab11a2fc3e208545090840692d11ba1b48", "methods": ["raw", "positive_sigmoid", "isotonic"], "new_gru_training": false, "purge_rows": 10, "seeds": [42, 43, 44], "test_evaluations": 0, "verified_prepared_sha256": "3792e9b687d086231588f4341b7fef80097a1f44c78dcf3073c201334b33f091"}

**Veri kimliği:** {"evaluation_scope": "existing historical validation only", "labels_id": "six-barriers-h10", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original-38fold; diagnostic 500/10/507 slices only"}

**Seçim kuralı:** Fixed probes, no final-test selection; late validation remains contaminated by earlier full-validation epoch selection, exploratory only.

**Karar / öğrenilen:** Verified feature drift and within-validation prevalence shift; B12 seed43 weak ranking precedes late drift. Calibration did not improve aggregate BCE in fixed pilot; equal seed averaging gives small gains but does not fix late fold37; adjacent-window averaging not a B12 solution. Old project had diagnostics/calibration/ensemble, not proof of solved stability. No production fix or test readiness claimed. Single-factor capacity pilot proposed but not run.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Existing epochs selected on full validation; late slice is exploratory, not independent holdout.
- All calibration conclusions restricted to specified500-row fits; not universal rejection.
- Feature/score associations are not causal attribution; GRU uses64-hour sequences.
- Overlapping labels/folds/seeds are dependent.
- No GRU checkpoint interventions or training; exact cause and reliable remedy remain unproven.
- Old project local snapshot differed and was excluded; only matched Drive B12 table used for feature diagnostics.

**Kanıt kopyaları:**
- [research/analyses/root-cause-20261017/PLAN.md](sources/e5f7fca25241fdd0b6a1581a2b497cd966a55ea00cb843370756042ac6f6907e.md) · SHA256 `e5f7fca25241fdd0b6a1581a2b497cd966a55ea00cb843370756042ac6f6907e`
- [research/analyses/root-cause-20261017/PLAN.md](sources/b8a746d886027e50db6de1b50f33cc11d0fe2c16ff9f32838656b6abef37a5e6.md) · SHA256 `b8a746d886027e50db6de1b50f33cc11d0fe2c16ff9f32838656b6abef37a5e6`
- [research/analyses/root-cause-20261017/REPORT.md](sources/cf33d99283b094f3850324f3bad150c699a2dda96e0c50be872cc6877cafa9e7.md) · SHA256 `cf33d99283b094f3850324f3bad150c699a2dda96e0c50be872cc6877cafa9e7`
- [research/analyses/root-cause-20261017/PROVENANCE.md](sources/6754274a168fd8655a82cfa8926bed774f808ebce4c486e96615e3f0ef95e795.md) · SHA256 `6754274a168fd8655a82cfa8926bed774f808ebce4c486e96615e3f0ef95e795`
- [research/analyses/root-cause-20261017/probe_summary.csv](sources/dc94f491a25c088d6d22251bb1e262de5fa2b82d551c1124ff3edfa32783570e.csv) · SHA256 `dc94f491a25c088d6d22251bb1e262de5fa2b82d551c1124ff3edfa32783570e`
- [research/analyses/root-cause-20261017/verified_feature_shift.csv](sources/7ffa30f1ed9801d2b716645798cd72614a457cbb7e90e17c9573dad1aadeb28d.csv) · SHA256 `7ffa30f1ed9801d2b716645798cd72614a457cbb7e90e17c9573dad1aadeb28d`
- [research/analyses/root-cause-20261017/within_validation_drift.csv](sources/9a6e526ecf7661fccd21d80b68cc6915a96c366909c1984f0025f130d0f6f81e.csv) · SHA256 `9a6e526ecf7661fccd21d80b68cc6915a96c366909c1984f0025f130d0f6f81e`
- [research/analyses/root-cause-20261017/epoch_objective_audit.csv](sources/b94633d2c70af77e59d7a9d4f2333c9789a42431c5c002fbd899339dbca5ac6e.csv) · SHA256 `b94633d2c70af77e59d7a9d4f2333c9789a42431c5c002fbd899339dbca5ac6e`
- [research/analyses/root-cause-20261017/adjacent_window_probe.csv](sources/d0f96ece70d81c49ef3903f62b29198199e68d59fe5cf95380fa3179ab6254de.csv) · SHA256 `d0f96ece70d81c49ef3903f62b29198199e68d59fe5cf95380fa3179ab6254de`
- [reports/root-cause-20261017/analysis-source.txt](sources/be02c3f82e2735b199593a2c0a75f7b2e12a7e387e935f373394093023782d84.txt) · SHA256 `be02c3f82e2735b199593a2c0a75f7b2e12a7e387e935f373394093023782d84`

[Son kayıt](events/000034.json) · revizyon 2 · Complete authorized root-cause diagnosis and fixed solution probes, including negative results and verified prepared-data drift.

## exp-020-original-questions-recap

**Özgün A/B/C/D eşik eğrileri ve altı bariyer dağılımı**

İlk iki teşhis sorusunun kapsamı, sonuçları ve sonraki eğitimlerden farkı nedir?

Kampanya: `campaign-002` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-011-threshold-diagnostics, exp-013-barrier-expansion, exp-016-selective-walk-forward, exp-019-root-cause-probes

**Yöntem:** {"barriers": ["2/5", "1/1", "1/2", "1.5/2", "2/2", "3/2"], "changed_factor": "reporting and existing-prediction threshold diagnostics only", "folds": 38, "models": ["A", "B", "C", "D"], "prediction_files": 456, "python": "3.13.7", "seeds": [42, 43, 44], "test_evaluations": 0, "training_runs": 0}

**Veri kimliği:** {"evaluation_scope": "validation predictions and development label distributions only", "labels_id": "original-ABCD-B25; existing-six-barriers-h10", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Betimsel validation eşik ızgarası 0:0.005:1; eşik seçilmedi, test okunmadı.

**Karar / öğrenilen:** A-only prior diagnosis extended to original B/C/D. Six existing label distributions and timeout returns verified and consolidated. Separate label diagnostics from later 684 training results; seed/period instability remains unresolved. No new training or model proposal executed.

**validation** · A original38fold x3seed · equal fold/seed mean; fixed threshold0.5

| Ölçüt | Kayıtlı değer |
|---|---:|
| f1 | 0.142418 |
| precision | 0.410499 |
| recall | 0.096839 |
| signal_rate | 0.062913 |

**Sınırlar / açık noktalar:**
- Epoch selection reused validation; curves are descriptive, not independent evaluation.
- Overlapping folds and seeds are dependent.
- Macro precision uses zero for empty groups for historical compatibility; active-only precision and empty counts supplied.
- A features are not a subset of B/C/D; not a pure architecture comparison.
- Full raw pipeline or model weights not re-audited.

**Kanıt kopyaları:**
- [research/analyses/question-recap-20261017/abcd_score_metrics.csv](sources/d8ce7d6fe9e9f345fbfd1e0f8abadf4a49d401044ad900159b213446ac752de0.csv) · SHA256 `d8ce7d6fe9e9f345fbfd1e0f8abadf4a49d401044ad900159b213446ac752de0`
- [research/analyses/question-recap-20261017/abcd_seed_curves.csv](sources/77d983cb692a789100e861a6a0cb304340366875e58398a751a84f9b324eb9c1.csv) · SHA256 `77d983cb692a789100e861a6a0cb304340366875e58398a751a84f9b324eb9c1`
- [research/analyses/question-recap-20261017/abcd_selected_thresholds.csv](sources/b77d37000aa025a6d6db17a9b3c879be9d49d9773d8192ac92e260caca4bc20c.csv) · SHA256 `b77d37000aa025a6d6db17a9b3c879be9d49d9773d8192ac92e260caca4bc20c`
- [research/analyses/question-recap-20261017/abcd_thresholds.csv](sources/8dbeb61996237275d654d72ee3e52c1af32a3899dd80291c62140bc9f29eda9d.csv) · SHA256 `8dbeb61996237275d654d72ee3e52c1af32a3899dd80291c62140bc9f29eda9d`
- [research/analyses/question-recap-20261017/analysis-source.txt](sources/d0c12ac640549f9c92db252b2c032c6d3b9db4f1d3e11981ff5974cce608d7b5.txt) · SHA256 `d0c12ac640549f9c92db252b2c032c6d3b9db4f1d3e11981ff5974cce608d7b5`
- [research/analyses/question-recap-20261017/input-manifest.txt](sources/e57522ceaec1c863f406465e5e425caf84feac1839e642439059eef10fbb8ee3.txt) · SHA256 `e57522ceaec1c863f406465e5e425caf84feac1839e642439059eef10fbb8ee3`
- [research/analyses/question-recap-20261017/output-manifest.txt](sources/28d3be1b7fe3fba16f8c7eab14ffdf152ab9673e3cc4974f96791b34bafdb0c7.txt) · SHA256 `28d3be1b7fe3fba16f8c7eab14ffdf152ab9673e3cc4974f96791b34bafdb0c7`
- [research/analyses/question-recap-20261017/PLAN.md](sources/2b61004aa59d2ac692af154a168f1a5414512379914534cf24733c3a1dfcfd0d.md) · SHA256 `2b61004aa59d2ac692af154a168f1a5414512379914534cf24733c3a1dfcfd0d`
- [research/analyses/question-recap-20261017/REPORT.md](sources/b741dbb3006f00d51099d8ffd14a48eb5915541638567eef274ddf9add5476ea.md) · SHA256 `b741dbb3006f00d51099d8ffd14a48eb5915541638567eef274ddf9add5476ea`
- [research/analyses/question-recap-20261017/six_barrier_counts.csv](sources/b408a20b116d15bb61b41db494ca9a1b466fc09d9978592e1d009c520baa9e67.csv) · SHA256 `b408a20b116d15bb61b41db494ca9a1b466fc09d9978592e1d009c520baa9e67`
- [research/analyses/question-recap-20261017/six_barrier_timeout_returns.csv](sources/ef9d0102b54145c2093ab6275361b4917829d8545f6fdab1d1580c759a2e2024.csv) · SHA256 `ef9d0102b54145c2093ab6275361b4917829d8545f6fdab1d1580c759a2e2024`

[Son kayıt](events/000035.json) · revizyon 1 · Complete original four-model threshold diagnostics and consolidate six existing barrier distributions; no training/test.

## exp-021-feature-comparison

**A6 / B37 / C37 / D37: eksik volatilite kanallarını koruyan karşılaştırma**

A özelliklerini içeren37 girdiyle GRU/TCN/hibrit nasıl karşılaştırılır; aynı GRU içinde6→37 özellik etkisi nedir?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-001-a, exp-002-b, exp-003-c, exp-004-d, exp-020-original-questions-recap

**Yöntem:** {"architectures": ["gru", "gru", "tcn", "tcn_gru"], "changed_factor": "B/C/D34→37; original6 inputs preserved as subset", "feature_counts": [6, 37, 37, 37], "hardware": "NVIDIA A100-SXM4-40GB", "original_engine_unchanged": true, "seeds": [42, 43, 44], "training_runs_planned": 456}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Original min-validation-BCE epoch rule; four candidates compared by macro validation BCE; threshold curves descriptive, no automatic threshold.

**Karar / öğrenilen:** Drive reports confirm A6/B37/C37/D37 completed. A still leads mean validation BCE/AP in all three seeds; richer models have higher AP in the last fold. No retraining or new method authorized.

**validation** · A; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap | 0.421212 |
| bce | 0.594332 |
| mean_best_epoch | 4.438596 |

**validation** · B; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap | 0.404929 |
| bce | 0.609470 |
| mean_best_epoch | 1.368421 |

**validation** · C; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap | 0.409587 |
| bce | 0.602906 |
| mean_best_epoch | 1.500000 |

**validation** · D; 38 folds x 3 seeds; A6/B37/C37/D37 · equal fold/seed BCE and AP means

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap | 0.411476 |
| bce | 0.601671 |
| mean_best_epoch | 1.482456 |

**Sınırlar / açık noktalar:**
- A vs C/D changes both inputs and architecture; do not claim pure architecture effect.
- Parameter budgets differ; no universal architecture ranking.
- Validation reused for epoch selection; folds/seeds dependent.
- Drive CSVs reviewed; checkpoints, raw predictions and all histories not independently re-audited.

**Kanıt kopyaları:**
- [research/analyses/feature-comparison-20261018/PLAN.md](sources/93b69d9f5915d4f4b5c708b400d3472bed449c23f5aff10cbc0a7110d4637ed1.md) · SHA256 `93b69d9f5915d4f4b5c708b400d3472bed449c23f5aff10cbc0a7110d4637ed1`
- [research/analyses/feature-comparison-review-20261024/REPORT.md](sources/7ffe7971dd8aeb94e94d4661b8460e3e510a01be758d10f419c6a985983b470f.md) · SHA256 `7ffe7971dd8aeb94e94d4661b8460e3e510a01be758d10f419c6a985983b470f`
- [research/analyses/feature-comparison-review-20261024/summary_at_050.csv](sources/9fb9b65172b341411cdf78d8ef792ae40e4986b53fb46355cf3f4db33a76a390.csv) · SHA256 `9fb9b65172b341411cdf78d8ef792ae40e4986b53fb46355cf3f4db33a76a390`
- [research/analyses/feature-comparison-review-20261024/paired_differences.csv](sources/45c23b6c183cdbd5f4adb6dfb886d64803895632f61a6041ac5781f59979030a.csv) · SHA256 `45c23b6c183cdbd5f4adb6dfb886d64803895632f61a6041ac5781f59979030a`
- [research/analyses/feature-comparison-review-20261024/metrics_by_fold_seed.csv](sources/ee41d73ba8413799b7f55f08f424ded15e4edf4037c13adf37131d3e9f143fe7.csv) · SHA256 `ee41d73ba8413799b7f55f08f424ded15e4edf4037c13adf37131d3e9f143fe7`
- [research/analyses/feature-comparison-review-20261024/drive_sources.json](sources/4e9fe3cc8cecbb693db9277380fe2d352e60cbf863c68540308740e15607b942.json) · SHA256 `4e9fe3cc8cecbb693db9277380fe2d352e60cbf863c68540308740e15607b942`

[Son kayıt](events/000039.json) · revizyon 2 · Correct stale planned status using completed Drive reports; user confirms comparison already run.

## exp-022-barrier-economics

**2/5, 1/1 ve 2/2: validation sinyallerinin brüt getirileri**

Başlangıç 2/5 oranının gerekçesi var mı; farklı eşiklerde sinyallerin ekonomik anlamı ve dönem kararlılığı nasıl?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-018-validation-stability, exp-020-original-questions-recap

**Yöntem:** {"architecture": "A6 GRU", "candidates": ["B25", "B11", "B22"], "costs": "excluded", "final_test": false, "folds": 38, "new_training": false, "primary_aggregation": "latest validation fold per timestamp within each seed; equal seed means", "secondary_aggregation": "equal active fold/seed groups", "seeds": [42, 43, 44], "threshold_grid": "0..1 by 0.01"}

**Veri kimliği:** {"evaluation_scope": "archived validation predictions only; unique hours per seed 27657", "labels_id": "tp2-sl5 / tp1-sl1 / tp2-sl2 h10 stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Descriptive fixed grid, 0.5 reference; no barrier or threshold selected.

**Karar / öğrenilen:** No documented special rationale for 2/5 found. Positive overall gross signal returns coexist with weak last-fold performance and aggregation sensitivity; no winner or final test.

**validation** · B11; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.025652 |
| exit_mean_pct | 0.021630 |
| exit_win_pct | 51.655844 |
| h10_mean_pct | 0.102521 |
| signals_mean | 5620.333333 |

**validation** · B22; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.089544 |
| exit_mean_pct | 0.104621 |
| exit_win_pct | 53.233718 |
| h10_mean_pct | 0.259635 |
| signals_mean | 537.000000 |

**validation** · B25; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.069185 |
| exit_mean_pct | 0.102237 |
| exit_win_pct | 60.813218 |
| h10_mean_pct | 0.210427 |
| signals_mean | 1646.666667 |

**Sınırlar / açık noktalar:**
- Epoch selection reused validation; not independent evaluation.
- Overlapping hypothetical hourly positions, no portfolio simulation or costs.
- Seed averages are not independent samples; high thresholds have few signals.
- Primary aggregation differs from historical equal-fold means; both reported.

**Kanıt kopyaları:**
- [research/analyses/barrier-economics-20261022/PLAN.md](sources/eb4750b6e8d12314d63d3a082c2cb71faaa9409f4e043e4c2b3a859ac701e1fb.md) · SHA256 `eb4750b6e8d12314d63d3a082c2cb71faaa9409f4e043e4c2b3a859ac701e1fb`
- [research/analyses/barrier-economics-20261022/LITERATURE.md](sources/54dff36d0700d2ef30281085c25a7bdf5ad8ccec43bc0310cc0ba0a0daa93214.md) · SHA256 `54dff36d0700d2ef30281085c25a7bdf5ad8ccec43bc0310cc0ba0a0daa93214`
- [research/analyses/barrier-economics-20261022/REPORT.md](sources/706e27414f8369ab2bb47e6fcd4c2468f5579ca1fc57bc80a35d0cd1ebd0a456.md) · SHA256 `706e27414f8369ab2bb47e6fcd4c2468f5579ca1fc57bc80a35d0cd1ebd0a456`
- [research/analyses/barrier-economics-20261022/selected_thresholds.csv](sources/8d95b7f865bb83562eb945f857cf127369743dc5b8505272fc02d9929a1db9b8.csv) · SHA256 `8d95b7f865bb83562eb945f857cf127369743dc5b8505272fc02d9929a1db9b8`
- [research/analyses/barrier-economics-20261022/fold_macro_threshold05.csv](sources/920b2ec801b9df25bbbf2af9618196f5c7bf72b6454edc389ef179e83b7017aa.csv) · SHA256 `920b2ec801b9df25bbbf2af9618196f5c7bf72b6454edc389ef179e83b7017aa`
- [research/analyses/barrier-economics-20261022/last_fold_threshold05.csv](sources/491d848213f6362c94b8a1cb72ce5599948d0788c4378512692d9c258250c253.csv) · SHA256 `491d848213f6362c94b8a1cb72ce5599948d0788c4378512692d9c258250c253`
- [research/analyses/barrier-economics-20261022/input_manifest.json](sources/2b99953ab813c5a2e41254b3fa70450e10bf2576b0226d04b612f881f0a48585.json) · SHA256 `2b99953ab813c5a2e41254b3fa70450e10bf2576b0226d04b612f881f0a48585`
- [research/analyses/barrier-economics-20261022/checks.json](sources/db19147660b34af13acb5de62f4d525a571235330c0d98e635631dbb4f63126c.json) · SHA256 `db19147660b34af13acb5de62f4d525a571235330c0d98e635631dbb4f63126c`
- [research/analyses/barrier-economics-20261022/output_manifest.json](sources/8471f1e5f7ac729d95c9a9f3cc6b7d03f068aeb971060b793edc63ee7a1ebfd0.json) · SHA256 `8471f1e5f7ac729d95c9a9f3cc6b7d03f068aeb971060b793edc63ee7a1ebfd0`

[Son kayıt](events/000037.json) · revizyon 1 · Complete requested literature and archived-validation economic diagnostics without training or final test.

## exp-023-barrier-economics-b12

**Pozitif model sinyallerinin getirileri: 1/2 bariyeri eklendi**

Pozitif model sinyallerinin gerçekleşen getirileri 1/2 bariyerinde nasıl değişiyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-022-barrier-economics

**Yöntem:** {"architecture": "A6 GRU", "candidates": ["B25", "B11", "B22", "B12"], "costs": "excluded", "final_test": false, "folds": 38, "new_training": false, "primary_aggregation": "latest validation fold per timestamp within each seed; equal seed means", "secondary_aggregation": "equal active fold/seed groups", "seeds": [42, 43, 44], "threshold_grid": "0..1 by 0.01"}

**Veri kimliği:** {"evaluation_scope": "archived validation predictions only; unique hours per seed 27657", "labels_id": "tp2-sl5 / tp1-sl1 / tp2-sl2 h10 stop-first / tp1-sl2 h10 stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Descriptive fixed grid, 0.5 reference; no barrier or threshold selected.

**Karar / öğrenilen:** B12 added with identical validation methodology. Overall positive mean returns coexist with negative last-fold returns in all seeds at 0.50; no threshold or barrier selected.

**validation** · B11; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.025652 |
| exit_mean_pct | 0.021630 |
| exit_win_pct | 51.655844 |
| h10_mean_pct | 0.102521 |
| signals_mean | 5620.333333 |

**validation** · B12; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.016141 |
| exit_mean_pct | 0.028749 |
| exit_win_pct | 63.549758 |
| h10_mean_pct | 0.095957 |
| signals_mean | 20716.333333 |

**validation** · B22; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.089544 |
| exit_mean_pct | 0.104621 |
| exit_win_pct | 53.233718 |
| h10_mean_pct | 0.259635 |
| signals_mean | 537.000000 |

**validation** · B25; 27657 hours/seed; threshold 0.50 · equal seed means after timestamp deduplication

| Ölçüt | Kayıtlı değer |
|---|---:|
| exit_lift_pp | 0.069185 |
| exit_mean_pct | 0.102237 |
| exit_win_pct | 60.813218 |
| h10_mean_pct | 0.210427 |
| signals_mean | 1646.666667 |

**Sınırlar / açık noktalar:**
- Epoch selection reused validation; not independent evaluation.
- Overlapping hypothetical hourly positions, no portfolio simulation or costs.
- Seed averages are not independent samples; high thresholds have few signals.
- Primary aggregation differs from historical equal-fold means; both reported.

**Kanıt kopyaları:**
- [research/analyses/barrier-economics-20261023/PLAN.md](sources/9ff3ae7ed3c46da1ffc138e84da3e7f29ad2903930caeb2a195013b3d262ae65.md) · SHA256 `9ff3ae7ed3c46da1ffc138e84da3e7f29ad2903930caeb2a195013b3d262ae65`
- [research/analyses/barrier-economics-20261023/REPORT.md](sources/0c32b97ae78bc83dddec1c22ec4a37d07932ecebca315f7d20230a3b8289b96b.md) · SHA256 `0c32b97ae78bc83dddec1c22ec4a37d07932ecebca315f7d20230a3b8289b96b`
- [research/analyses/barrier-economics-20261023/selected_thresholds.csv](sources/199cf6674f904902a571a8e460d25bf209bc8d0787b2340678e20bb5dbf73930.csv) · SHA256 `199cf6674f904902a571a8e460d25bf209bc8d0787b2340678e20bb5dbf73930`
- [research/analyses/barrier-economics-20261023/fold_macro_threshold05.csv](sources/c593f125db84ad9603c3231d63f37ebeaaaeac03a6e30bf81acf5ad9be92c6ac.csv) · SHA256 `c593f125db84ad9603c3231d63f37ebeaaaeac03a6e30bf81acf5ad9be92c6ac`
- [research/analyses/barrier-economics-20261023/last_fold_threshold05.csv](sources/ad9cd041fa76ca7165a77294c8888b2fca6c87c5ab70b5fd09979a584491e5ef.csv) · SHA256 `ad9cd041fa76ca7165a77294c8888b2fca6c87c5ab70b5fd09979a584491e5ef`
- [research/analyses/barrier-economics-20261023/input_manifest.json](sources/81b241c22da7d039384763a8a14fff36fbd2738da2227f3cc57629e2146205fa.json) · SHA256 `81b241c22da7d039384763a8a14fff36fbd2738da2227f3cc57629e2146205fa`
- [research/analyses/barrier-economics-20261023/checks.json](sources/459fec04cac7f351c590e984eb9fd88fee58e26bba6be477ca17f0669cdb1dc4.json) · SHA256 `459fec04cac7f351c590e984eb9fd88fee58e26bba6be477ca17f0669cdb1dc4`
- [research/analyses/barrier-economics-20261023/output_manifest.json](sources/46615414d18a9c9cb96e1c682fee72ae20252809b8e18449ca19aa3dcf3cfd8c.json) · SHA256 `46615414d18a9c9cb96e1c682fee72ae20252809b8e18449ca19aa3dcf3cfd8c`

[Son kayıt](events/000038.json) · revizyon 1 · Add B12 to requested positive-signal return diagnostics; preserve previous three candidates exactly.

## exp-024-early-epoch-diagnostics

**A6/B37/C37/D37: erken epoch seçimi ve eğitim eğrilerinin neden analizi**

En iyi validation BCE neden ilk epochlarda; model, seed ve dönem boyunca train BCE ve validation AP nasıl değişiyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-021-feature-comparison

**Yöntem:** {"changed_factor": null, "common_epochs": [1, 16], "scope": "read-only analysis of 456 existing histories", "source_release": "advisor-feature-comparison-v1.0.0", "training_or_test_started": false}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Original minimum validation BCE unchanged; descriptive equal fold/seed summaries; no new threshold or checkpoint selection.

**Karar / öğrenilen:** Strong overfitting-compatible pattern, especially in 37-input models; selection records consistent. Learning-rate, feature and drift causes not isolated. Propose single-factor learning-rate comparison, not executed.

**validation** · A; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_down_first_to16 | 80.000000 |
| best_epoch_1 | 17.000000 |
| best_epoch_le3 | 56.000000 |
| best_epoch_mean | 4.438596 |
| epoch16_average_precision | 0.382020 |
| epoch16_bce | 0.699519 |
| first_average_precision | 0.404281 |
| first_bce | 0.609349 |
| runs | 114.000000 |
| train_down_val_up_first_to16 | 111.000000 |

**validation** · B; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_down_first_to16 | 88.000000 |
| best_epoch_1 | 88.000000 |
| best_epoch_le3 | 110.000000 |
| best_epoch_mean | 1.368421 |
| epoch16_average_precision | 0.358819 |
| epoch16_bce | 1.503299 |
| first_average_precision | 0.399854 |
| first_bce | 0.611985 |
| runs | 114.000000 |
| train_down_val_up_first_to16 | 114.000000 |

**validation** · C; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_down_first_to16 | 74.000000 |
| best_epoch_1 | 68.000000 |
| best_epoch_le3 | 112.000000 |
| best_epoch_mean | 1.500000 |
| epoch16_average_precision | 0.376726 |
| epoch16_bce | 1.391687 |
| first_average_precision | 0.397324 |
| first_bce | 0.607570 |
| runs | 114.000000 |
| train_down_val_up_first_to16 | 114.000000 |

**validation** · D; 38 folds x 3 seeds · equal fold/seed means and descriptive counts; fixed epoch 1 vs 16

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_down_first_to16 | 82.000000 |
| best_epoch_1 | 71.000000 |
| best_epoch_le3 | 112.000000 |
| best_epoch_mean | 1.482456 |
| epoch16_average_precision | 0.368116 |
| epoch16_bce | 1.743814 |
| first_average_precision | 0.402457 |
| first_bce | 0.607968 |
| runs | 114.000000 |
| train_down_val_up_first_to16 | 114.000000 |

**Sınırlar / açık noktalar:**
- Validation reused for epoch selection; folds and seeds dependent.
- No epochwise raw scores, gradient norms or train eval losses.
- No checkpoint loading or raw feature/label recomputation.
- Train loss measured during updates/dropout; validation at epoch end/eval.
- No verified remedy; new experiment requires explicit authorization.

**Kanıt kopyaları:**
- [research/analyses/early-epochs-20261024/PLAN.md](sources/038e1ed37669e16539d0f53655079546bbaa8344e2d0dee5e65850c04878a633.md) · SHA256 `038e1ed37669e16539d0f53655079546bbaa8344e2d0dee5e65850c04878a633`
- [research/analyses/early-epochs-20261024/REPORT.md](sources/9b3db00ee23ff82859c4f9ce6b1e65fae763eedf820deaa89e1fe3ee5a626b51.md) · SHA256 `9b3db00ee23ff82859c4f9ce6b1e65fae763eedf820deaa89e1fe3ee5a626b51`
- [research/analyses/early-epochs-20261024/model_summary.csv](sources/2bc0489fc132aa0247b672093536c250e0e5bb8e1d59e4ff7ef771fd78b237d7.csv) · SHA256 `2bc0489fc132aa0247b672093536c250e0e5bb8e1d59e4ff7ef771fd78b237d7`
- [research/analyses/early-epochs-20261024/run_diagnostics.csv](sources/664796599e0966341800613d0df94cc190306330e162f47a4216b2e91567adf9.csv) · SHA256 `664796599e0966341800613d0df94cc190306330e162f47a4216b2e91567adf9`
- [research/analyses/early-epochs-20261024/input_manifest.json](sources/b8e0eb846e09b25e13b2c3dedc83d425d8d1dd6f75527e235d67e5b74aeadf69.json) · SHA256 `b8e0eb846e09b25e13b2c3dedc83d425d8d1dd6f75527e235d67e5b74aeadf69`
- [research/analyses/early-epochs-20261024/checks.json](sources/b72f905a313794badb0f4070d6f81bfb57b17c8d7195a15bae8beb9a96f5a49b.json) · SHA256 `b72f905a313794badb0f4070d6f81bfb57b17c8d7195a15bae8beb9a96f5a49b`
- [research/analyses/early-epochs-20261024/output_manifest.json](sources/3336c5706f5914bc2ec68c3a6baaaefa63f1a88c9cec4fea3426b12a2984c7ea.json) · SHA256 `3336c5706f5914bc2ec68c3a6baaaefa63f1a88c9cec4fea3426b12a2984c7ea`

[Son kayıt](events/000040.json) · revizyon 1 · Audit existing histories; distinguish observed overfitting from unproven causes; no new training or test.

## exp-025-b37-learning-rate

**B37 GRU: yalnız öğrenme hızı 0.001 → 0.0001**

Düşük öğrenme hızı validation BCE/AP ve seed kararlılığını iyileştiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-021-feature-comparison, exp-024-early-epoch-diagnostics

**Yöntem:** {"changed_factor": "learning_rate 0.001 -> 0.0001", "control_reused": true, "folds": 38, "new_training_runs": 114, "release": "advisor-learning-rate-v1.0.0", "seeds": [42, 43, 44]}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Original minimum validation BCE; fixed 0.5 descriptive threshold; no final test.

**Karar / öğrenilen:** Lower learning rate improves selected BCE modestly and AP slightly, reduces seed metric spread, but overfitting and zero-signal behavior persist; no final test or threshold selected.

**validation** · control · equal fold/seed means; 114 paired runs

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_falls_best_to_last | 94.000000 |
| ap_mean | 0.404929 |
| bce_mean | 0.609470 |
| best_epoch_le3 | 110.000000 |
| best_epoch_max | 5.000000 |
| best_epoch_median | 1.000000 |
| epoch16_ap_mean | 0.358819 |
| epoch16_bce_mean | 1.503299 |
| epochs_max | 20.000000 |
| epochs_min | 16.000000 |
| last_ap_mean | 0.357630 |
| last_bce_mean | 1.522554 |
| median_seed_range_ap | 0.031145 |
| median_seed_range_bce | 0.012970 |
| no_signal_runs | 1.000000 |
| pooled_f1 | 0.214006 |
| pooled_precision | 0.447450 |
| pooled_recall | 0.140635 |
| train_falls_val_rises | 114.000000 |

**validation** · candidate · equal fold/seed means; 114 paired runs

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_falls_best_to_last | 76.000000 |
| ap_mean | 0.410256 |
| bce_mean | 0.601146 |
| best_epoch_le3 | 68.000000 |
| best_epoch_max | 22.000000 |
| best_epoch_median | 3.000000 |
| epoch16_ap_mean | 0.390261 |
| epoch16_bce_mean | 0.640668 |
| epochs_max | 37.000000 |
| epochs_min | 16.000000 |
| last_ap_mean | 0.387084 |
| last_bce_mean | 0.656657 |
| median_seed_range_ap | 0.023631 |
| median_seed_range_bce | 0.006745 |
| no_signal_runs | 23.000000 |
| pooled_f1 | 0.156436 |
| pooled_precision | 0.463465 |
| pooled_recall | 0.094099 |
| train_falls_val_rises | 114.000000 |

**Sınırlar / açık noktalar:**
- Validation reused for epoch selection; overlapping folds.
- Patience 15 and epoch budget 100 unchanged.
- Four focused checks passed; no Colab training performed.
- Weights not included; no inference rerun.
- Macro precision includes zero-signal groups; pooled counts also reported explicitly.

**Kanıt kopyaları:**
- [research/analyses/learning-rate-20261024/PLAN.md](sources/7d7fc826fa31a971892154fdc917f134b51bf2719be539b718a2f38f883ca9b0.md) · SHA256 `7d7fc826fa31a971892154fdc917f134b51bf2719be539b718a2f38f883ca9b0`
- [research/analyses/learning-rate-review-20261024/REPORT.md](sources/087b879122ad50d4b1668bc63ef17abdd36a41221de90e91e8119bb731fe2cb8.md) · SHA256 `087b879122ad50d4b1668bc63ef17abdd36a41221de90e91e8119bb731fe2cb8`
- [research/analyses/learning-rate-review-20261024/checks.json](sources/9c3b095a1777fe736fd57e47fbfb12bf11d99f42413994c0deadffb28faf995a.json) · SHA256 `9c3b095a1777fe736fd57e47fbfb12bf11d99f42413994c0deadffb28faf995a`
- [research/analyses/learning-rate-review-20261024/summary.csv](sources/fb44f7dfccefcd383fdbc6e8e05eb9cf65857c9addb0de11e0807c1eb4262afd.csv) · SHA256 `fb44f7dfccefcd383fdbc6e8e05eb9cf65857c9addb0de11e0807c1eb4262afd`
- [research/analyses/learning-rate-review-20261024/paired.csv](sources/6192a383cc91ed2aa727de289ace884f844e5ac5125256f347c4d82b108eb38d.csv) · SHA256 `6192a383cc91ed2aa727de289ace884f844e5ac5125256f347c4d82b108eb38d`
- [research/analyses/learning-rate-review-20261024/seed_summary.csv](sources/59f49f83a4888dbad957eea038633d37d8975bdfa9d5194b00ddfd63ae440e61.csv) · SHA256 `59f49f83a4888dbad957eea038633d37d8975bdfa9d5194b00ddfd63ae440e61`
- [research/analyses/learning-rate-review-20261024/audit_by_run.csv](sources/3b739a1f8861b151b3fd8ca830ef552439a28dd491a8e27ed91413338492fa5d.csv) · SHA256 `3b739a1f8861b151b3fd8ca830ef552439a28dd491a8e27ed91413338492fa5d`

[Son kayıt](events/000042.json) · revizyon 2 · Review user-completed Colab ZIP; verify 114 paired runs against original control evidence.

## exp-026-learning-rate-thresholds

**B37 öğrenme hızları: validation eşik ve sinyal kapsamı**

Düşük hızda skor dağılımı ve eşik değişimi seçiciliği nasıl etkiliyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-025-b37-learning-rate

**Yöntem:** {"aggregation": "pooled confusion counts over fold/seed prediction instances; no deduplication", "coverage_match": "nearest candidate signal rate to control threshold0.5; descriptive only", "scope": "existing validation predictions only", "threshold_grid": "0..1 step0.005"}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** No threshold selected; original min-BCE epoch weights unchanged.

**Karar / öğrenilen:** Upper scores contract; at comparable coverage precision is similar. High precision is supported by few records and sparse folds. No final test or new training.

**validation** · candidate threshold0.465; descriptive matched coverage · pooled fold/seed counts

| Ölçüt | Kayıtlı değer |
|---|---:|
| empty_runs | 9.000000 |
| precision | 0.446694 |
| recall | 0.144691 |
| signal_rate | 0.100562 |

**Sınırlar / açık noktalar:**
- Validation reused for epoch selection and descriptive threshold inspection.
- Overlapping folds/seeds are not independent trades.
- No threshold or new feature group authorized by this report.

**Kanıt kopyaları:**
- [research/analyses/learning-rate-thresholds-20261024/REPORT.md](sources/9dd516fb8609e0f77574196e862a2ca6dfe5891de10273dfcb62b6fe2919cfda.md) · SHA256 `9dd516fb8609e0f77574196e862a2ca6dfe5891de10273dfcb62b6fe2919cfda`
- [research/analyses/learning-rate-thresholds-20261024/checks.json](sources/7825da588be2a343d2bfcd6b0e5e193031d07da9689f729cfe895d98050f4b8c.json) · SHA256 `7825da588be2a343d2bfcd6b0e5e193031d07da9689f729cfe895d98050f4b8c`
- [research/analyses/learning-rate-thresholds-20261024/selected_thresholds.csv](sources/115581707d14100c8b46ee6e265e2ceb47e5f2bb9cb07dfde6c7824b72b7e301.csv) · SHA256 `115581707d14100c8b46ee6e265e2ceb47e5f2bb9cb07dfde6c7824b72b7e301`

[Son kayıt](events/000043.json) · revizyon 1 · User authorized descriptive threshold comparison using existing predictions.

## exp-027-a6-learning-rate

**A6 GRU: öğrenme hızı 0.0001 ile eksik kontrol**

Düşük hız A6 modelini de geliştiriyor mu; aynı hızda A6/B37 karşılaştırması nasıl değişiyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-021-feature-comparison, exp-025-b37-learning-rate, exp-026-learning-rate-thresholds

**Yöntem:** {"changed_factor": "learning_rate 0.001 -> 0.0001", "control_reused": true, "experiment": "A", "folds": 38, "new_training_runs": 114, "release": "advisor-learning-rate-v1.1.0", "seeds": [42, 43, 44]}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Original minimum validation BCE; fixed 0.5 descriptive threshold; no final test.

**Karar / öğrenilen:** A6 low LR reduces seed spread and delays deterioration but does not improve selected validation BCE/AP; zero-signal runs rise 14 to 35. Preserve original reference; no final test.

**validation** · A6 lr0.0001; 114 fold-seed runs · equal-run BCE/AP; pooled confusion counts at threshold0.5

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_mean | 0.419869 |
| bce_mean | 0.594545 |
| median_seed_range_ap | 0.013485 |
| median_seed_range_bce | 0.003653 |
| no_signal_runs | 35.000000 |
| pooled_f1 | 0.123988 |
| pooled_precision | 0.485573 |
| pooled_recall | 0.071067 |

**Sınırlar / açık noktalar:**
- Reused validation and overlapping folds/seeds; not independent final performance.
- Two runs reached 100-epoch cap.
- Review ZIP excludes weights; checkpoint files/inference not reverified.

**Kanıt kopyaları:**
- [research/analyses/a6-learning-rate-20261028/PLAN.md](sources/54dc894275e552b3d42744716ba2ba101a0f47cb51a8214bc726d7cd0231526e.md) · SHA256 `54dc894275e552b3d42744716ba2ba101a0f47cb51a8214bc726d7cd0231526e`
- [research/analyses/a6-learning-rate-20261028/REPORT.md](sources/0a8867647fb83f48d01822a654fe283d8d65c66af688a6bd44979545cc7a9f2a.md) · SHA256 `0a8867647fb83f48d01822a654fe283d8d65c66af688a6bd44979545cc7a9f2a`
- [research/analyses/a6-learning-rate-20261028/checks.json](sources/beaa6b6f5bcbcb6efa13e2b19dade401be5552c9a1353b3cbf7c16aa66f07f4c.json) · SHA256 `beaa6b6f5bcbcb6efa13e2b19dade401be5552c9a1353b3cbf7c16aa66f07f4c`

[Son kayıt](events/000045.json) · revizyon 2 · Audit user-completed A6 low-LR Drive results; all 114 validation runs complete.

## exp-028-a6-thresholds

**A6 öğrenme hızları: eşik, eşit kapsam ve dönem kararlılığı**

Düşük hızda sinyal kaybı skor ölçeği mi, sıralama kalitesi mi; aynı sinyal oranında ne değişiyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-027-a6-learning-rate, exp-026-learning-rate-thresholds

**Yöntem:** {"aggregation": "pooled fold/seed confusion counts; no deduplication or ensemble", "global_match": "nearest signal rate; no label optimization", "threshold_grid": "0..1 step0.005", "within_run_match": "top 1/2/5/10/20 percent; rounded counts; retrospective diagnostic"}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Original min-validation-BCE checkpoints unchanged; no threshold selected.

**Karar / öğrenilen:** Upper scores contract; matched coverage shows no consistent low-LR precision advantage. Last fold retains ranking below 0.5; fold28 ranking deteriorates. Keep original A6 reference; no final test.

**validation** · top51 per run; 114 runs each · equal-run precision; same count per run

| Ölçüt | Kayıtlı değer |
|---|---:|
| candidate_better_pairs | 53.000000 |
| candidate_precision | 0.462504 |
| control_better_pairs | 54.000000 |
| control_precision | 0.473168 |
| tied_pairs | 7.000000 |

**Sınırlar / açık noktalar:**
- Reused validation; overlapping folds and repeated seeds are not independent trades.
- Retrospective top-k cutoffs are not prospective trading rules.
- High-threshold precision has sparse support; no economic or significance claim.

**Kanıt kopyaları:**
- [research/analyses/a6-thresholds-20261028/REPORT.md](sources/012228e4b07377c6f4abe272b79acf01552e3fe1c01a1a13bfdfb023c9424846.md) · SHA256 `012228e4b07377c6f4abe272b79acf01552e3fe1c01a1a13bfdfb023c9424846`
- [research/analyses/a6-thresholds-20261028/checks.json](sources/b17cff39a00ef8aa792cff51f4e874b7a237e9c0950feaa5ca7abb9ec09b33c0.json) · SHA256 `b17cff39a00ef8aa792cff51f4e874b7a237e9c0950feaa5ca7abb9ec09b33c0`
- [research/analyses/a6-thresholds-20261028/matched_summary.csv](sources/517fdfbc82acf088b3cb44f53731ae8ba1b7d18efa317b6685076951d6a4c8f4.csv) · SHA256 `517fdfbc82acf088b3cb44f53731ae8ba1b7d18efa317b6685076951d6a4c8f4`

[Son kayıt](events/000046.json) · revizyon 1 · User authorized detailed A6 threshold and matched-coverage diagnosis on existing predictions.

## exp-029-a6-period-diagnosis

**A6 fold28/37: train-validation dağılım ve etiket ilişkisi**

Fold28 ve37 farkını etiket oranı, mevcut altı özellik dağılımı ve epoch geçmişleri açıklıyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-028-a6-thresholds

**Yöntem:** {"associations": "marginal Spearman; descriptive only", "distribution": "Wasserstein/train IQR, KS, tail rates; unweighted input rows", "epoch_review": "existing fold28/37 histories; no checkpoint replacement", "labels": "sequence endpoints only", "scope": "38 train/validation folds; six existing inputs; no test or training"}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Unchanged minimum validation BCE; no new rule.

**Karar / öğrenilen:** Marginal shift and TP-rate drop alone do not explain failure. Fold28 volatility-label associations weaken and BCE/AP epoch preferences diverge. Audit all histories before any selection-rule change.

**validation** · fold28 versus fold37; candidate LR0.0001 · three-seed mean; feature shift mean over six inputs

| Ölçüt | Kayıtlı değer |
|---|---:|
| fold28_mean_shift | 0.126100 |
| fold28_top5_precision | 0.104575 |
| fold37_mean_shift | 0.479200 |
| fold37_top5_precision | 0.503268 |

**Sınırlar / açık noktalar:**
- Reused validation and overlapping folds; focus periods chosen after outcomes.
- Marginal feature associations are not GRU attribution or causal proof.
- No alternate-epoch predictions available; no new inference.

**Kanıt kopyaları:**
- [research/analyses/a6-period-diagnosis-20261028/REPORT.md](sources/38106917d79c19e8b02f2256875013e2304aedb9165f92f6abd05f5a026e580e.md) · SHA256 `38106917d79c19e8b02f2256875013e2304aedb9165f92f6abd05f5a026e580e`
- [research/analyses/a6-period-diagnosis-20261028/checks.json](sources/b6c873ba9e50b3285ff52b77e6a31f7f09312300dbdb43a9c1eb37d928a6e610.json) · SHA256 `b6c873ba9e50b3285ff52b77e6a31f7f09312300dbdb43a9c1eb37d928a6e610`
- [research/analyses/a6-period-diagnosis-20261028/epoch_tradeoff.csv](sources/22e8a843da347e46b38237085784705661984cb7cc177cb781e7bfc2aff49e4a.csv) · SHA256 `22e8a843da347e46b38237085784705661984cb7cc177cb781e7bfc2aff49e4a`

[Son kayıt](events/000047.json) · revizyon 1 · User authorized existing-feature train/validation diagnosis; identities verified against frozen frame.

## exp-030-comprehensive-diagnosis

**684 eğitim: epoch, eşik, dönem ve 37 girdi teşhisi**

Mevcut karşılaştırılabilir bütün eğitimlerde seçim ölçütü, dönem ve girdi teşhisleri ne gösteriyor?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **mixed**

Önceki kayıtlar: exp-029-a6-period-diagnosis, exp-027-a6-learning-rate, exp-025-b37-learning-rate, exp-021-feature-comparison

**Yöntem:** {"conditions": 6, "context": "all37 marginal shifts and associations, sparse inputs explicitly undefined when needed", "features_audited": 37, "folds": 38, "runs": 684, "scope": "existing train/validation artifacts; retrospective epoch logs; no new training or test", "seeds": [42, 43, 44], "thresholds": "0.30..0.70 step0.05", "topk": "1/2/5/10/20 percent per run; diagnostic only"}

**Veri kimliği:** {"evaluation_scope": "validation only; no test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Unchanged min-validation-BCE weights; no new threshold or checkpoint rule.

**Karar / öğrenilen:** No consistent low-LR gain in equal-coverage precision; widespread retrospective BCE/AP divergence; period effects persist. Marginal input shifts/association changes do not provide a general cause. Sparse whale flags recorded without removal.

**validation** · six conditions, 38 folds, 3 seeds · equal run means; counts not independent

| Ölçüt | Kayıtlı değer |
|---|---:|
| different_bce_ap_epoch | 473.000000 |
| feature_fold_pairs | 1406.000000 |
| runs | 684.000000 |
| test_evaluations | 0.000000 |
| zero_train_iqr_pairs | 152.000000 |

**Sınırlar / açık noktalar:**
- Reused validation, overlapping folds/seeds; not independent trades or final test.
- AP maxima are retrospective within BCE-stopped histories; alternative-epoch precision unavailable.
- Main independent review PASS; full37 follow-up unavailable due usage limit, locally checked.
- Marginal input means omit explicitly undefined dimensions; no causal or feature-removal inference.

**Kanıt kopyaları:**
- [research/analyses/comprehensive-diagnosis-20261028/REPORT.md](sources/50473b125fc558e3a907b03a0ff798b13699a2040847f4837c96c3f7cdea40bb.md) · SHA256 `50473b125fc558e3a907b03a0ff798b13699a2040847f4837c96c3f7cdea40bb`
- [research/analyses/comprehensive-diagnosis-20261028/checks.json](sources/455adfb380891a3681157dd5cb2dc7a7696401733c27584b4d74786fc55d2c5b.json) · SHA256 `455adfb380891a3681157dd5cb2dc7a7696401733c27584b4d74786fc55d2c5b`
- [research/analyses/comprehensive-diagnosis-20261028/feature_checks.json](sources/0ba8a71931678de703a41d7deac93ddcbb75b0c043e518e94134269284a3b408.json) · SHA256 `0ba8a71931678de703a41d7deac93ddcbb75b0c043e518e94134269284a3b408`
- [research/analyses/comprehensive-diagnosis-20261028/summary.csv](sources/bc7aa9b47fa2c8317f345f71e5e8865bfd28921bb83155c723f9742bbbdaf422.csv) · SHA256 `bc7aa9b47fa2c8317f345f71e5e8865bfd28921bb83155c723f9742bbbdaf422`

[Son kayıt](events/000048.json) · revizyon 1 · Complete user-authorized all-run diagnostics and full37 marginal input audit; preserve test boundary.

## exp-031-checkpoint-selection

**A6: seÃ§im ve deÄŸerlendirme ayrÄ±mÄ±yla BCE/AP checkpoint karÅŸÄ±laÅŸtÄ±rmasÄ±**

AynÄ± eÄŸitim akÄ±ÅŸÄ±nda minBCE ve maxAP seÃ§imi, sonraki validation bÃ¶lÃ¼mÃ¼nde seÃ§icilik ve dÃ¶nem kararlÄ±lÄ±ÄŸÄ±nÄ± deÄŸiÅŸtiriyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-030-comprehensive-diagnosis, exp-021-feature-comparison

**Yöntem:** {"assessment_rows": 528, "assessment_targets": 465, "folds": 38, "gap_rows": 24, "learning_rate": 0.001, "model": "A6 GRU", "release": "advisor-checkpoint-selection-v1.0.0", "seeds": [42, 43, 44], "selected_checkpoints": 228, "selection_rows": 528, "selection_targets": 465, "sequence_length": 64, "stopping": "common selection BCE patience15, maximum100", "thresholds": "fixed0.5 plus selection-score top5/top10 cutoff; assessment untouched by choice", "train_rows": 5040, "trajectories": 114}

**Veri kimliği:** {"evaluation_scope": "selection/assessment inside historical validation only; no final test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Checkpoint epochs frozen from selection minBCE/maxAP; no assessment-driven choice.

**Karar / öğrenilen:** AP checkpoint selection did not improve subsequent assessment AP or selective precision consistently; retain BCE control. No final test. 114 trajectories complete in review; weights not independently downloaded.

**validation** · 114 matched A6 trajectories, 465 assessment targets each · Equal-run BCE/AP means; audit counts

| Ölçüt | Kayıtlı değer |
|---|---:|
| ap_selector_ap | 0.403354 |
| ap_selector_bce | 0.643427 |
| bce_selector_ap | 0.404100 |
| bce_selector_bce | 0.611859 |
| completed_trajectories | 114.000000 |
| recomputed_decision_rows | 684.000000 |
| verified_nonweight_hashes | 798.000000 |

**Sınırlar / açık noktalar:**
- Historical validation has been seen; assessment is separated within new run, not an unseen final test.
- Overlapping folds and repeated seeds remain dependent.
- Common BCE stopping; not an AP early-stopping comparison.
- New assessment cohort is not directly comparable to old1017 validation targets.

**Kanıt kopyaları:**
- [research/analyses/checkpoint-selection-20261029/PLAN.md](sources/ccf31ae05ae6cbbdc3bb25d8747e20ce8cbeecac2bf9e350a789f01e10d1b1d2.md) · SHA256 `ccf31ae05ae6cbbdc3bb25d8747e20ce8cbeecac2bf9e350a789f01e10d1b1d2`
- [research/analyses/checkpoint-selection-20261030/REPORT.md](sources/9b8552f3e80053c4630b036a024a080fbec466e96674b8c38043f607840a36cb.md) · SHA256 `9b8552f3e80053c4630b036a024a080fbec466e96674b8c38043f607840a36cb`

[Son kayıt](events/000050.json) · revizyon 2 · Completed Colab review: AP selection advantage did not transfer to subsequent assessment.

## exp-032-cnn-gru

**AltÄ± Ã¶zellik: GRU ve nedensel CNN ardÄ±ndan GRU**

Yerel nedensel CNN Ã¶n iÅŸlemesi, aynÄ± altÄ± girdide GRU kontrolÃ¼ne gÃ¶re sonraki validation dÃ¶neminde seÃ§icilik ve kararlÄ±lÄ±ÄŸÄ± artÄ±rÄ±yor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **not_selected**

Önceki kayıtlar: exp-031-checkpoint-selection, exp-021-feature-comparison

**Yöntem:** {"assessment_rows": 528, "assessment_targets": 465, "folds": 38, "gap_rows": 24, "learning_rate": 0.001, "model": "A6 GRU / Conv1D32-k3-GELU ardÄ±ndan aynÄ± GRU", "release": "advisor-cnn-gru-v1.0.0", "seeds": [42, 43, 44], "selected_checkpoints": 228, "selection_rows": 528, "selection_targets": 465, "sequence_length": 64, "stopping": "each architecture selection BCE patience15, maximum100", "thresholds": "fixed0.5 plus selection-score top5/top10 cutoff; assessment untouched by choice", "train_rows": 5040, "trajectories": 228}

**Veri kimliği:** {"evaluation_scope": "selection/assessment inside historical validation only; no final test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Epoch yalnÄ±z seÃ§im BCE; fixed0.5 ve seÃ§im Ã¼st%5/%10 skor cutofflarÄ± deÄŸerlendirmeye deÄŸiÅŸmeden uygulanÄ±r.

**Karar / öğrenilen:** CNN-GRU genel AP/BCE ve dönem/seed kararlılığında tutarlı iyileşme sağlamadı; GRU kontrolü korunur.228 çalışma tamam; final test yok.

**validation** · 228 run, mimari başına114; bölüm başına465 assessment hedefi · AP/BCE eşit run ortalaması; precision toplam TP/sinyal

| Ölçüt | Kayıtlı değer |
|---|---:|
| cnn_gru_ap | 0.400784 |
| cnn_gru_bce | 0.613366 |
| cnn_gru_top5_precision | 0.424365 |
| gru_ap | 0.404100 |
| gru_bce | 0.611859 |
| gru_top5_precision | 0.411541 |

**Sınırlar / açık noktalar:**
- Tarihsel validation gÃ¶rÃ¼lmÃ¼ÅŸtÃ¼r; final test deÄŸildir.
- DÃ¶nemler/seedler baÄŸÄ±msÄ±z deÄŸildir.
- Parametre sayÄ±sÄ± eÅŸit deÄŸildir; bu somut mimari deÄŸiÅŸikliÄŸi karÅŸÄ±laÅŸtÄ±rÄ±lÄ±r.
- Sabit hiperparametreler her mimarinin eriÅŸebileceÄŸi en iyi performansÄ± gÃ¶stermez.

**Kanıt kopyaları:**
- [research/analyses/cnn-gru-20261030/PLAN.md](sources/86b4605a0f22f5b6458d0995984b720e752a7b0f478b35f010031cd0e0a1102f.md) · SHA256 `86b4605a0f22f5b6458d0995984b720e752a7b0f478b35f010031cd0e0a1102f`
- [research/analyses/cnn-gru-20261031/REPORT.md](sources/ca7d5315bf1e4c04c3c54e084267face7f8ba1383d4454c83a2e28cb3773e0d4.md) · SHA256 `ca7d5315bf1e4c04c3c54e084267face7f8ba1383d4454c83a2e28cb3773e0d4`

[Son kayıt](events/000052.json) · revizyon 2 · Kullanıcının tamamlanmış CNN-GRU ZIP çıktıları doğrulandı; aday genel iyileşme sağlamadı.

## exp-033-transfer-diagnosis

**GRU ve CNN-GRU seçimden değerlendirmeye aktarım teşhisi**

Mevcut iki mimari aynı dönemlerde mi zorlanıyor ve seçim avantajı sonraki bölüme taşınıyor mu?

Kampanya: `campaign-001` · Durum: **completed** · Sonuç: **inconclusive**

Önceki kayıtlar: exp-030-comprehensive-diagnosis, exp-031-checkpoint-selection, exp-032-cnn-gru

**Yöntem:** {"aggregation": "Üç seed ortalamasıyla dönem Spearman korelasyonu; AP-pozitif oranı betimleyici farkı", "changed_factor": "Yok; mevcut tahmin/history üzerinde betimleyici analiz", "folds": 38, "runs": 228, "seeds": [42, 43, 44]}

**Veri kimliği:** {"evaluation_scope": "selection/assessment inside historical validation only; no final test command", "labels_id": "original-tp2-sl5-h10-stop-first", "raw_sha256": "a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c", "snapshot_id": "legacy-colab-v1-development", "split_id": "original33551-38fold-5040-1080-720-step720-purge24-embargo24"}

**Seçim kuralı:** Yeni model/epoch/eşik seçimi yok; final test yok.

**Karar / öğrenilen:** Kesin neden doğrulanmadı. Ortak dönem davranışı güçlü, seçim avantajı aktarımı zayıf. Sonraki öneri yalnız GRU hidden128->64; uygulanmadı/eğitilmedi.

**validation** · Exp032 aynı228 run; seçim/assessment465 hedef · 38 fold, her fold üç seed ortalaması

| Ölçüt | Kayıtlı değer |
|---|---:|
| cnn_transfer_excess_spearman | 0.188533 |
| gru_transfer_excess_spearman | 0.088084 |
| shared_excess_spearman | 0.875916 |

**Sınırlar / açık noktalar:**
- Tarihsel validation gÃƒÂ¶rÃƒÂ¼lmÃƒÂ¼Ã…Å¸tÃƒÂ¼r; final test deÃ„Å¸ildir.
- DÃƒÂ¶nemler/seedler baÃ„Å¸Ã„Â±msÃ„Â±z deÃ„Å¸ildir.
- Parametre sayÃ„Â±sÃ„Â± eÃ…Å¸it deÃ„Å¸ildir; bu somut mimari deÃ„Å¸iÃ…Å¸ikliÃ„Å¸i karÃ…Å¸Ã„Â±laÃ…Å¸tÃ„Â±rÃ„Â±lÃ„Â±r.
- Sabit hiperparametreler her mimarinin eriÃ…Å¸ebileceÃ„Å¸i en iyi performansÃ„Â± gÃƒÂ¶stermez.

**Kanıt kopyaları:**
- [research/analyses/cnn-gru-transfer-20261031/REPORT.md](sources/9bc013119c14f8ea725cb02ffe36a913564c8dbd58e1d98f5c405447263a9cf3.md) · SHA256 `9bc013119c14f8ea725cb02ffe36a913564c8dbd58e1d98f5c405447263a9cf3`

[Son kayıt](events/000053.json) · revizyon 1 · Önceki analizleri tekrarlamadan exp032 seçim-değerlendirme aktarımını tamamla.
