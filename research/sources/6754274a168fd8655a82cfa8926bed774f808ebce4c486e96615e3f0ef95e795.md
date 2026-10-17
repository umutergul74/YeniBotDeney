# Kaynak ve tekrar üretim kimliği

Advisor repo commit: 386bde26008eee13412495ae99632677b3c6582e
Eski proje HEAD: 741d1d4bebbb7fe2a931d09d56f5fe6d87bac006
Eski projenin dirty çalışma ağacı salt okunur incelendi. HEAD tek başına aşağıdaki dosyaları tanımlamaz.

## Eski proje kaynak dosyaları SHA256
- ../yeniBot/docs/current-status.md: `4b6462b78b0d3f976c67b885f68ae1cf2fcabd6485be0d2282f314c5c0d42490`
- ../yeniBot/docs/experiment-history.md: `61bb81267a9edd240bb375648f5de35b953874390b4c77b075ebb65ea2d12578`
- ../yeniBot/SKILLS.md: `c6dda0e0b64bc43377b3a699695a1d5409d4d7f747a7b0e56166a3f2e22e15b6`
- ../yeniBot/config.yaml: `97edc222205da8c06f6a983c9c45701b8e99ec9c5a2b0590746e2d03ac2a2c91`
- ../yeniBot/yenibot/diagnostics/calibration.py: `2ca8cf05456aa1d98408195d0f110e133b08d20f872f9996733dbb1d9c4bdd63`
- ../yeniBot/yenibot/experiment/holdout.py: `e5e54ff30638359cf700dd298112134bd68eb039eddbcddbef4ff88c79696597`
- ../yeniBot/yenibot/experiment/thresholds.py: `770aefdf6eb5ef3fbf09e51b0f9a956a4ae7fd0b49061acf91e99819bd7167a9`

## Mevcut ortam
- Python 3.13.7
- numpy: 2.2.6
- pandas: 2.3.3
- scikit-learn: 1.7.2
- pyarrow: 25.0.1
- matplotlib: 3.10.7

## Tekrar üretim
Rapor/scripts kaynak metni deftere capture edildi. Depo kökünde sırayla probe.py, feature_drift.py, adjacent.py, figures.py çalıştırılır. Girdiler reports/review-20261017/source.zip ve reports/root-cause-20261017/B12.parquet. Kaynak hashleri REPORT.md içinde. Bu scriptler test indirme veya GRU eğitimi yapmaz.

## CSV SHA256
- adjacent_window_probe.csv: `d0f96ece70d81c49ef3903f62b29198199e68d59fe5cf95380fa3179ab6254de`
- ensemble_paired_effect.csv: `b67db6c5b33247060640b4f028cc3e1b30f47739e98851139321853a1a5ded1a`
- epoch_objective_audit.csv: `b94633d2c70af77e59d7a9d4f2333c9789a42431c5c002fbd899339dbca5ac6e`
- matched_fold_summary.csv: `f9ff650916d15c5b7c60f33f7ea089b65d1db8864c84725b4fa087270663b380`
- probe_by_fold.csv: `27d60516761728c7b7605db3c2fbf71e08a33ba5098a0f97425142627772ecaf`
- probe_summary.csv: `dc94f491a25c088d6d22251bb1e262de5fa2b82d551c1124ff3edfa32783570e`
- score_feature_association.csv: `840ba6ac8e9411e2031d86bfaf302d543a2cbe14ded2eede5b139ed7e48ea184`
- verified_feature_shift.csv: `7ffa30f1ed9801d2b716645798cd72614a457cbb7e90e17c9573dad1aadeb28d`
- within_validation_drift.csv: `9a6e526ecf7661fccd21d80b68cc6915a96c366909c1984f0025f130d0f6f81e`
