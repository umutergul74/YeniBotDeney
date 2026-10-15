# Deney defteri

Bu görünüm kayıtlı sonuçları listeler; analiz veya eğitim çalıştırmaz.
Kaynak: `events/` içindeki eklemeli kayıtlar. Rakamlar kaynak raporların yuvarlatılmış değerleridir.
Validation ve test ayrı kapsamdır; bu tablo otomatik bir başarı sıralaması değildir.

**12 deney/plan · 14 geçmiş kaydı**

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
| [exp-011-threshold-diagnostics](#exp-011-threshold-diagnostics) | Plan · Validation eşik–performans teşhisi | planned | pending |
| [exp-012-barrier-diagnostics](#exp-012-barrier-diagnostics) | Plan · ATR bariyerleri ve etiket dağılımı | planned | pending |

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

Kampanya: `campaign-002` · Durum: **planned** · Sonuç: **pending**

Önceki kayıtlar: exp-010-final

**Yöntem:** {"aggregation": null, "analysis": "precision/recall/F1 vs threshold", "threshold_grid": null, "training": false}

**Veri kimliği:** {"evaluation_scope": "development-validation-only; September 2026 excluded", "labels_id": null, "raw_sha256": null, "snapshot_id": null, "split_id": null}

**Seçim kuralı:** Testte seçim yok. Betimsel teşhis; eşik/etiket kazananı henüz tanımlanmadı.

**Karar / öğrenilen:** Çalıştırılmadı. Validation girdileri, ızgara ve seçim amacı önce kaydedilecek.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Girdi manifestleri ve analiz planı henüz kesinleştirilmedi.
- Yeni özellik/mimari denemesinden önce teşhis önerisi.

**Kanıt kopyaları:**

[Son kayıt](events/000011.json) · revizyon 1 · Kullanıcının ilettiği ikinci öneri; yalnızca plan kaydı.

## exp-012-barrier-diagnostics

**Plan · ATR bariyerleri ve etiket dağılımı**

TP/SL seçimi ilk temas sınıflarını ve süre dolumu getirilerini nasıl etkiliyor?

Kampanya: `campaign-002` · Durum: **planned** · Sonuç: **pending**

Önceki kayıtlar: exp-010-final

**Yöntem:** {"analysis": "first-touch counts and timeout return distribution", "horizon_hours": 10, "same_bar_rule": null, "tp_sl_atr": [[2, 5], [2, 2], [3, 2]], "training": false}

**Veri kimliği:** {"evaluation_scope": "development-validation-only; September 2026 excluded", "labels_id": null, "raw_sha256": null, "snapshot_id": null, "split_id": null}

**Seçim kuralı:** Testte seçim yok. Betimsel teşhis; eşik/etiket kazananı henüz tanımlanmadı.

**Karar / öğrenilen:** Çalıştırılmadı. Uygun tarih evreni, ATR ve temas kuralı belirlenmeden etiket üretilmeyecek.

**Henüz sonuç yok.**

**Sınırlar / açık noktalar:**
- Girdi manifestleri ve analiz planı henüz kesinleştirilmedi.
- Yeni özellik/mimari denemesinden önce teşhis önerisi.

**Kanıt kopyaları:**

[Son kayıt](events/000012.json) · revizyon 1 · Kullanıcının ilettiği ikinci öneri; yalnızca plan kaydı.
