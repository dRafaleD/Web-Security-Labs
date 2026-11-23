# Gün 50 — Idempotency Anahtarı Süresi ve Tekrar Kullanımı

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](expiry_tombstone_demo.py)

## 49. günden devam
Önceki gün eski idempotency anahtarının normalizasyon kuralını koruduk. Peki bu anahtar **zaman aşımına uğrarsa** ve sunucu kaydı silerse?

**TTL (Time To Live):** kaydın geçerli kalacağı süre. **Tombstone:** eskiden kullanılmış kimliği hatırlatan kayıt. **Replay:** aynı işlemin yeniden gönderilmesi.

Bu uygulamada kabul edilen anahtar 10 zaman birimi boyunca geçerli. Aynı istek bu sürede `REPLAY`; farklı içerik `KEY_CONFLICT`. Süre dolunca `EXPIRED_KEY` dönüyor ve eski anahtar **yeni işlem diye tekrar uygulanmıyor**. Yeni ve ayrı bir anahtarla güncel sürüme işlem yapılabiliyor.

## Çalıştır
```bash
python3 labs/50-idempotency-key-expiry-and-reuse-tombstones/expiry_tombstone_demo.py
```

## Sorular
Süresi dolan anahtar tamamen unutulursa ne olur? Tombstone ne işe yarar? Gerçek API'de kayıtlar ne kadar saklanmalı ve neden transaction gerekir?

## Sınırlar
Gerçek API, veritabanı veya dağıtık sistem içermez; zaman ve veri sentetiktir.
