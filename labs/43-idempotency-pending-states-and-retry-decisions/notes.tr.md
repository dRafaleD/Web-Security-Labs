# Gün 43 — Idempotency PENDING Durumu ve Tekrar İstek Kararları

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](pending_demo.py)

## 42. günden devam
İki istemcinin aynı sürümü güncellemeye çalışmasını gördük. Peki **ilk istek bitmeden aynı istek yeniden gelirse** ne yapacağız?

**PENDING:** işlem başladı ama henüz tamamlanmadı. **IN_PROGRESS:** aynı isteğin hâlen işlendiği bilgisi. **COMMITTED:** güncelleme başarıyla kaydedildi. **REPLAY:** tamamlanmış isteğin tekrar gönderilmesi. **KEY_CONFLICT:** aynı anahtarın farklı içerikle yeniden kullanılması.

Modelde ilk geçerli istek PENDING kaydı açar. Aynı anahtar ve içerikle gelen tekrar **IN_PROGRESS** döner, ikinci kez yazmaz. İlk işlem tamamlandıktan sonra aynı istek **REPLAY** olur. İşlem başlamış ama iptal edilmişse bekleyen kayıt silinir ve yeniden denenebilir.

## Çalıştırma
~~~bash
python3 labs/43-idempotency-pending-states-and-retry-decisions/pending_demo.py
~~~

## Sorular
PENDING ve COMMITTED farkı nedir? Aynı isteğin ikinci defa çalıştırılmasını nasıl önleriz? Sunucu çökmesi durumunda neden kalıcı ve atomik veri kaydı gerekir? `IN_PROGRESS` sonucu başarı garantisi verir mi?

## Sınırlar
Gerçek API, veritabanı veya eşzamanlı thread yoktur. Üretim ortamında transaction, crash recovery ve yetki kontrolleri şarttır.
