# Gün 6 — Authorization ve Access Control Temelleri

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

Authentication kullanıcının kimliğini belirledikten sonra authorization'ın ne yaptığını anlamak ve her protected resource/action için access-control kararının server tarafından uygulanması gerektiğini öğrenmek.

Bu lab:

- authentication vs authorization
- subject, object ve action
- object-level authorization
- function-level authorization
- role ve ownership
- 401 vs 403
- deny-by-default
- server-side enforcement
- IDOR/BOLA kavramları
- güvenli local access-control testi

konularını kapsar.

Eklenen Flask uygulaması küçük ve savunma odaklıdır. Gerçek servislere saldırmayı değil, doğru authorization check'lerinin nasıl düşünülmesi gerektiğini gösterir.

## 1. Authentication authorization değildir

Day 5'ten:

```text
Authentication -> Sen kimsin?
Authorization  -> Ne yapmana izin var?
```

Bir kullanıcı doğru şekilde authenticate edilmiş olsa bile belirli resource'a erişme yetkisi olmayabilir.

```text
Alice login olur
    ↓
identity biliniyor
    ↓
Alice Bob'un private profile'ını ister
    ↓
server ownership/permission kontrol eder
    ↓
deny
```

Login'in geçerli olması sonraki request'in authorized olduğu anlamına gelmez.

## 2. Subject, object ve action

Access control için üç soru:

```text
Subject -> request'i kim yapıyor?
Object  -> hangi resource hedefleniyor?
Action  -> hangi işlem isteniyor?
```

Örnek:

```text
Subject: user 1
Object:  profile 1
Action:  read
```

Authorization kararı sadece URL'ye değil bu kombinasyona bağlıdır.

## 3. Object-level authorization

Uygulamada:

```text
/profiles/1
/profiles/2
```

olduğunu düşün.

User 1'in profile 2'nin varlığını veya ID'sini bilmesi erişim izni vermez.

Server şuna benzer policy uygulamalıdır:

```text
requester owner mı?
        OR
requester izinli privileged role'e sahip mi?
```

Bu object-level authorization'dır.

## 4. IDOR / BOLA kavramı

**IDOR**, insecure direct object reference problemleri için yaygın kullanılan terimdir. API security tarafında **BOLA**, Broken Object Level Authorization anlamına gelir.

Savunma açısından temel ders:

> Object identifier hiçbir zaman tek başına authorization control olarak görülmemelidir.

ID, UUID, filename veya path değiştiğinde server-side permission check atlanmamalıdır.

Identifier resource'u bulur; authorization ise requester'ın o resource'a erişip erişemeyeceğine karar verir.

## 5. Function-level authorization

Access control işlemlere de uygulanır.

```text
/profile        -> normal user function
/admin/report   -> administrator function
```

Browser'da admin button'ını gizlemek yeterli değildir. Client görünür UI kullanmadan HTTP request oluşturabilir.

Server:

```text
request -> subject belirle -> permission kontrol et -> action
```

akışını enforce etmelidir.

## 6. Client-side check security boundary değildir

JavaScript user experience için control gizleyebilir:

```text
if not admin:
    hide admin button
```

Fakat client-side state client'ın kontrolündedir.

```text
client-side check -> UX
server-side check -> security decision
```

Client-side kontrol ek savunma/UX sağlayabilir fakat tek enforcement noktası olamaz.

## 7. 401 ve 403

### 401 Unauthorized

İsmi biraz kafa karıştırıcıdır. Genellikle gerekli authenticated identity'nin kurulamadığını, credential'ın eksik/geçersiz olduğunu ifade eder.

```text
"Bu request için geçerli authenticated identity yok."
```

### 403 Forbidden

Server request'i/identity'yi anlar fakat operation'a izin vermez.

```text
"Kim olduğunu biliyorum ama bunu yapamazsın."
```

Gerçek uygulamalar bilgi sızıntısını azaltmak için error davranışını farklı tasarlayabilir; status code tek başına security model değildir.

## 8. Role-Based Access Control

Basit RBAC:

```text
student -> normal features
analyst -> analysis features
admin   -> administrative features
```

Permission'lar role'lere bağlanır.

RBAC policy yönetimini kolaylaştırabilir ama her problemi çözmez. Aynı role sahip iki user yine sadece kendi private record'larına erişebiliyor olabilir.

Bu yüzden role check yanında object ownership de gerekebilir.

## 9. Ownership check

Yaygın policy:

```text
allow if:
    requester object'in owner'ı
    OR requester explicit admin permission'a sahip
otherwise:
    deny
```

Exact policy uygulamaya bağlıdır.

Ownership bilgisi trusted server-side data'dan gelmelidir. Client'ın gönderdiği `owner=true` gibi bir değer güvenilir authorization kaynağı değildir.

## 10. Deny by default

Güçlü zihinsel model:

```text
matching permission yok
        ↓
       deny
```

Her şeyi default allow edip sonradan engellemek yerine izin verilen durumları tanımla; policy'ye uymayan request'i reddet.

Yeni route/resource eklenirken accidental exposure riskini azaltır.

