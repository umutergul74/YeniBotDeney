# Araştırma çalışma alanı

Başlangıç noktası **[Deney defteri](INDEX.md)**. Notebooklar yalnızca deney
çalıştırma araçlarıdır; araştırmanın hafızası bu dizindir.

## Çalışma döngüsü

1. Soru/öneri gelir. Yeni kalıcı kimlikle plan açılır; önceki deneye bağlanır.
2. Ham veri snapshot'ı, etiket sürümü, zaman ayrımı, seçim ölçütü, adaylar ve
   bütçe sonuçlara bakmadan yazılır. Bilinmeyen alanlar açıkça boş bırakılır.
3. Kullanıcı çalıştırmayı istediğinde ayrı run/workspace açılır. Her tekrarın
   run ID, tam commit, ortam kilidi, seedler, veri/config hashleri ve artifact
   konumları kayda eklenir. Yeni çalıştırma aynı deney kimliğini kullanarak
   eski run'ı ezmez; yeni kimlik + `parent_ids` ile bağlanır.
4. Çıktı ve hata kanıtları saklanır. Validation ve test ayrı sonuç bloklarıdır.
5. Başarı ölçütüne göre karar ve öğrenilen ders yazılır. Olumsuz, yarım kalmış
   ve teknik hata ile bitmiş deneyler de saklanır.
6. Kayıt doğrulanır, defter üretilir, commit/push yapılır ve ayrıca yedek alınır.

İlk kurulumda iki teşhis önerisi yalnızca plan olarak saklandı. Kullanıcının
sonraki açık isteğiyle 15 Ekim 2026'da [teşhisler tamamlandı](analyses/diagnostics-20261015/REPORT.md).
Eğitim ve yeni test değerlendirmesi yapılmadı; yeni eşik/bariyer seçilmedi.

## Durum ile sonuç farklıdır

| Alan | Değerler | Anlamı |
|---|---|---|
| status | planned, running, completed, failed, abandoned | İşlem ne durumda? |
| outcome | pending, selected, not_selected, mixed, inconclusive, technical_failure | Bu kapsamda ne öğrendik? |

`completed + not_selected` başarısız bir yazılım çalışması değildir: deney
tamamlanmış, aday seçilmemiştir. `selected` üretime hazır veya kârlı demek değildir.
Genel bir başarılı/başarısız etiketi yerine ölçüt ve gerekçe birlikte korunur.

## Kalıcı kayıt yapısı

- `events/`: artan sıra, önceki dosyanın SHA256'sı ve tam kayıt revizyonları.
  Eski dosyalar değiştirilmez/silinmez. Düzeltme gerekçeli yeni event'tir.
- `sources/`: kaynak inceleme belgelerinin içerik hashli kopyaları. Kaynak
  belge daha sonra değişse de dayanak korunur.
- `INDEX.md`: kayıtlardan üretilen okunabilir görünüm; elle düzenlenmez.
- `templates/`: yeni plan şablonu. Eğitim kodu veya çalışma talimatı değildir.
- `campaigns/`: birbirini izleyen araştırma soruları ve kararların bağlamı.

Mevcut tarihsel metrikler kaynak raporlardan aktarıldı; yeniden hesaplanmadı.
Aktarım tarihi deneyin gerçek çalışma tarihi değildir. Eksik ham/model
hashleri uydurulmadı. Kayıtlı review belgesinin hash doğrulaması, dışarıdaki
ham veri ve checkpointlerin mevcut veya doğrulanmış olduğu anlamına gelmez.

## Komutlar (depo kökünden)

Yalnızca Python standart kütüphanesi gerekir; ML paketi/Drive bağlantısı gerekmez.

```powershell
python scripts/advisor_lab.py list
python scripts/advisor_lab.py show exp-001-a
python scripts/advisor_lab.py show exp-001-a --history
python scripts/advisor_lab.py validate
python scripts/advisor_lab.py report --output research/INDEX.md
```

Plan için `templates/experiment.json` dosyasını `reports/my-plan.json` olarak
kopyalayın, alanları doldurun ve yeni kimlik verin:

```powershell
python scripts/advisor_lab.py create --file reports/my-plan.json --reason "Yeni araştırma sorusu; henüz çalıştırılmadı"
```

Sonuç/düzeltme için `show` çıktısındaki tam kaydı bir dosyaya alın, güncelleyin;
aynı kimlikle `append --file ... --reason ...` kullanın. Eski revizyon korunur.
`capture <rapor-dosyası>` küçük kanıt belgesini kopyalar ve kayda eklenecek
evidence nesnesini döndürür. Teknik hata raporunu da böyle saklayın.
Komutlar otomatik eğitim veya Git push başlatmaz.

Veri/etiket/model/ayar değişikliği eski kaydın düzeltmesi değildir; **yeni deney**
kimliği gerekir. Metadata düzeltmesi açıklanır; eski karar silinmez.
Bir deftere tek yazıcı kullanın. Sert kesintide `.writer.lock` kaldıysa başka
yazıcı olmadığını doğrulayın; yarım event'i geçerli kanıtmış gibi kullanmayın.

## Karşılaştırma kuralları

Aynı ham veri tek başına aynı deney koşulu değildir. Etiketler, timestamp/split,
seed kapsamı, ölçüt tanımı, toplulaştırma ve ortam da karşılaştırmada belirtilir.
Defter otomatik kazanan seçmez ve farklı cohort'ları tek sıralamaya karıştırmaz.
A–D'de A'nın altı özelliği B/C/D'nin birebir altkümesi değildir; bu sınırlama korunur.

Eşik seçimi validation'da yapılır. Bariyer değişikliği yeni etiket sürümüdür;
farklı hedeflerin BCE/F1 değerleri doğrudan aynı hedefin iyileşmesi gibi sunulmaz.
Eylül 2026 testinden yalnızca mevcut sonuçlar raporlanır; yeni seçim/deneme yapılmaz.

## Yedek ve kurtarma

```powershell
python scripts/advisor_lab.py bundle reports/research-backup-20261015.zip
python scripts/advisor_lab.py verify-bundle reports/research-backup-20261015.zip
```

Yedek mevcut dosyanın üstüne yazmaz; her seferinde benzersiz ad kullanın.
ZIP'i doğruladıktan sonra farklı diske/Drive'a ikinci kopya alın. Kurtarmada
boş bir dizine açın, `--root <açılan-dizin> validate` çalıştırın; mevcut defteri
üzerine açmayın. Hash zinciri rastlantısal değişiklikleri yakalar; Git'teki
önceki commit ve ayrı yedek olmadan bilinçli bütün-geçmiş yeniden yazımını
veya son kayıtların silinmesini tek başına ispatlayamaz.

**Bu ZIP deney defteri ve küçük kanıt belgeleridir. Ham veri/model yedeği değildir.**
Büyük artifactler Drive workspace'lerinde ayrıca saklanmalı; tam envanter ve
hashleri deney kaydına bağlanmalı. Git push da büyük artifactlerin yedeği değildir.
Hiçbir yerel araç mutlak veri kaybetmeme garantisi vermez; Git + ayrı defter
yedeği + artifact yedeği birlikte gereklidir.
