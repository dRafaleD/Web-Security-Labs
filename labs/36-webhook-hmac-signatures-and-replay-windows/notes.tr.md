# Gün 36 — Webhook HMAC İmzaları ve Replay Süresi

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](webhook_demo.py)

## Problem: webhook otomatik olarak güvenilir değildir
Ödeme sağlayıcısı veya CI sisteminden geldiği iddia edilen callback hâlâ **dışarıdan gelen bir HTTP isteğidir**. Uygulama durumunu değiştirmeden önce sağlayıcının tarif ettiği imza denetimi uygulanmalıdır.

## HMAC nedir?
**HMAC-SHA256**, gizli paylaşılan anahtar ile ham istek baytlarından mesaj doğrulama kodu üretir. Salt SHA-256 hash'i, göndericinin gizli anahtarı bildiğini göstermez. Karşılaştırmada `hmac.compare_digest` kullan.

**Önemli:** JSON'u ayrıştırıp yeniden yazdığında boşluklar ve bayt sırası değişebilir. İmza kontrolü, sağlayıcı kuralına göre **alınan ham baytlar** üzerinde yapılmalıdır. Gerçek secret'ı kaynak koda veya loga ekleme.

## Tekrar oynatma (replay)
İmzalanmış geçerli isteği tekrar göndermek, imzayı kendiliğinden bozmaz. Zaman penceresi eski istekleri engeller; fakat pencerenin içindeki tekrarlara karşı **event ID/nonce kayıt sistemi** ve idempotent işlem gerekir. Birden fazla sunucu varsa kayıt merkezi ve atomik olmalıdır.

## Uygulama
```bash
python3 webhook_demo.py
```
Yalnız sentetik baytlar ve **demo anahtarı** kullanılır. Program geçerli, içeriği değiştirilmiş, süresi bitmiş ve tekrar gönderilmiş örnekleri sınar. Gerçek webhook sağlayıcısının protokolünü uyguladığı iddia edilmez.

## Görevler
1. Mesajdaki tek bayt değişikliğinin imzayı neden bozduğunu açıkla.
2. Tekrar işlenmeyi hangi kontrol engelliyor?
3. Saat kaymasının zaman penceresine etkisini değerlendir.
4. Neden JSON parse/iş mantığından **önce** imza doğrulanır?
5. Sadece RAM'deki tekrar kayıtlarının çok sunuculu sistemlerdeki eksiğini yaz.

## Güvenlik ve sınırlar
Gerçek HTTP servisi, gerçek ödeme isteği veya kimlik bilgisi kullanılmaz. İmzanın geçerli olması, istenen **işlemin ayrıca yetkili olduğu** anlamına gelmez.
