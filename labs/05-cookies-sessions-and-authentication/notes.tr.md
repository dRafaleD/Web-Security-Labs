# Gün 5 — Cookie, Session ve Authentication Güvenliği

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Browser cookie'leri ve server-side session'ların login state'i nasıl tuttuğunu, authentication ile authorization farkını ve hangi cookie attribute'larının yaygın session risklerini azaltmaya yardımcı olduğunu öğrenmek.

Bu lab yalnızca local Flask uygulaması kullanır.

## 1. Session neden vardır?

HTTP protokol seviyesinde stateless'tir. Server iki request'in otomatik olarak aynı logged-in user'a ait olduğunu hatırlamaz.

Yaygın model:

```text
login request
    ↓
server identity doğrular
    ↓
session state oluşturur
    ↓
browser session cookie alır
    ↓
sonraki request cookie gönderir
    ↓
server request'i session ile ilişkilendirir
```

## 2. Cookie yapısı

```http
Set-Cookie: session=example; Path=/; HttpOnly; SameSite=Lax
```

Önemli attribute'lar:

- **Name / Value**
- **Domain**
- **Path**
- **Expires / Max-Age**
- **Secure**
- **HttpOnly**
- **SameSite**

## 3. HttpOnly

`HttpOnly`, cookie'nin normal client-side JavaScript API'lerinden okunmasını engeller.

Bazı XSS senaryolarında session theft etkisini azaltmak için defense in depth sağlar.

XSS açığını kendi başına çözmez.

## 4. Secure

`Secure`, browser'ın cookie'yi yalnızca güvenli HTTPS transport üzerinden göndermesini ister.

Önemli:

> Secure cookie değerini kendi başına encrypt etmez.

Transport'u TLS korur.

Bu localhost labı plain HTTP olduğu için Secure bilerek kapalıdır.

## 5. SameSite

```text
SameSite=Strict
SameSite=Lax
SameSite=None
```

Cross-site cookie gönderim davranışının bazı bölümlerini kontrol eder ve CSRF riskini azaltmaya yardımcı olabilir.

Tek başına bütün CSRF savunmalarının yerine geçmez.

## 6. Authentication ve authorization

Authentication:

```text
Sen kimsin?
```

Authorization:

```text
Neye yetkin var?
```

```text
user login olur
        ↓
authenticated
        ↓
/admin ister
        ↓
server role kontrol eder
        ↓
authorized değilse 403
```

Başarılı login her resource'a permission anlamına gelmez.

## 7. Session lifecycle

```text
create
  ↓
use
  ↓
gerektiğinde rotate
  ↓
expire / logout
  ↓
invalidate
```

Session çok uzun yaşarsa, doğru invalidate edilmezse veya authorization zayıf varsayımlara dayanırsa güvenlik problemi oluşabilir.

## 8. Local Flask lab

Gerekirse virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

Çalıştır:

```bash
python app.py
```

Aç:

```text
http://127.0.0.1:5000/
```

Uygulama sadece dummy local login kullanır ve gerçek credential içermez.

## 9. Session cookie'yi incele

Training form ile login ol.

DevTools:

```text
Application / Storage -> Cookies
```

Bak:

- cookie name
- Path
- HttpOnly
- SameSite
- Secure

Gerçek servislerdeki real cookie'leri repoya koyma.

## 10. curl ile gözlem

```bash
curl -i http://127.0.0.1:5000/
```

Dummy login ve cookie kaydetme:

```bash
curl -i -c cookies.txt   -X POST   -d "username=student"   http://127.0.0.1:5000/login
```

Cookie'yi tekrar kullan:

```bash
curl -i -b cookies.txt http://127.0.0.1:5000/profile
```

Client'ın request'ler arasında state taşımasını gösterir.

## 11. Logout

`/logout` çağır.

Sonra `/profile` tekrar iste.

Beklenen: session artık authenticated olarak tanınmamalı.

Session invalidation'ın authentication security içindeki yerini gösterir.

## 12. Session fixation kavramı

Session fixation; uygulamanın attacker tarafından bilinen pre-authentication session identifier'ını authentication sonrasında uygunsuz biçimde geçerli tutmasıyla ilişkili weakness sınıfıdır.

Defensive prensip:

> Untrusted pre-authentication session, uygun session handling olmadan privileged authenticated session'a dönüştürülmemelidir.

## 13. Session ID neden hassastır?

Session identifier bearer credential gibi davranıyorsa onu elinde bulunduran kişi session gibi davranabilir.

Bu yüzden:

- gereksiz session ID loglama,
- GitHub'a commit etme,
- transport'ta koru,
- doğru expire/invalidate et,
- cookie scope'u doğru ayarla.

## 14. Password notu

Demo bilinçli olarak gerçek password storage implement etmez.

Gerçek uygulamalarda plaintext password saklanmamalıdır. Password storage ayrı bir labda iyi bilinen password-hashing yöntemleriyle işlenecektir.

## 15. Mini alıştırmalar

1. Local app'e login ol.
2. DevTools'ta session cookie'yi bul.
3. HttpOnly ve SameSite değerlerini doğrula.
4. Bu HTTP localhost labında Secure'un neden kapalı olduğunu açıkla.
5. curl cookie jar ile `/profile` erişimini dene.
6. Logout sonrası authenticated state'in kaybolduğunu doğrula.
7. Authentication / authorization farkını açıkla.
8. Gerçek session value'larını nota koymanın neden riskli olduğunu açıkla.

## Sorular

1. Web application neden session state'e ihtiyaç duyar?
2. HttpOnly neyi sınırlar?
3. Secure neyi gerektirir?
4. SameSite bütün CSRF savunmalarının yerine geçer mi?
5. Authentication ve authorization farkı nedir?
6. Logout'ta session neden invalidate edilmelidir?
7. Session fixation temel olarak nedir?
8. Session ID neden hassas olabilir?
9. Real password neden plaintext saklanmamalıdır?
10. Neden session lifecycle sadece login ekranından daha önemlidir?

## Ana çıkarım

```text
identity verification
      ↓
session creation
      ↓
safe cookie attributes
      ↓
authorization checks
      ↓
rotation / expiry
      ↓
logout / invalidation
```
