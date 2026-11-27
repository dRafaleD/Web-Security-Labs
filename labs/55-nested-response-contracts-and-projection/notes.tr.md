# Gün 55 — İç İçe API Yanıt Sözleşmeleri ve Alan Projeksiyonu

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](nested_dto.py)

54. günde üst düzey yanıt sözleşmesini denetledik. Bugün profile nesnesinin tamamını kopyalamak yerine izinli alanlardan yeni iç içe nesne oluşturuyoruz. Üst alanın izinli olması tüm alt alanları yetkili yapmaz. Sekiz sözleşme ve üç projeksiyon kontrolü fazla/eksik alan ve tür hatalarını kapsar. Hayalî bir iç alan ekle, çıktıda olmadığını doğrula; izinli yeni görüntüleme alanı eklerken olumlu/olumsuz testleri güncelle. Önceden yetkilendirme yapılmış varsayılır. Gerçek sunucu veya veri yoktur.

## Çalıştır
```bash
python3 labs/55-nested-response-contracts-and-projection/nested_dto.py
```
