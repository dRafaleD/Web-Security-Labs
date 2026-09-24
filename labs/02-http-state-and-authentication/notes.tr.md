# Gün 2 — HTTP Methodları, Header'lar, Cookie'ler, Session ve Kimlik Doğrulama

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

HTTP request'i yalnızca tanımaktan bir adım ileri gitmek. Bu lab methodlar, header'lar, cookie'ler, session'lar, authentication, authorization, browser storage ve önemli güvenlik attribute'larını inceler.

Alıştırmalar gözlem odaklıdır ve browser veya kendi local server'ını kullanır.

## 1. HTTP methodları

| Method | Tipik amaç |
| --- | --- |
| GET | Kaynak almak |
| POST | Veri göndermek/oluşturmak |
| PUT | Kaynağı değiştirmek/güncellemek |
| PATCH | Kısmi güncelleme yapmak |
| DELETE | Silme talep etmek |
| HEAD | Response body olmadan header'ları istemek |
| OPTIONS | Desteklenen iletişim seçeneklerini/methodları sormak |

Method adı tek başına **authorization sağlamaz**. Server, mevcut kullanıcının istenen işlemi yapmaya yetkili olup olmadığına ayrıca karar vermelidir.

## 2. Request yapısı

```http
POST /login HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
User-Agent: ExampleBrowser

username=eren&password=example
```

Ayrı bölümlere dikkat et:

```text
request line
headers

body
```

Buradaki credential'lar yalnızca dummy eğitim verisidir.

## 3. Faydalı request header'ları

### Host

Hedef hostu belirtir.

### User-Agent

Client yazılımı hakkında bilgi verir.

### Accept

Client'ın kabul edebildiği response formatlarını belirtir.

### Content-Type

Body'nin formatını açıklar:

```http
Content-Type: application/json
```

### Authorization

Kullanılan authentication scheme'e göre credential veya token taşıyabilir.

Gerçek token, cookie, password, API key veya session identifier'larını bu repoya asla commit etme.

## 4. Faydalı response header'ları

Örnek:

```http
Content-Type: text/html
Content-Length: 1234
Cache-Control: no-store
Set-Cookie: session=...
```

Response header'ları browser davranışını, caching'i, cookie'leri ve güvenlik kontrollerini etkileyebilir.

İleride Content-Security-Policy ve Strict-Transport-Security gibi header'ları daha ayrıntılı inceleyebiliriz.

## 5. Cookie'ler

Server browser'dan cookie saklamasını isteyebilir:

```http
Set-Cookie: theme=dark
```

Browser daha sonraki request'te geri gönderebilir:

```http
Cookie: theme=dark
```

Cookie'ler tercih, identifier veya session ile ilgili değerler saklayabilir.

Browser'ın saklaması bir cookie'yi otomatik olarak gizli yapmaz.

## 6. Önemli cookie attribute'ları

### Secure

```http
Set-Cookie: session=example; Secure
```

Browser'a cookie'yi normal browser kuralları altında yalnızca güvenli HTTPS bağlantılarında göndermesini söyler.

### HttpOnly

```http
Set-Cookie: session=example; HttpOnly
```

Normal client-side JavaScript'in cookie'yi okumasını engeller. Bazı XSS senaryolarının etkisini azaltırken özellikle önemlidir.

### SameSite

```text
SameSite=Strict
SameSite=Lax
SameSite=None
```

Cookie'nin cross-site request'lerde ne zaman gönderileceğini etkiler ve CSRF savunmalarıyla ilgilidir.

Modern browserlarda `SameSite=None` normalde `Secure` ile birlikte kullanılır.

## 7. Cookie ve session aynı şey değildir

Yaygın bir tasarım:

```text
Browser
   |
   | Cookie: session_id=abc123
   v
Server
   |
   | abc123 -> server-side session data
   v
Logged-in state
```

Browser yalnızca identifier tutarken anlamlı session state server tarafında olabilir.

Self-contained token kullanan başka mimariler de vardır; her uygulamanın aynı çalıştığını varsayma.

## 8. Authentication ve authorization

**Authentication:**

```text
Sen kimsin?
```

**Authorization:**

```text
Ne yapmaya yetkin var?
```

Bir kullanıcı başarıyla login olabilir fakat admin sayfasına erişmeye yetkili olmayabilir.

Bu fark ileride access-control açıklarını öğrenirken çok önemli olacaktır.

## 9. Browser lab — cookie ve header incele

Kendi local uygulamanı veya incelemekte rahat olduğun normal bir siteyi kullan.

