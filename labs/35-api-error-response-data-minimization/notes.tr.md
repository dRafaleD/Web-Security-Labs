# Gün 35 — Güvenli API Hata Yanıtları ve Veri Minimizasyonu

[English](notes.md) · [Türkçe](notes.tr.md) · [Pratik](error_demo.py)

## Hedef

Bu çalışma yalnızca izinli ve zararsız yerel örnekler üzerinden **Güvenli API Hata Yanıtları ve Veri Minimizasyonu** konusunu ele alır. Çıktıların doğrudan gözlem mi, yorum mu olduğunu ayırmayı hedefler.

## Temel bilgiler

1. Herkese açık API yanıtı stack trace, anahtar veya iç dosya yolu yerine kontrollü hata kodları içermelidir.

2. Ayrıntılı hata bilgisi saklama ve maskeleme kurallarıyla korunan sunucu loglarına aittir.

3. Doğru HTTP durum kodu ve istek ilişkilendirme kimliği, hassas veri sızdırmadan teşhise yardımcı olur.

## Uygulama

Önce dosyayı oku, sonucu tahmin et, ardından çalıştır:

```bash
python error_demo.py
```

Try inserting a fabricated exception message; verify the response never reflects it.

## Görevler

1. Beklenen ve gözlenen sonuçları karşılaştır.
2. Bir pozitif ve bir negatif örneği belgele.
3. Tek bir göstergeyle kesin sonuç çıkarmanın riskini açıkla.
4. Kodu zararsız bir sınır değerle değiştir ve testi tekrarla.

## Bilgi kontrolü

- Girdi hangi güven sınırını geçiyor?
- Hangi veri eksik veya yanlış yorumlanabilir?
- Gerçek sistemde hangi bağımsız doğrulama gerekir?

## Güvenlik ve sınırlar

Gerçek zararlı dosyalar, saldırı hedefleri veya üretim sistemleri kullanılmaz. Bu küçük eğitim örneği saha performansı garantilemez.
