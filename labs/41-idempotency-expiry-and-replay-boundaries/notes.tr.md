# Gün 41 — Idempotency Süresi ve Replay Sınırları

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](expiry_demo.py)

## 40. günden devam
Idempotency key, kayıt saklandığı sürece aynı işlemin tekrar uygulanmasını önleyebilir. Fakat bu kayıtların **saklama süresi (TTL)** vardır. Süre dolunca eski istek ne olur?

Örnekte anahtar kullanıcıya, isteğin içeriğine ve beklenen sürüme bağlıdır. Süre dolmadan aynı istek gelirse `REPLAY`; farklı içerik gelirse `KEY_CONFLICT` döner. Süre dolduğunda anahtar yeni sayılabilir ama **eski sürüm kontrolü**, daha önce uygulanmış güncellemeyi reddeder.

## Çalıştır
```bash
python3 labs/41-idempotency-expiry-and-replay-boundaries/expiry_demo.py
```

## Sorular
TTL sona erince neden eski istek yeniden güvenilir olmaz? Anahtar kaydı ve belge güncellemesi neden tek bir atomik veritabanı işlemi olmalı? Aynı anda gelen iki istek hangi problemi doğurur?

## Sınırlar
Bu gerçek bir HTTP veya veritabanı uygulaması değildir; tek süreçli ve sahte zamanlı eğitim modelidir.