Developer Tools:

```text
Network -> bir request seç -> Headers
```

Bul:

- method
- path
- request headers
- response headers
- status code
- Content-Type

Ardından browser'ın storage/application panelinden seçilen origin'in cookie'lerini incele.

Gerçek session değerlerini repoya yazma veya screenshot olarak paylaşma.

Sadece attribute isimlerini veya sanitize edilmiş örnekleri kaydet.

## 10. Local HTTP lab

Boş bir practice klasöründe:

```bash
python3 -m http.server 8000
```

Sonra:

```bash
curl -i http://127.0.0.1:8000/
```

`-i`, response header'larını body ile birlikte gösterir.

HEAD isteği:

```bash
curl -I http://127.0.0.1:8000/
```

Verbose:

```bash
curl -v http://127.0.0.1:8000/
```

Verbose çıktı client'ın gönderdiği ve server'ın döndürdüğü satırları ayırmayı kolaylaştırır.

## 11. GET ve HEAD karşılaştır

```bash
curl -i http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/
```

Karşılaştır:

- status
- headers
- response body

HEAD, GET'e karşılık gelen header'ları response body'yi taşımadan almak için tasarlanmıştır.

## 12. Küçük bir cookie labı oluştur

`cookie_server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header(
            "Set-Cookie",
            "training_session=demo123; HttpOnly; SameSite=Lax"
        )
        self.end_headers()
        self.wfile.write(b"Harmless cookie lab\n")

HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

Çalıştır:

```bash
python3 cookie_server.py
```

Ziyaret et:

```text
http://127.0.0.1:8000/
```

Developer Tools üzerinden response'u ve cookie attribute'larını incele.

Bu bilerek dummy bir cookie'dir. Authentication değildir ve secret içermez.

## 13. curl ile incele

```bash
curl -i http://127.0.0.1:8000/
```

Şunu bul:

```http
Set-Cookie: training_session=demo123; HttpOnly; SameSite=Lax
```

Not: Küçük server HEAD implement etmiyorsa `curl -I` yerine `curl -i` kullan.

## 14. Güvenlik mantığı

Varsayımsal cookie:

```http
Set-Cookie: session=abc; Secure; HttpOnly; SameSite=Lax
```

Her attribute'un ne sağladığını düşün.

Tek bir attribute'u komple güvenlik çözümü olarak görme:

- `Secure` cookie'nin transportuyla ilgilidir.
- `HttpOnly` script erişimini sınırlar.
- `SameSite` bazı cross-site gönderim davranışlarını kontrol eder.
- server yine güçlü session management ve authorization uygulamalıdır.

Güvenlik birden fazla kontrolün birlikte çalışmasıyla oluşur.

## 15. Mini alıştırmalar

### A — Header'lar

Developer Tools ile beş request/response header'ı bul ve her birinin amacını tek cümleyle açıkla.

### B — Methodlar

Local server'da GET ve HEAD'i karşılaştır.

### C — Cookie

Local cookie server'ı çalıştır ve şunları bul:

- cookie name
- cookie value
- HttpOnly
- SameSite

Bu HTTP-only localhost alıştırmasında neden `Secure` bilerek eklenmedi?

### D — Authentication / authorization

```text
Alice başarıyla login olur.
Alice /admin ister.
Server 403 Forbidden döndürür.
```

Hangi adım authentication, hangisi authorization ile ilgilidir?

## Sorular

1. GET ile POST kavramsal olarak nasıl farklıdır?
2. POST kullanmak veriyi otomatik olarak güvenli yapar mı?
3. Request header ve response header arasındaki fark nedir?
4. `Set-Cookie` ne yapar?
5. `HttpOnly` ne işe yarar?
6. `Secure` ne işe yarar?
7. SameSite neden cross-site request'ler açısından önemlidir?
8. Authentication ile authorization arasındaki fark nedir?
9. Gerçek session ID'leri neden GitHub'a commit edilmemelidir?
10. Açıkları öğrenmeden önce normal HTTP davranışını bilmek neden önemlidir?

## Ana çıkarım

Web güvenliği state ve trust ilişkisini anlamakla başlar.

```text
request
  ↓
method + path + headers + body
  ↓
authentication
  ↓
session/state
  ↓
authorization kararı
  ↓
response
```

İleride web açıklarını incelerken aynı parçalar uygulamanın varsayımlarının ve güvenlik kontrollerinin nerede bozulduğunu anlamana yardımcı olacak.
