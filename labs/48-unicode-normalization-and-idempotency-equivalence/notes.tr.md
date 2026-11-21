# Gün 48 — Unicode Normalizasyonu ve Idempotency Eşitliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](unicode_idempotency_demo.py)

## 47. günden devam
Önceki gün JSON'un boyutunu ve derinliğini sınırladık. Şimdi iki metnin **mantıksal olarak aynı istek** olup olmadığını inceliyoruz.

**Unicode NFC:** bazı farklı karakter dizilişlerini aynı standart gösterime dönüştürür. Örneğin `é` karakterinin tek kod noktası ile `e` + birleşen aksan gösterimi. **NFKC:** daha geniş uyumluluk dönüşümleri yapar; her API için uygun değildir. **Casefold:** büyük/küçük harf farkını birleştirebilir.

Örnekte NFC uygulanıyor; bu iki `Café` biçimi aynı idempotency isteği sayılıyor. Ama `café` ve `Café` ya da `①` ve `1` otomatik eşit kabul edilmiyor. Unicode kontrol/biçimlendirme karakterleri ve tekrar JSON anahtarları reddediliyor.

## Çalıştırma
```bash
python3 labs/48-unicode-normalization-and-idempotency-equivalence/unicode_idempotency_demo.py
```

## Sorular
NFC ile NFKC farkı nedir? Büyük-küçük harfi birleştirmek niçin her zaman doğru değildir? İki uygulama farklı normalizasyon kullanırsa aynı isteği nasıl yanlış yorumlayabilir?

## Sınırlar
Gerçek API veya veritabanı yoktur; Unicode politikasının örnek bir alt kümesidir.
