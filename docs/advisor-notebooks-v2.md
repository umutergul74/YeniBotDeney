# Advisor notebookları v2 — tekrar üretilebilir çalışma düzeni

15 Ekim 2026. Bağımsız depo: `C:/Users/Umut/Desktop/advisor-research`.
Dal: `codex/advisor-reproducible-notebooks`.
Değişmeyen araştırma motoru başlangıcı: `741d1d4`.

## Amaç ve sınır

Colab'ın önceden kurulu paketlerini araştırma ortamı kabul etmiyoruz. Yeni
notebooklar ayrı Linux x86_64/Python 3.13.15 ortamında çalışır. Bilimsel paketlerin
tam bağımlılık zinciri `requirements/advisor-linux-py313.lock` içinde sürüm ve
dağıtım hashleriyle sabittir. Kurucu uv aracının Linux wheel'i de hash ile sabittir.
Paketler Colab host Python'una veya kullanıcının yerel global ortamına kurulmaz.

Bu bir platformlar arası bit eşitliği garantisi değildir. GPU/driver/işletim sistemi
sayısal sonucu etkileyebilir. Eğitim Tesla T4 ile sınırlandırılır; aynı çalışma
alanında Python build'i, paket, GPU/CUDA/cuDNN, kaynak kod veya commit değişirse
devam edilmez. Yeni koşul için yeni WORKSPACE_ID ve gerekirse yeni protokol gerekir.
Eski Colab host ortamının aynen yeniden yaratıldığı iddia edilmez.

## Kod ve eski kanıtlar

`yenibot/training/advisor*.py`, özellik/etiket/model motoru ve bilimsel YAML
ayarları değiştirilmedi. Eski notebooklar `notebooks/archive/advisor_v1/` altında
özgün Git byte'ları ve SHA256SUMS ile korunur. Sonuçlar/model ağırlıkları yeniden
üretilmedi. Eylül 2026 artık görülmüştür; yeni araştırmanın final testi olarak
yeniden kullanılamaz.

Yeni notebooklar `advisor-notebooks-v2.0.2` sabit Git yayınına bağlıdır. Yayın
etiketini taşımayın; sonraki kod değişikliğini yeni yayın ve yeni çalışma olarak
yönetin. Aynı oturumda başka dalın kodunu import etmeyin. Python araştırma
kodunu notebook kernel'ı yerine `-I` ile izole alt süreç yürütür.

## Drive dizinleri

Kök: `MyDrive/yeniBot/advisor_experiments/`.

| Dizin | Kullanımı |
|---|---|
| `colab_v1/` | Tarihsel arşiv; v2 tarafından salt okunur |
| `recovery_v2/<WORKSPACE_ID>/` | Eksik A/B–D tablolarının yeni ve hash doğrulamalı kopyası |
| `research_v2/<WORKSPACE_ID>/` | Yeni ortamda bütün kontrol ve adayların ayrı sonuçları |
| `archive_audit_v2/<WORKSPACE_ID>/` | Eski final sonucunun salt okunur denetim raporu |
| `reproducibility_cache_v2/` | Yalnizca hashli kurucu wheel; uv kilitleri ve paket onbellegi yerel disktedir |

Workspace içi:

- `inputs/`: hash doğrulanmış, ayrı ham kaynak kopyaları.
- `data/`: hazırlanmış Parquet tabloları, manifestler ve çalıştırma ayarları.
- `runs/`: her seed/fold'un ağırlık, optimizer/RNG, scaler ve ilerleme kayıtları.
- `reproducibility/`: tam kod/ortam kimliği, paket kilidi, ortam profili ve Git kaynak kod ZIP kopyası.
- `sessions/<session>/`: kurulum/günlükler ve aşama durum kayıtları.
- `STATUS.md` ve `STATUS.json`: son işlem ve kesinti durumu.
- `reports/prepared_frames.zip`: **gerçek hazırlanmış tablolar ve manifestler**.
- `reports/advisor_latest_review_bundle.zip`: küçük inceleme paketi; ağırlık içermez.
- `reports/full_artifact_inventory.json`: raw/model/çıktı dosyalarının envanteri; değişebilen oturum günlükleri ayrıca listelenir.

Modeller dahil tam yedek için yalnızca reports klasörünü değil, workspace'in
tamamını indirin. ZIP iki parçaya bölünürse bütün parçalar gerekir.

## 06 ve 07 — eksik dosyaları geri elde etmek

Varsayılan MODE='recovery', ALLOW_TRAINING=False. Önce 06, sonra 07. Her ikisinde
aynı WORKSPACE_ID kullanılır. Eski Drive `colab_v1` sabit snapshot'ı bulunmalıdır.
Yeni ham veri indirilmez. 06 A tablosunu, 07 B/C/D'nin ortak tablosunu hazırlar.
Özgün run protocol data_sha256 eşleşmeden Drive'a özgün kopya olarak yayımlanmaz.
Başarılı çıktılar recovery workspace'in `data/` ve `reports/prepared_frames.zip`
alanındadır. Eski manifest veya tabloların üzerine yazılmaz.

