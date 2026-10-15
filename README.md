# YeniBotDeney · Advisor araştırma çalışma alanı

Bu depo aynı veri üzerinde soruların, deneylerin ve öğrenilenlerin biriktiği
bağımsız araştırma laboratuvarıdır. Başlangıç noktası **[Deney defteri](research/INDEX.md)**.
Notebooklar çalıştırma aracıdır; kalıcı hafıza sonuç/karar kayıtlarıdır.

## Araştırmanın hafızası

- **[Deney defteri ve kayıtlı sonuç tabloları](research/INDEX.md):** ne denendi,
  ne elde edildi, hangi ölçüte göre seçildi/seçilmedi ve kanıtı nerede?
- **[Çalışma, kayıt, düzeltme ve yedekleme rehberi](research/README.md).**
- **[Kampanya 001](research/campaigns/001-model-comparisons.md):** A–D → wavelet
  → loss → final. 10 tarihsel kayıt; yeniden eğitim yapılmadı.
- **[Kampanya 002](research/campaigns/002-diagnostics.md):** validation eşikleri
  ve 2/5, 2/2, 3/2 ATR bariyerleri. İki analiz tamamlandı:
  **[grafikler ve sonuç tablosu](research/analyses/diagnostics-20261015/REPORT.md)**.
- **[10 bariyer senaryosu ve aday karşılaştırması](research/analyses/barrier-expansion-20261015/REPORT.md):**
  7 ek senaryo tamamlandı; sonraki validation için 1/1, 1/2 ve 1.5/2 adayları.
  Eğitim yapılmadı, üretim bariyeri seçilmedi.

Kayıtlar Git'te sürümlenir. Düzeltmeler gerekçeli yeni revizyon olarak eklenir;
önceki sonuç ve karar silinmez. Kanıt belgelerinin hashli kopyaları saklanır.
Teknik tamamlanma, yöntem seçimi ve nihai başarım ayrı değerlendirilir.

## Gerektiğinde çalıştırma araçları

[Notebook rehberi](notebooks/README.md). Mevcut notebooklar tarihsel protokolün
tekrar üretimi/kurtarma/denetimi içindir; yeni teşhis planlarını çalıştırmaz.

| İhtiyaç | Notebook | Colab |
|---|---|---|
| Eksik eski tabloları geri elde et | [01 · Veri kurtarma](notebooks/workflows/01_recover_data.ipynb) | [Aç](https://colab.research.google.com/github/umutergul74/YeniBotDeney/blob/advisor-notebooks-v2.1.0/notebooks/workflows/01_recover_data.ipynb) |
| Kontrol veya isteğe bağlı deney çalıştır | [02 · Araştırma](notebooks/workflows/02_research.ipynb) | [Aç](https://colab.research.google.com/github/umutergul74/YeniBotDeney/blob/advisor-notebooks-v2.1.0/notebooks/workflows/02_research.ipynb) |
| Tamamlanmış final dosyalarını denetle | [03 · Arşiv denetimi](notebooks/workflows/03_audit_archive.ipynb) | [Aç](https://colab.research.google.com/github/umutergul74/YeniBotDeney/blob/advisor-notebooks-v2.1.0/notebooks/workflows/03_audit_archive.ipynb) |

## Güncel durum · 15 Ekim 2026

Tarihsel A–D, wavelet, loss ve final deneyleri tamamlandı. Seçilen yapı:
**6 özellik + GRU + wavelet kapalı + saf BCE**. Final performansı sınırlı ve
seed duyarlı; üretim veya işlem stratejisi başarısı iddiası yok.
[Final sonuçları](docs/advisor-final-results.md).

Eylül 2026 artık görülmüş testtir. Yeni model/eşik seçimi için tekrar
kullanılmaz. 03 yalnızca dosya bütünlüğünü denetler.

02 mevcut protokolün izole ortamda tekrar üretimidir. Yeni piyasa verisi veya
yeni bilimsel protokol sağlamaz. Wavelet ve loss zorunlu adımlar değildir;
araştırma sorusu gerektiriyorsa seçilir. Eski 08/09/10'un açıklaması
[notebook rehberinde](notebooks/README.md).

## Çalışma düzeni

- Yeni girişler `advisor-notebooks-v2.1.0` sabit yayınına bağlıdır.
- Drive hesabı `icinbedava34@gmail.com`; eski `colab_v1` arşivi salt okunurdur.
- Kod/ortam değişirse yeni workspace gerekir; eski dosyalar üzerine yazılmaz.
- Eğitim varsayılan kapalıdır; veri, checkpoint ve raporlar Drive'a kaydedilir.
- Anlamlı değişiklikler çalışma dalında commit/push edilir; main'e otomatik merge yok.
- Doğrulama değişen kapsamla sınırlıdır: [test bütçesi](docs/test-budget.md).

## Belgeler

- [Ortam, kayıt ve kesintiden devam](docs/advisor-notebooks-v2.md)
- [Güncel yöntem değerlendirmesi ve sonraki protokol önerileri](docs/research-methods-roadmap.md)
- [Tarihsel deney kaydı](docs/advisor-experiments-status.md)
- [Depo bağlantısı ve Git çalışma düzeni](docs/workspace-migration.md)
- [Katkı kuralları](CONTRIBUTING.md)
- [Özgün projenin tarihsel README kopyası](docs/legacy-project-readme.md)

Eski 00–10 notebookları uyumluluk/tarihçe içindir; aktif giriş noktaları
`notebooks/workflows/` altındadır. Donmuş motor, eski sonuçlar ve paket kilidi korunur.
