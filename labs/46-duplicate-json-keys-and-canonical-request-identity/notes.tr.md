# Gün 46 — JSON Tekrarlanan Anahtarlar ve İstek Kimliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](strict_json_demo.py)

## 45. günden devam
Önceki gün aynı JSON içeriğinin alan sırası değişse bile **aynı mantıksal istek** olduğunu öğrendik. Ancak JSON içinde **aynı alan adı iki kez yazılırsa** ne olur?

Örnek: `{"version":1,"version":2}`. Bazı sistemler ilkini, bazıları sonuncusunu alabilir. Bu da uygulama ile aradaki proxy'nin **farklı istek yorumlamasına** neden olabilir.

Kod önce yinelenen tüm anahtarları reddeder, sonra veri yapısını ve tipleri doğrular. `NaN`, `true` türünde sürüm, izin verilmeyen alanlar ve eski sürüm reddedilir. Ancak bunlardan sonra standart JSON gösterimi ve SHA-256 ile fingerprint hesaplanır.

## Çalıştır
```bash
python3 labs/46-duplicate-json-keys-and-canonical-request-identity/strict_json_demo.py
```

## Sorular
Tekrarlanan key'in sonuncusunu kabul etmek neden riskli? Kontrolden önce neden canonicalization yapılmamalı? Idempotency neden tek başına gerçek veritabanı yarışını çözmez?

## Sınırlar
Gerçek HTTP sunucusu veya veritabanı içermez; yalnızca yerel örnektir.
