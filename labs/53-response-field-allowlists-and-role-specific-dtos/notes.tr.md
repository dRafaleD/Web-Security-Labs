# Gün 53 — Yanıt Alanı İzin Listesi ve Role Özel DTO

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](response_dto.py)

52. günde nesne yetkilendirmesi yaptık. Bugün izin sonrasında açık DTO alan listesi kullanıyoruz. Sahip title ve status, auditor yalnızca title görür. Yetkisiz kullanıcı boş 404 alır. internal_note ve sonradan eklenen özel alan otomatik olarak yanıta girmez.

**Alıştırma:** sahip DTO'suna izinli açıklama alanı ekle ve yanıt anahtarlarını test et. Başka tenant için hayalî kayıt ekleyip sınırları doğrula. Alan izin listesinin neden nesne yetkilendirmesi yerine geçmediğini açıkla. Dokuz kontrol vardır; gerçek HTTP, veritabanı veya üçüncü taraf sistem yoktur.

## Çalıştır
```bash
python3 labs/53-response-field-allowlists-and-role-specific-dtos/response_dto.py
```
