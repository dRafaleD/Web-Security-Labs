# Gün 38 — JSON Şema Doğrulaması ve Mass Assignment Savunması

[English](notes.md) · [Türkçe](notes.tr.md) · [Çevrimdışı Python lab](schema_guard_demo.py)

## 37. günden devam
Önceki gün JSON gövdesinin **geçerli olup olmadığını** kontrol etmiştik. Peki geçerli JSON içindeki her alana güvenebilir miyiz? Hayır. İstemci tarafından gönderilen bütün alanların sunucu nesnesine doğrudan aktarılmasına **mass assignment (toplu alan atama)** riski eşlik eder.

Örneğin `{"id":7,"action":"read","is_admin":true}` geçerli JSON'dur. Ama `is_admin` alanı üzerinden kullanıcı kendi yetkisini belirleyemez. İstemci girdileri için **izin verilen alanların listesi (allowlist)** uygulanmalı.

## Katmanları ayıralım
1. **Ayrıştırma:** Hatalı UTF-8, geçersiz JSON veya yinelenen anahtarlar reddedilir (37. günde işlendi).
2. **Şema:** Yalnızca iki alan kabul ediyoruz: `id` (tam sayı) ve `action` (`read` veya `list`). `owner`, `role`, `is_admin` gibi ek anahtarlar reddedilir.
3. **Nesne düzeyinde yetkilendirme:** `id` değeri doğru olsa bile başka kullanıcıya ait kaynağa erişim engellenmelidir. Bu problem IDOR/BOLA ile ilişkilidir.
4. **İş mantığı:** Şema ve yetkiyi geçen bir isteğin ne yapabileceğine de sunucu karar verir.

Örnekte `alice` ile `bob` adlı iki hayalî kullanıcı ve onlara ait kaynaklar var. **Kullanıcı kimliğini JSON'dan almıyoruz**; doğrulanmış oturum bağlamını temsil eden ayrı parametreden alıyoruz.

## Çalıştırma
```bash
python3 schema_guard_demo.py
```
Python standart kütüphanesi yeterli. Kod gerçek sunucu kurmaz veya dosya değiştirmez. Geçerli istek, fazladan yetki alanı, sahte sahip bilgisi, yanlış veri tipi, `true` değerinin tamsayı sanılması, geçersiz işlem ve başkasının kaynağına erişim vakaları test edilir.

## Mini görevler
1. Python'da `bool` değerinin `int` ile ilişkisi neden şema kontrolünde önemlidir?
2. `**request.json` ile tüm alanları model nesnesine aktarmak nasıl risk yaratır?
3. Şeması doğru olan istekte BOLA/IDOR nasıl oluşabilir?
4. `write` işlemini önce varsayılan olarak reddet, ardından açık yetki kuralı tasarla.
5. Gerçek uygulamada oturum ve rol bilgisini nereden almalısın?
6. Hata mesajlarında hangi iç bilgileri göstermemeliyiz?

## Güvenlik sınırı
Bu örnek gerçek kimlik doğrulama veya üretim ortamı API'si değil, **yetki ve şemayı ayrı değerlendiren** yerel bir eğitim modelidir. Şemanın doğru olması, otomatik erişim yetkisi vermez.
