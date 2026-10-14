# Gün 10 — SSRF Temelleri, URL Ayrıştırma, Redirect ve Egress Güvenliği

[English](notes.md) · [Türkçe](notes.tr.md)

**Amaç:** Day 8 path ve Day 9 upload trust boundary bilgisini server-side URL fetch güvenliğine taşımak.

**Önemli:** Python örneği sadece URL policy kararı verir, gerçek HTTP/DNS isteği GÖNDERMEZ. Production-ready SSRF koruması değildir.

## 1. SSRF threat model

SSRF, user-controlled verinin server'ın istek gönderdiği hedefi beklenmedik biçimde değiştirmesidir. Server iç servisleri görebilir; dış kullanıcı bu servislere doğrudan erişemeyebilir. Risk yalnız URL'nin tuhaf olması değil, isteğin hangi ağ yetkisiyle gönderildiğidir.

## 2. URL bileşenleri ve parser

URL; scheme, authority/host, port, path, query ve fragment içerir. Yetki kararını parsed hostname üzerinden ver, string contains ile değil. Hostname'in uzun başka bir domain içinde görünmesi yetki sağlamaz.

## 3. Scheme ve port sınırı

İşlev için gerçekten gereken protocol/port dışında izin verme. Bu lab yalnız HTTPS/443 kabul eder. Genel amaçlı fetcher, beklenmeyen protocol ve iç servislere erişim açabilir.

## 4. Userinfo ve belirsizlik

URL userinfo, fragment, Unicode ve encoding içerebilir. İhtiyacın olmayan syntax'ı reddet ve tutarlı parser kullan. Tarayıcıda nasıl göründüğüne bakarak host yetkisi verme.

## 5. Allowlist ve blocklist

Bilinen partner servisi için exact host allowlist daha anlaşılır. 'Şüpheli host yasak' blocklist alternatif temsil ve yeni hedefleri kaçırabilir. Exact match faydalıdır ama runtime DNS risklerini tek başına çözmez.

## 6. DNS resolution ve rebinding

Hostname beklenmeyen private, loopback veya link-local IP'ye çözülebilir; doğrulama ile bağlantı arasında değişebilir. Production'da gerçek resolved/connected IP, IPv4/IPv6, rebinding ve egress kuralları dikkate alınmalı. Demo bağlantı kurmaz.

## 7. Redirect zinciri

İzinli ilk URL disallowed hedefe redirect yapabilir. Redirect kapatılmalı veya her hop için aynı policy uygulanmalı. İlk adresi kontrol edip client'ın keyfî hedefe gitmesine izin verme.

## 8. Egress ve segmentasyon

Application URL kontrolü outbound firewall, network isolation, sınırlı DNS ve minimum credential ile desteklenmeli. Uygulama mantığında hata varsa ağ katmanı zararı azaltabilir.

## 9. Metadata ve iç kaynaklar

Cloud metadata, admin paneli ve loopback servisi server'ın erişebildiği fakat user'ın keyfî seçmemesi gereken kaynaklar olabilir. Lab bunlara hiçbir istek göndermez; sadece güven sınırını açıklar.

## 10. Authorization ve log

Allowed URL bile ilgili user'ın yetkili işine uygun olmalı. Policy kararı ve request ID logla; secret/token içeren URL'leri gereksiz kaydetme. URL allowlist kullanıcı yetkilendirmesinin yerine geçmez.

## Yerel uygulama

Python 3 standard library yeterli:

```bash
python3 url_policy.py
python3 -m unittest -v test_url_policy.py
```

Eğitim allowlist'i gerçek sitelere istek göndermez: `reports.example.test` ve `status.example.test`. Script bunların yalnız host, scheme, port ve URL syntax uygunluğunu inceler. Gerçek DNS çözülmesi, redirect ve socket bağlantısı **yoktur**.

### Karar akışı

```text
untrusted URL
   ↓
parse + syntax validation
   ↓
scheme / port / exact host allowlist
   ↓
[training only: policy decision]
   ↓
production requires DNS/IP/redirect/egress enforcement
```

### Mini challenge

1. `reports.example.test.evil.test` neden host allowlist'inden geçmez açıkla.
2. Bağlantı açmadan redirect için ikinci URL'ye tekrar policy uygulayan bir fonksiyon tasarla.
3. Production HTTP client'da DNS rebinding riskine karşı hangi katmanların gerekli olduğunu çiz.
4. Uygulamanın neden real secret, admin token veya raw URL loglamaması gerektiğini açıkla.

### Alıştırmalar

1. URL components ayır.
2. Host ve path farkını anlat.
3. Tests çalıştır.
4. Protocol kısıtlamasını incele.
5. Port kontrolünü analiz et.
6. Userinfo reddini açıkla.
7. Subdomain/suffix riskini anlat.
8. IP literal kontrolünü yorumla.
9. DNS rebinding riskini tarif et.
10. Redirect policy eklemenin mantığını yaz.
11. Egress firewall senaryosu tasarla.
12. SSRF triage raporu yaz.

### Sorular

1. SSRF nedir?
2. Hangi trust boundary geçilir?
3. Host parsing neden kritik?
4. String contains niye yetersiz?
5. Allowlist ne kazandırır?
6. Blocklist neden eksik?
7. Scheme sınırı niye gerekli?
8. Userinfo nedir?
9. DNS rebinding nedir?
10. IPv6 neden düşünülmeli?
11. Redirect nasıl risk yaratır?
12. Egress control ne sağlar?
13. Metadata service örneği neden hassas?
14. URL check authorization mıdır?
15. Bu demo neden production-ready değildir?

**Ana çıkarım:** SSRF'yi önlemek yalnız URL string filtrelemek değildir; application policy, gerçek bağlantı hedefi ve ağ egress sınırları birlikte gerekir.
