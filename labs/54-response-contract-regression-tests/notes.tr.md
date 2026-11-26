# Gün 54 — Yanıt Sözleşmesi Regresyon Testleri

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](contract_checks.py)

53. günde role özel DTO ve alan listeleri kullandık. Bugün yanıt alanları ve veri türleri için regresyon sözleşmesi oluşturuyoruz. Domain nesnesine eklenen iç alan dış DTO'ya otomatik sızmamalı. Member ve auditor çıktılarını karşılaştır; fazla alan, eksik alan, yanlış tür ve bilinmeyen rol farklı sonuç verir. 11 senaryoyu tahmin et, yeni hayalî özellik ekle ve member çıktısının değişmediğini doğrula. Şema testi tek başına nesne yetkilendirmesi veya izinli metin içinde hassas veri bulunmamasını garanti etmez. Gerçek HTTP veya dış hedef yoktur.

## Çalıştır
```bash
python3 labs/54-response-contract-regression-tests/contract_checks.py
```
