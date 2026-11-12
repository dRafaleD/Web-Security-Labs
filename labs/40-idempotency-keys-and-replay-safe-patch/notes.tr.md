# Gün 40 — Idempotency Key ile Güvenli PATCH Tekrarı

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](idempotency_demo.py)

## 39. günden devam
Önceki gün, PATCH işleminde alan yetkisi ve sürüm kontrolü vardı. Şimdi düşün: sunucu güncellemeyi yaptı ama istemcinin bağlantısı kesildi. İstemci **aynı isteği tekrar** gönderdi. Değişiklik bir kez daha uygulanmalı mı?

**Idempotency key:** aynı mantıksal işlemi temsil eden benzersiz anahtar.
**Replay (tekrar):** aynı isteğin yeniden gönderilmesi.
**Request fingerprint:** aktör, hedef belge, beklenen sürüm ve isteğin içeriğinden üretilen özet.
**Optimistic concurrency:** verinin beklenen sürümle eşleşip eşleşmediğini kontrol etme.

## Nasıl çalışır?
Hayalî belgemiz `alice` kullanıcısına ait ve sürümü 2.

1. `request-001` ilk kez gelirse izinli alan güncellenir ve sürüm 3 olur.
2. Aynı anahtar ve **tam olarak aynı istek** yeniden gelirse önceki sonuç dönülür; sürüm yine 3 kalır.
3. Aynı anahtarla farklı içerik gelirse işlem reddedilir.
4. Başka kullanıcı bu anahtarı kullanarak belgeye erişemez.
5. Yeni anahtarla eski sürüm gönderilirse işlem yine reddedilir.
6. Doğru yeni istek sürüm 4'ü oluşturur; tekrar gönderilmesi ikinci güncelleme yapmaz.

**Önemli:** bu örnekte anahtar, gerçek bir yetkilendirme aracı değildir. Sunucu kimlik ve kaynak yetkisini önceden doğrulamalıdır.

## Çalıştırma
~~~bash
python3 labs/40-idempotency-keys-and-replay-safe-patch/idempotency_demo.py
~~~

## Alıştırmalar
1. İdempotency key neyi önler?
2. Anahtar neden kullanıcı ve veri içeriğine bağlanmalı?
3. Ağ zaman aşımı ile gerçek işlem hatası nasıl ayrılır?
4. İki paralel istek gelirse sadece bellekteki kayıt neden yetersiz kalabilir?
5. Gerçek servis neden kalıcı ve atomik bir veritabanı işlemi kullanmalı?

## Sınır
Bu eğitim kodu tek işlemli ve bellek içi bir modeldir. Gerçek HTTP, veritabanı veya kimlik bilgisi kullanılmaz.
