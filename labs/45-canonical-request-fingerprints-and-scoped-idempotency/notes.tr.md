# Gün 45 — Standart İstek Özeti ve Idempotency Kapsamı

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](canonical_idempotency_demo.py)

## 44. günden devam
Önceki gün worker'ların aynı işi iki kez yapmasını önlemek için **lease** ve **fencing token** kavramlarını gördük. Bugün sunucunun **aynı mantıksal isteği** nasıl tanıyacağını inceliyoruz.

**Canonicalization:** aynı anlama gelen verileri belirli standart sırada kodlama. **Request fingerprint:** kullanıcı, kaynak, sürüm ve istek içeriğini temsil eden özet. **Idempotency key:** mantıksal işlemi tanımlayan anahtar.

JSON nesnesinde `name` ve `active` alanları farklı sırayla gelse bile aynı içerik sayılmalı. Aynı anahtar ve aynı istek `REPLAY`; aynı anahtarla başka içerik `KEY_CONFLICT` olur. Kullanıcı yetkisi, sürüm ve izinli alanlar ayrıca doğrulanır.

## Çalıştır
~~~bash
python3 labs/45-canonical-request-fingerprints-and-scoped-idempotency/canonical_idempotency_demo.py
~~~

## Sorular
Alan sıralaması neden hash'i gereksiz yere değiştirmemeli? Veri doğrulamadan hash üretmek neden sakıncalı? Neden fingerprint bir erişim izni değildir?

## Sınırlar
Tek süreçli örnektir; gerçek API, transaction veya eşzamanlı işlem güvenliği sunmaz.