## 11. Local Flask labı

Gerekirse:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

Çalıştır:

```bash
python safe_app.py
```

Uygulama yalnızca:

```text
127.0.0.1:5000
```

üzerinde listen eder.

`X-Training-User` sadece local lab için identity selector'dır. **Gerçek authentication değildir** ve production authentication tasarımı olarak kullanılmamalıdır.

## 12. Training identity'leri

```text
1  -> student    -> user
2  -> analyst    -> user
99 -> admin-demo -> admin
```

Identity kontrolü:

```bash
curl -i -H "X-Training-User: 1" http://127.0.0.1:5000/me
```

Header olmadan:

```bash
curl -i http://127.0.0.1:5000/me
```

Status code farkını gözlemle.

## 13. Object-level check

User 1 kendi profile'ını ister:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/profiles/1
```

Beklenen: allowed.

User 1 profile 2'yi ister:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/profiles/2
```

Beklenen: `403 Forbidden`.

Buradaki ders “ID değiştirerek bir yere saldırmak” değildir. Client geçerli object ID gönderse bile server'ın ownership/permission check yapması gerektiğini görmektir.

## 14. Administrative function check

Normal user:

```bash
curl -i -H "X-Training-User: 1" \
  http://127.0.0.1:5000/admin/report
```

Beklenen: `403`.

Training admin:

```bash
curl -i -H "X-Training-User: 99" \
  http://127.0.0.1:5000/admin/report
```

Beklenen: allowed.

Bu function-level authorization örneğidir.

## 15. Sadece frontend kontrolü neden yetmez?

Frontend normal user için `/admin/report` linkini hiç göstermiyor olabilir.

Bu iyi UI davranışıdır ama endpoint yine server-side role check'e ihtiyaç duyar. HTTP request UI'dan bağımsız oluşturulabilir.

```text
hidden button != protected endpoint
```

## 16. Authorization tutarlı olmalı

Yaygın engineering problemi: aynı resource'a ulaşan bir route korunurken diğer route'un unutulması.

Policy olarak düşün:

```text
her protected read
her protected write
her protected delete
her privileged action
        ↓
authorization decision
```

Framework helper, middleware veya policy layer gibi merkezi mekanizmalar teknolojiye göre duplicated/inconsistent check riskini azaltabilir.

## 17. Client'tan gelen role bilgisine güvenme

Güvensiz tasarım fikri:

```text
POST /report
role=admin
```

Server sadece client “admin'im” dedi diye privilege vermemelidir.

Role/ownership bilgisi trusted authenticated session veya server-side state'ten türetilmelidir.

## 18. Access-control logları

Faydalı defensive log alanları:

- authenticated subject identifier
- requested resource/action
- allow/deny sonucu
- timestamp
- ilgili policy reason

Password, session token veya gereksiz sensitive personal data loglama.

Tekrarlanan denied request security telemetry olabilir ama malicious behavior demeden önce context gerekir.

## 19. Access-control review checklist

Protected endpoint için sor:

```text
1. Requester kim?
2. Hangi resource/action isteniyor?
3. Permission data nereden geliyor?
4. Check server-side mı?
5. Object ownership kontrol ediliyor mu?
6. Role/function permission kontrol ediliyor mu?
7. Hiçbir rule izin vermiyorsa ne oluyor?
8. Equivalent route'lar tutarlı korunuyor mu?
9. Denial uygun şekilde loglanıyor mu?
10. Allowed ve denied case test ediliyor mu?
```

## Alıştırmalar

1. Local Flask app'i başlat.
2. Training identity olmadan `/me` iste ve status'u incele.
3. User 1 ile kendi profile'ına eriş.
4. User 1'in user 2 profile'ına erişemediğini doğrula.
5. Normal user'ın `/admin/report` erişiminin reddedildiğini doğrula.
6. Training admin'in admin report'a erişebildiğini doğrula.
7. Source içinde object-level authorization check'i bul.
8. Function-level authorization check'i bul.
9. Admin button gizlemenin neden yeterli olmadığını açıkla.
10. Allowed owner, denied non-owner ve allowed admin için üç test case yaz.

## Sorular

1. Authentication ve authorization farkı nedir?
2. Subject, object ve action ne demektir?
3. Object ID neden authorization mekanizması değildir?
4. IDOR/BOLA'nın savunma açısından temel fikri nedir?
5. Privileged function neden server-side korunmalıdır?
6. 401 ve 403 arasındaki pratik fark nedir?
7. RBAC neden ownership check'e hâlâ ihtiyaç duyabilir?
8. Deny-by-default ne demektir?
9. Role neden doğrudan client input'tan alınmamalıdır?
10. Neden hem allowed hem denied path test edilmelidir?

## Ana çıkarım

```text
authenticated identity
        ↓
subject + object + action
        ↓
server-side policy check
        ↓
allow veya deny
        ↓
consistent logging/testing
```

Authentication uygulamaya requester'ın kim olduğunu söyler. Authorization ise her protected operation için bu identity'nin ne yapabileceğine ayrıca karar vermelidir.
