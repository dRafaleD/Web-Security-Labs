# Gün 9 — File Upload Güvenliği, Content Validation, Storage Isolation ve Güvenli Serving

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç

File upload güvenliğini tek extension check değil, uçtan uca bir security pipeline olarak anlamak.

Bu gün upload trust boundary, filename, content validation, size limit, server-generated ID, isolated storage, hashing, safe retrieval, authorization, quarantine, parser riskleri ve logging konularını birlikte işler.

## 1. Upload untrusted data'dır

~~~text
client
  ↓
upload
  ↓
filename + bytes
  ↓
validation
  ↓
storage
  ↓
metadata
  ↓
authorized retrieval
~~~

Filename, Content-Type ve bytes client-controlled kabul edilmelidir.

## 2. Original filename path değildir

Original name display metadata olarak saklanabilir fakat doğrudan server path yapılmamalıdır.

~~~text
original name -> metadata
server ID -> storage identity
~~~

## 3. Extension ile content aynı şey değildir

.txt extension gerçek text garantisi değildir.

Lab:

- .txt extension,
- size limit,
- UTF-8 decode

kontrolü yapar.

Real formatlarda format-aware parser gerekebilir.

## 4. Content-Type proof değildir

Client text/plain diyebilir ama bytes farklı olabilir.

Content-Type yardımcı metadata'dır, security proof değildir.

## 5. Signature ve parser

Magic byte/header formatı tanımaya yardımcı olabilir fakat complete valid/safe file garantilemez.

Parser kullanılıyorsa parser da attack surface olur.

## 6. Size limit

Upload bandwidth, RAM, disk ve parser/scanner time tüketir.

Lab 256 KiB limit kullanır ve bounded read yapar.

## 7. Isolated storage

Upload'ları application code, template, script ve config directory'lerinden ayır.

~~~text
application/
uploads/
logs/
database/
~~~

## 8. Upload execute edilmemeli

~~~text
upload -> validate -> inert data -> controlled retrieval
~~~

mantığı tercih edilir.

## 9. Object ID kullan

Client internal path seçmesin.

~~~text
/files/<object-id>
~~~

Server ID'den metadata ve trusted stored filename bulsun.

## 10. Path safety authorization değildir

İki ayrı soru sor:

1. Path storage dışına çıkabiliyor mu?
2. Requester bu object'e authorized mı?

İkisi farklı problemdir.

## 11. Hash

SHA-256 artifact identity, duplicate comparison ve audit için faydalıdır.

Hash file'ın safe olduğunu kanıtlamaz.

## 12. Quarantine / scanning

~~~text
upload
  ↓
quarantine
  ↓
validate
  ↓
scan
  ↓
policy
  ↓
publish
~~~

Clean scanner result kesin safe guarantee değildir.

## 13. Archive ve image riskleri

Archive expanded size, nesting ve internal path riskleri taşır.

Image parser/resizer da attack surface olabilir.

Size/dimension limit, updated parser, re-encoding ve isolation düşünülebilir.

## 14. Local lab

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
python safe_upload_demo.py
~~~

Harmless file:

~~~bash
printf "hello upload lab\n" > demo.txt
curl -F "file=@demo.txt" http://127.0.0.1:5000/upload
~~~

ID, original name, size ve SHA-256 gözlemle.

## 15. ID ile retrieval

~~~bash
curl -OJ http://127.0.0.1:5000/files/<ID>
~~~

Client internal storage path'i bilmez/seçmez.

## 16. Negative test

Local app'te:

- empty,
- wrong extension,
- oversized,
- invalid UTF-8

deneyerek policy'nin predictable fail ettiğini doğrula.

## 17. Logging

Object ID, user, original name, size, SHA-256, validation sonucu ve timestamp gibi alanlar loglanabilir.

Gereksiz file content loglama.

## 18. Mini challenge — ownership

Metadata'ya owner ekle ve retrieval'da training identity kontrol et.

Bunun validation değil authorization olduğunu açıkla.

## 19. Mini challenge — quarantine

pending / approved / rejected state ekle.

Sadece approved file download olsun.

## 20. Mini challenge — image pipeline

PNG/JPEG için request, validation, parser, storage, authorization ve serving katmanlarını tasarla.

Extension'a tek başına güvenme.

## 21. Checklist

~~~text
1. Filename path olarak trusted mı?
2. Size bounded mı?
3. Actual content validate ediliyor mu?
4. Storage isolated mı?
5. Upload executable olabilir mi?
6. Server ID kullanılıyor mu?
7. Retrieval authorize ediliyor mu?
8. Archive limitli mi?
9. Parser güncel/izole mi?
10. Hash var mı?
11. Quarantine gerekiyor mu?
12. Internal path leak oluyor mu?
~~~

## Alıştırmalar

1. App'i çalıştır.
2. Valid text upload et.
3. Hash'i doğrula.
4. ID ile file al.
5. Empty file test et.
6. Wrong extension test et.
7. Oversized file test et.
8. Original vs stored name açıkla.
9. Extension vs content açıkla.
10. Path safety vs authorization açıkla.
11. Quarantine flow tasarla.
12. Image upload flow tasarla.

## Sorular

1. Upload neden untrusted?
2. Original filename neden storage path olmamalı?
3. Extension neden yetersiz?
4. Content-Type neden yetersiz?
5. Size limit neden önemli?
6. Storage isolation neden önemli?
7. Object ID neden faydalı?
8. Hash ne işe yarar?
9. Clean scanner result neden garanti değildir?
10. Archive hangi ek riskleri getirir?
11. Image parser neden attack surface olabilir?
12. Validation ve authorization neden ayrıdır?

## Ana çıkarım

~~~text
untrusted file
    ↓
limit + validate
    ↓
server-generated identity
    ↓
isolated storage
    ↓
quarantine / scan
    ↓
authorization
    ↓
controlled serving
~~~

File upload security tek extension check değil, bütün pipeline'dır.
