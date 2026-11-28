# Gün 56 — Liste Yanıtı Sözleşmeleri ve Öğe Doğrulama

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](collection_contract.py)

55. günde iç içe yanıt alanlarını inceledik. Bugün en fazla üç öğeli hayalî bir sayfa için şema kontrolü yapıyoruz. count bu sayfadaki öğe sayısıdır. Her öğede yalnızca boş olmayan id ve title metinleri bulunur. Tekrarlı kimlik, fazla alan, yanlış tür ve sayaç farkı reddedilir. On bir sonucu tahmin et, üç farklı geçerli öğe içeren sayfa ekle. Şema kontrolü nesne yetkilendirmesi sağlamaz; count tüm veritabanı sayısı değildir. Gerçek HTTP sunucusu yoktur.

## Çalıştır
```bash
python3 labs/56-collection-response-contracts-and-item-validation/collection_contract.py
```
