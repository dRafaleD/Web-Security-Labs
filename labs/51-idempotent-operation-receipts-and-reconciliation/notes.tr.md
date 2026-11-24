# Gün 51 — Idempotent İşlem Makbuzları ve Uzlaştırma

[English](notes.md) · [Türkçe](notes.tr.md) · [Code](receipt_demo.py)

50. günde süresi dolan idempotency anahtarlarının eski işlemi yeniden uygulamasını önledik. Bugün işlem sonucundan emin olmayan istemci için yalnızca okuma yapan **işlem makbuzu sorgulamasını** ekliyoruz. Makbuz kullanıcı, kaynak ve işlem anahtarına bağlıdır. Geçmiş sürümün başarılı olması kaynağın şu an aynı durumda olduğunu göstermez. Sürüm geriye gitmiş görünüyorsa yeni yazma yapmak yerine inceleme istenir.

**Sorular:** Makbuz sorgulama ile işlemi tekrar uygulama neden farklı? Güncel yetki neden tekrar kontrol edilmeli? Veritabanında makbuz ile işlem hangi şekilde atomik tutulmalı?

Yetki ve sürüm değerleri güvenilen hayalî sunucudan gelir. Gerçek HTTP, veritabanı veya değişiklik işlemi yoktur.

## Çalıştır
```bash
python3 labs/51-idempotent-operation-receipts-and-reconciliation/receipt_demo.py
```
