# Gün 1 — HTTP Temelleri ve Request/Response Analizi

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Web güvenlik açıklarına geçmeden önce HTTP request/response modelini anlamak ve normal browser trafiğini incelemeyi öğrenmek.

## Temel model

Bir web sayfası açtığında:

```text
Browser
   |
   | HTTP request
   v
Web server
   |
   | HTTP response
   v
Browser
```

HTTPS, HTTP trafiğini aktarım sırasında TLS ile korur; ancak uygulama tarafında method, path, header, status code ve body gibi HTTP kavramları kullanılmaya devam eder.

## Basit bir HTTP request

Kavramsal olarak:

```http
GET / HTTP/1.1
Host: example.com
User-Agent: Browser
Accept: text/html
```

Önemli parçalar:

- **Method:** `GET` veya `POST` gibi hangi işlemin istendiğini belirtir
- **Path:** hangi kaynağın istendiğini belirtir
- **Headers:** request hakkındaki metadata'dır
- **Body:** request ile gönderilebilen isteğe bağlı veridir

## Basit bir HTTP response

Conceptually:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>...</html>
```

Important parts:

- **Status code:** request'in sonucunu belirtir
- **Headers:** response hakkındaki metadata'dır
- **Body:** döndürülen içeriktir

Yaygın status-code grupları:

```text
2xx -> başarılı
3xx -> yönlendirme
4xx -> istemci taraflı request problemi
5xx -> sunucu taraflı hata
```

## Lab 1 — Browser Developer Tools

Tarayıcının Developer Tools bölümünü aç ve **Network** sekmesini seç.

Şurayı ziyaret et:

```text
https://example.com/
```

Document request'i seç ve şunları incele:

- Request URL
- Request Method
- Status Code
- Request Headers
- Response Headers

Henüz hiçbir şeyi değiştirme. İlk hedef yalnızca browser ile server arasındaki konuşmayı okuyabilmek.

## Lab 2 — Request'leri karşılaştır

Sayfayı yenile ve ana document ile diğer kaynaklara giden request'leri incele.

Şunları sor:

- Ana document'i hangi request yüklüyor?
- Hangi HTTP method kullanılıyor?
- Hangi status code dönüyor?
- `Content-Type` nedir?
- `User-Agent` header'ını hangi taraf gönderiyor?

## İsteğe bağlı yerel alıştırma

Boş bir alıştırma klasöründe basit bir local server başlat:

```bash
python3 -m http.server 8000
```

Visit:

```text
http://127.0.0.1:8000/
```

Şimdi local request'i Developer Tools üzerinden incele.

Server kendi makinen üzerinde çalıştığı için temel request gözlemi için güvenli bir hedeftir.

## Burp Suite bağlantısı

İlerleyen lab'lerde Burp Suite'i intercepting proxy olarak kullanabiliriz.

Şimdilik şu akışı hatırla:

```text
Browser -> request -> server
Browser <- response <- server
```

Bir proxy bu iki tarafın arasına girerek izinli testlerde trafiğin incelenmesini sağlayabilir.

## Sorular

1. Sayfayı hangi HTTP method yükledi?
2. Hangi status code'u aldın?
3. Döndürülen içerik türünü hangi header açıklıyor?
4. Request header ile response header arasındaki fark nedir?
5. HTTPS, HTTP iletişimine ne ekler?

## Ana çıkarım

Açıkları öğrenmeden önce normal web trafiğini rahatça okuyabilir hale gel.

Her request için şunları sor:

```text
Kim gönderdi?
Hangi method kullanıldı?
Hangi path istendi?
Hangi header'lar vardı?
Body var mıydı?
Server ne döndürdü?
```

Bu sorular ileride yapacağımız web güvenliği analizlerinin temelini oluşturur.
