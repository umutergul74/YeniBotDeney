# Deney defteri

Bu görünüm kayıtlı sonuçları listeler; analiz veya eğitim çalıştırmaz.
Kaynak: `events/` içindeki eklemeli kayıtlar. Rakamlar kaynak raporların yuvarlatılmış değerleridir.
Validation ve test ayrı kapsamdır; bu tablo otomatik bir başarı sıralaması değildir.

**14 deney/plan · 21 geçmiş kaydı**

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
| [exp-014-barrier-training](#exp-014-barrier-training) | Dört ATR bariyeri: GRU/BCE, ayrı epoch/eşik doğrulaması ve Ekim testi | planned | pending |

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

Kampanya: `campaign-002` · Durum: **planned** · Sonuç: **pending**

Önceki kayıtlar: exp-013-barrier-expansion

**Yöntem:** {"architecture": "GRU", "horizon_hours": 10, "loss": "BCE", "same_bar_rule": "stop-first", "seeds": [42, 43, 44], "tp_sl_atr": [[2, 5], [1, 1], [1, 2], [1.5, 2]], "training_runs": 12}

**Veri kimliği:** {"evaluation_scope": "planned; no new training or test executed", "labels_id": "barriers-four-h10", "raw_sha256": "f3a29be9f7a935ca144fe70a701b41072f30a1b2432b177faa309a8c37b404c6", "snapshot_id": "legacy-final-fit-raw", "split_id": "fixed-train-20251218-20260715-val-20260717-20260808-cal-20260810-20260830-test-20261002-20261014"}

**Seçim kuralı:** Epoch: validation BCE. Threshold: mean calibration F1, ties highest threshold. Candidate: calibration BCE skill, ties ID. Test cannot select.

**Karar / öğrenilen:** Colab T4 notebook hazırlanıyor; test 2–14 Ekim 2026. Eğitim/test henüz yapılmadı.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- 13-day single holdout, overlapping labels, no trading costs.
- Previously seen August is development only; September excluded from evaluation.
- Different label targets; no absolute strategy winner claim.

**Kanıt kopyaları:**
- [research/analyses/barrier-training-20261015/PLAN.md](sources/712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32.md) · SHA256 `712f6072f0a9443e3d879bec33544b78c76335855c9f764715c813d1769b2e32`

[Son kayıt](events/000021.json) · revizyon 1 · Kullanıcı eğitim notebookunu ve uygun yeni test dönemi seçimini yetkilendirdi.
