# Gün 3 — Browser Güvenliği, Same-Origin Policy, CORS ve CSRF Temelleri

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Browser'ın web originlerini nasıl ayırdığını, cross-origin erişimin neden sınırlandığını, CORS'un bu sınırı kontrollü biçimde nasıl gevşettiğini ve otomatik credential kullanımının CSRF açısından neden önemli olduğunu anlamak.

Bu lab ilerideki vulnerability odaklı çalışmalar için kavramsal temel oluşturur.

## 1. Origin nedir?

Browser güvenliğinde origin şu üç parçaya dayanır:

```text
scheme + host + port
```

Örnek:

```text
https://example.com
https://api.example.com
http://example.com
https://example.com:8443
```

Bunların hepsi aynı origin değildir. Scheme, host veya effective port değişirse origin değişebilir.

## 2. Same-Origin Policy

Same-Origin Policy (SOP), browser'ın temel güvenlik sınırlarından biridir.

Basitleştirilmiş haliyle bir origin altında çalışan JavaScript'in başka bir origin'e ait hassas içeriği serbestçe okumasını sınırlar.

Böyle bir sınır olmasaydı zararlı bir sayfa kullanıcının login olduğu başka sitelerdeki verileri okuyabilirdi.

SOP, "bütün cross-origin request'ler imkânsızdır" demek değildir. Browser normal kullanımda birçok cross-origin request gönderebilir; asıl önemli sınırlardan biri script'in response'u okuyabilmesidir.

## 3. Same-site ve same-origin

Aynı kavram değillerdir.

Şimdilik:

```text
same-origin -> scheme + host + port karşılaştırması
same-site   -> SameSite cookie gibi mekanizmalarda kullanılan daha geniş site kavramı
```

## 4. CORS

CORS = Cross-Origin Resource Sharing.

Server'ın belirli cross-origin response'ların hangi originler tarafından okunabileceğini browser'a bildirmesini sağlayan mekanizmadır.

Örnek response:

```http
Access-Control-Allow-Origin: https://example-client.test
```

Bu "web güvenliğini kapatmak" değildir; browser'a belirli bir cross-origin policy bildirir.

## 5. Basit örnek

JavaScript:

```text
https://app.example
```

üzerinde çalışırken:

```text
https://api.example
```

adresine request gönderirse iki adres farklı origin'dir.

Script'in response'u okuyabilmesi browser kurallarına ve API'nin CORS response'una bağlıdır.

## 6. Preflight request

Bazı cross-origin request'lerde browser önce OPTIONS gönderir:

```http
OPTIONS /api/profile HTTP/1.1
Origin: https://app.example
Access-Control-Request-Method: PUT
```

Server policy bilgisi dönebilir:

```http
Access-Control-Allow-Origin: https://app.example
Access-Control-Allow-Methods: GET, PUT
```

Bu ön kontrole **preflight** denir. Her cross-origin request preflight gerektirmez.

## 7. Origin header

```http
Origin: https://app.example
```

Server bunu CORS ile ilgili kararlarında kullanabilir.

`Origin` ve `Host` aynı değildir:

```text
Host   -> request'in hedeflediği server/virtual host
Origin -> request'i başlatan context ile ilişkili security origin
```

## 8. Credential ve cookie'ler

Cookie kuralları izin verdiğinde browser cookie'leri request'e otomatik ekleyebilir.

Bu önemli bir güvenlik sorusu doğurur:

> Browser kullanıcının credential'larını otomatik gönderiyorsa server, state-changing işlemin başka bir site tarafından istenmeden tetiklenmediğini nasıl anlar?

Buradan CSRF kavramına geçiyoruz.

## 9. CSRF kavramı

CSRF = Cross-Site Request Forgery.

Temel risk şu koşullarda ortaya çıkar:

1. kullanıcı hedef siteye authenticated durumdadır,
2. browser ilgili credential'ları otomatik ekler,
3. başka bir site state-changing request tetikleyebilir,
4. hedef uygulama işlemin gerçekten kullanıcı tarafından istendiğini yeterince doğrulamaz.

Savunma açısından:

```text
authenticated request
        +
state-changing action
        +
request origin/intention validation
```

