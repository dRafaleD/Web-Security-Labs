# Gün 49 — Sürümlü Unicode Normalizasyonu ve Idempotency Tekrarları

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](policy_migration_demo.py)

## 48. günden devam
Önceki gün `Café` ile `Cafe + birleşik aksan` yazımını **NFC** normalizasyonuyla eşdeğer saydık. Peki uygulamanın bu kuralı zaman içinde **değişirse** eski idempotency anahtarlarına ne olur?

**Canonicalization policy:** eşitlik için kullanılan standartlaştırma kuralı. **Policy version:** bu kuralın sürümü. **Replay:** eski işlemin aynı anahtarla tekrarlanması.

Model başlangıçta `raw-v1` kullanır; metinler birebir karşılaştırılır. Sonra yeni istekler için `nfc-v2` politikasına geçilir. Ancak **eski key**, oluşturulduğu andaki `raw-v1` kuralını kullanmayı sürdürür. Yeni kural eski anahtarın anlamını sessizce değiştiremez.

## Çalıştır
```bash
python3 labs/49-versioned-unicode-canonicalization-and-idempotency-retries/policy_migration_demo.py
```

## Sorular
Eski key'e yeni normalizasyon uygulamak neden riskli? Unicode eşdeğerliği neden her API'de aynı değil? Gerçek sunucuda bu kayıtları neden atomik saklamalıyız?

## Sınırlar
Gerçek sunucu veya veritabanı bulunmaz; eğitim amaçlı yerel örnektir.
