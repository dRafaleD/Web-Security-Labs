# Gün 42 — Eşzamanlı Tekrar İstekleri, Sürüm ve Idempotency

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](race_demo.py)

## 41. günden devam
Idempotency key ile süre sınırını öğrendik. Ancak **race condition (yarış durumu)** farklı bir problemdir: iki istemci aynı belge sürümünü okuyup neredeyse aynı anda değişiklik yapmak isterse ne olur?

Bu örnekte A ve B, belgenin sürümünü 2 olarak okur. A'nın işlemi sürümü 3 yapar. B eski sürüm 2 ile geldiği için reddedilir. A aynı isteği yeniden gönderirse **REPLAY** olur, tekrar güncelleme yapılmaz. Aynı anahtarla değişen istek **KEY_CONFLICT** sonucu verir.

**Compare-and-swap:** kaydı yalnızca beklenen sürüm hâlâ geçerliyse güncelleme. Gerçek sistemde belge değişikliği ile idempotency kayıtları **aynı veritabanı transaction'ında atomik** olarak yazılmalıdır.

## Çalıştırma
~~~bash
python3 labs/42-concurrent-retries-version-checks-and-idempotency/race_demo.py
~~~

## Sorular
İki istemci aynı sürümü gördüğünde yarış nasıl doğar? Güncelleme başarılı ama ledger yazımı başarısız olursa ne olabilir? Python'daki bu örnek neden gerçek atomiklik sağlamaz?

## Sınır
Gerçek HTTP, veritabanı veya thread kullanılmaz; sadece olası iki istek sırası simüle edilir.