## Yeni araştırma: 06 → 07 → 08 → 09

06/07'de MODE='research', ortak yeni WORKSPACE_ID ve ALLOW_TRAINING=True seçilir.
06 yeni A kontrolünü; 07 sırayla B,C,D kontrollerini üretir. Varsayılan tüm liste
tek tek daraltılabilir; 08 öncesinde her kapsam 38 fold × 3 seed tamamlanmalıdır.
Eski `colab_v1` kontrol metrikleri yeni ortamla birleştirilmez.

08/09 MODE='research' kullanır. ALLOW_TRAINING=True açıkça seçilmelidir.
Referanslar performansa göre değil, tek tamamlanmış kapsam kimliğiyle çözülür.
Mevcut dar motor, validation kazananı A/6 özellik olduğunda wavelet/loss çalışır.
Yeni ortamda başka aday kazanırsa bu sonuç gizlenmez veya A zorlanmaz; motor
durur ve mimari/özellik kapsamı için yeni bilimsel protokol hazırlanır.

Model, etiket, purge/embargo, loss ve seçim ölçütleri değiştirilmedi. Epoch ve
yöntem seçimi validation BCE; geçmiş 10 saatlik etiket ufku için iki sınırda
24 saat boşluk korunur. Yeni nihai test bu notebook setinde otomatik seçilmez.

## 10 — tarihsel finali denetlemek

10 yalnızca eski final planını, kilitli modellerin dosya hashlerini, fit/test
tablolarını ve tahmin hashlerini denetler. Modelleri deserialize etmez, inference
veya yeni test değerlendirmesi yapmaz. Eski finali yeni ortamla yeniden eğitmek
veya başka eşikle puanlamak bu notebookun işlemi değildir.

## Kesinti ve takip

Normal Python/hücre kesintisinde son tamamlanan epoch checkpoint'i korunur;
workspace lease'i bırakılır. Notebooku aynı ayarlarla baştan çalıştırmak kurucu
önbelleğini ve uygun checkpointleri kullanır. Geçici veri hazırlama kesilirse
kalıcı veri/manifest çifti bozulmaz; yayınlanmamış hesaplama tekrar denenebilir.

Sert VM kapanması `.writer_lease` bırakabilir. Drive, güvenilir dağıtık kilit
garantisi sağlamaz. İkinci runtime'ı aynı workspace'e yazdırmayın. Stale lease
durumunda diğer yazıcının durduğunu doğrulayın, owner.json kaydını saklayın ve
yalnızca o workspace'in lease klasörünü kaldırın. Kontrolsüz otomatik kilit
kırma veya checkpoint üstüne yazma yoktur.

## Doğrulama durumu

Kod değişikliği için sentetik persistence/isolation testleri ve mevcut advisor
regresyonları; nihai gate olarak tek Linux tam CPU CI çalışması kullanılır.
Gerçek Colab kurulumu ve uzun eğitim kullanıcı oturumunda ayrıca doğrulanmalıdır.
CI CPU kontrolleri, T4/CUDA yeniden üretimini doğrulamaz. Testler tamamlanmadan
bu belge tek başına geçmiş bir başarı iddiası değildir.

## v2.0.1 - Drive/FUSE installation fix

uv cache, locks and temporary files now stay in local
`/content/advisor_isolated_runtime/`. Drive/FUSE does not support all uv
lock/persist operations. Drive `reproducibility_cache_v2` stores only the
verified bootstrap wheel; the old `uv-cache` subdirectory is no longer used.
Prepared data, models, configurations and logs are still saved to Drive.
Packages may download again in a new runtime; local cache survives within it.

After the v2.0.0 bootstrap error, open the v2.0.1 notebook in a new Colab
runtime and run from the beginning. Do not delete Drive files. If preparation
and training were never reached, the same WORKSPACE_ID can be used. Existing
v2.0.0 workspaces with a frozen identity require a new WORKSPACE_ID for a new
commit. The historical archive and package lock are unchanged.

## v2.0.2 - Colab plotting environment isolation

The launcher sets MPLBACKEND=Agg before importing research packages. Notebook
subprocesses, bootstrap and runtime checks use the same headless backend.
No matplotlib_inline or IPython packages are added to the research lock.
Inherited UV_SYSTEM_PYTHON is removed from bootstrap subprocesses as well.

For an already-open v2.0.1 session, before retrying the preparation cell:

```python
import os
os.environ["MPLBACKEND"] = "Agg"
```

This does not edit tracked sources or change data/model settings. Keep the same
release across 06/07 in an existing workspace. A new release must use a new
WORKSPACE_ID if an older release has already frozen that workspace identity.