Mimariye göre CSRF token, SameSite cookie ve origin doğrulaması gibi kontroller kullanılabilir.

Tek bir mekanizmanın bütün tasarımları çözdüğünü varsayma.

## 10. CORS ve CSRF aynı değildir

Yeni başlayanlarda sık karıştırılır.

**CORS**, browser JavaScript'inin CORS kuralları altında cross-origin response'u okuyup kullanabilmesiyle ilgilidir.

**CSRF**, authenticated kullanıcının browser'ına istemediği bir işlemi yaptırmakla ilgilidir.

```text
CORS != CSRF koruması
```

## 11. Local origin deneyi

İki ayrı terminalde:

```bash
python3 -m http.server 8000
```

ve başka klasörde:

```bash
python3 -m http.server 9000
```

Karşılaştır:

```text
http://127.0.0.1:8000
http://127.0.0.1:9000
```

Host aynı olsa da port farklı olduğu için origin farklıdır.

Amaç browser kontrolünü bypass etmek değil, origin kimliğini anlamaktır.

## 12. Header gözlemleme

Developer Tools üzerinden kendi uygulamanı veya normal bir siteyi incele.

Varsa şunları ara:

```text
Origin
Referer
Access-Control-Allow-Origin
Access-Control-Allow-Methods
Vary
```

Her response'un CORS header içermesi gerekmez. Olmaması tamamen normal olabilir.

Sadece sanitize edilmiş gözlemleri kaydet.

## 13. Zararsız CORS demo server

`cors_server.py`:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

ALLOWED_ORIGIN = "http://127.0.0.1:8000"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.end_headers()
        self.wfile.write(b'{"message":"CORS training response"}')

HTTPServer(("127.0.0.1", 9000), Handler).serve_forever()
```

Çalıştır:

```bash
python3 cors_server.py
```

Response'u incele:

```bash
curl -i http://127.0.0.1:9000/
```

Şunu bul:

```http
Access-Control-Allow-Origin: http://127.0.0.1:8000
```

Unutma: curl header'ı gösterir fakat CORS enforcement browser davranışıdır.

## 14. Security header'ları policy sinyalidir

Şimdilik şu isimleri tanı:

```text
Content-Security-Policy
Strict-Transport-Security
X-Content-Type-Options
Referrer-Policy
Access-Control-Allow-Origin
```

Detaylarını ileride ayrı ayrı inceleyeceğiz.

## 15. Mini alıştırmalar

### A — Origin karşılaştırması

Hangileri same-origin?

```text
https://example.com       vs https://example.com/profile
https://example.com       vs http://example.com
https://example.com       vs https://api.example.com
https://example.com       vs https://example.com:8443
```

### B — CORS header

Local CORS server'ı çalıştır ve allowed origin'i bul.

### C — Browser incelemesi

Doğal olarak oluşuyorsa bir request/response içinde `Origin` veya CORS header'ı bul. Üçüncü taraf sistemlere zorla request üretme.

### D — Mantık

JavaScript'in kullanıcının login olduğu diğer bütün sitelerin response'larını okuyabilmesinin neden tehlikeli olacağını açıkla.

## Sorular

1. Origin'i hangi üç bileşen belirler?
2. Same-Origin Policy neden vardır?
3. SOP bütün cross-origin network request'leri tamamen engeller mi?
4. `Access-Control-Allow-Origin` ne bildirir?
5. CORS preflight nedir?
6. `Host` ve `Origin` arasındaki fark nedir?
7. Otomatik gönderilen cookie'ler CSRF açısından neden önemlidir?
8. CORS ve CSRF neden farklı kavramlardır?
9. Aynı host üzerindeki 8000 ve 9000 portları same-origin midir?
10. CORS header'ını curl ile görmek neden curl'ün CORS uyguladığı anlamına gelmez?

## Ana çıkarım

```text
origin
  ↓
browser security boundary
  ↓
cross-origin request
  ↓
gerektiğinde CORS policy
  ↓
credential/cookie
  ↓
server-side authorization ve anti-CSRF kontrolleri
```

Bu sınırları anlamak ileride XSS, CSRF, CORS misconfiguration ve authentication lablarını çok daha anlaşılır hale getirir.
