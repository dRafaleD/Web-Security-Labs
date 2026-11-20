# Gün 47 — JSON Boyut/Derinlik Sınırı ve Idempotency

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](request_limits_demo.py)

## 46. günden devam
Önceki gün tekrarlanan JSON key'lerini reddettik. Şimdi ek soru: istek **çok büyük** veya **aşırı iç içe** olursa ne olacak?

**Byte limit:** gelen verinin bayt olarak üst sınırı. **Nesting depth:** JSON nesnelerinin iç içe derinliği. **Canonical fingerprint:** doğrulanmış isteğin tutarlı SHA-256 özeti. **Idempotency:** aynı işlemin ikinci kez uygulanmasını engelleme yaklaşımı.

Kod kimlik yetkisini kontrol eder, 160 bayt sınırını uygular, JSON'u ayrıştırır, yinelenen alanları reddeder, derinlik ve şema kontrolü yapar. Yalnızca geçerli istekler için idempotency kaydı oluşturur. Hatalı isteğin **anahtar ayırmaması** önemli.

## Çalıştır
```bash
python3 labs/47-request-size-depth-and-idempotency-boundaries/request_limits_demo.py
```

## Sorular
Bayt sınırı karakter sınırından neden farklıdır? Çok derin JSON'un zararı nedir? Hatalı istek idempotency anahtarı kaydederse ne olabilir?

## Sınır
Gerçek HTTP, veritabanı ve concurrency yoktur; sadece yerel test verileridir.
