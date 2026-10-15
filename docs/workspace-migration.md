# Bağımsız araştırma deposu

15 Ekim 2026: çalışma alanının yayın hedefi
`https://github.com/umutergul74/YeniBotDeney.git` oldu (`origin`).
Önceki depo `legacy-source` adıyla kaynak geçmişi için korunur; oraya push yapılmaz.
Çalışma dalı `codex/advisor-reproducible-notebooks`; main'e birleştirme yapılmaz.

İlk aktarım mevcut Git geçmişini korur; veri, checkpoint veya yerel raporları
eklemez. İlk aktarım yalnızca bu belgedir ve CI atlanır. Sonraki notebook
düzenlemesi kendi değişiklik kapsamıyla doğrulanır. Eski yayın etiketleri
taşınmaz/değiştirilmez. Yeni notebook sürümü yeni bir etiket alır.

Anlamlı aşamalar: temiz diff → kapsam seçimi → ilgili doğrulama → açıklayıcı
commit → origin'e push. Günlükler `reports/` altında tutulur. Başarılı aynı
testleri yerel ve CI'da tekrarlamak yerine tek doğrulama yeri seçilir.
