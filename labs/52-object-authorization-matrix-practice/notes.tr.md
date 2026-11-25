# Gün 52 — Uygulama Günü: Nesne Yetkilendirmesi ve Yanıt Sözleşmesi

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](authorization_matrix.py)

Yerel bir fonksiyon ile nesne seviyesinde yetkilendirmeyi çalışıyoruz. Kimlik güvenilen kullanıcı listesinden gelir. GET için aynı tenant içindeki sahip ve admin, PATCH için yalnızca sahip yetkilidir. Bulunmayan veya gizlenen kayıtlar bu hayalî uygulamada aynı 404 sonucunu verir.

| İstek | Durum |
|---|---:|
| Sahip kendi kaydını okur | 200 |
| Sahip kendi kaydını günceller | 200 |
| Başka üye kaydı okumak ister | 404 |
| Aynı tenant admin okur | 200 |
| Admin başkasının kaydını güncellemek ister | 403 |
| Başka tenant kaydını okumak | 404 |
| Bilinmeyen kullanıcı | 401 |
| Desteklenmeyen HTTP metodu | 405 |

**Alıştırmalar:** 15 sonucu tahmin et. Tenant a içinde ikinci kayıt ekle, sahip ve sahip olmayan kullanıcı testleri yaz. Reddedilen okuma ile bulunmayan kayıt yanıtını karşılaştır. Aynı durum kodu neden tek başına tam gizlilik sağlamaz? Gerçek backend'de kimlik ve veritabanı kapsamı kontrolünü tasarla.

Beklenen özet: 15 cases + 1 response-consistency check passed. Gerçek HTTP sunucusu, dış sistem veya veri değişikliği yoktur.

## Çalıştır
```bash
python3 labs/52-object-authorization-matrix-practice/authorization_matrix.py
```
