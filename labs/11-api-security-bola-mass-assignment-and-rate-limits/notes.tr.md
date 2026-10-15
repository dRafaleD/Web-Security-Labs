# Gün 11 — API Güvenliği: BOLA, Mass Assignment ve Rate Limit Tasarımı

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

Bu gün önceki labların üzerine inşa edilen, yalnızca yerel ve zararsız eğitim verisi kullanan uygulamalı bir çalışmadır. Kodun her varsayımını incele; çıktıları otomatik güvenlik kanıtı sayma.

## Öğrenme hedefleri

- Object-level authorization
- BOLA test design
- Mass assignment
- Authentication vs authorization
- Rate-limit models
- Response safety
- Negative testing
- Operational controls

## Veri akışı ve tehdit modeli

```text
controlled training input
        ↓
parser / evaluator / analyst
        ↓
security or evidence check
        ↓
observable result
        ↓
review assumptions and limits
```

## 1. Object-level authorization

Her okuma/güncellemede sahiplik kontrolü yap; ID tek başına erişim hakkı vermez.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 2. BOLA test design

Kendi kaydı ve başkasının kaydını karşılaştır; sızdırmayan ret cevabı bekle.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 3. Mass assignment

Yalnız açıkça izinli JSON alanları değişebilmeli; owner/role değişimini engelle.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 4. Authentication vs authorization

Sunucuda doğrulanmış kimlik kullan; istemcinin ayrıcalık iddiasına güvenme.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 5. Rate-limit models

Kimlik başına istek kotası, zaman penceresi ve dağıtık sayaç tasarla; demo gerçek middleware değil.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 6. Response safety

Kontrollü 400/404 dön; kayıt içeriği ve stack trace sızdırma.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 7. Negative testing

Başka sahip, izinsiz güncelleme, beklenmeyen alan ve yanlış türü test et.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## 8. Operational controls

Audit, kapsam, yetki iptali, pagination ve kötüye kullanım tespitini ek katman olarak düşün.

**Görev:** Bu kontrolün hangi yanlış yorum veya güven sınırı ihlalini önlediğini bir örnekle açıkla.

## Uygulama

Yalnızca repo içindeki dosyaları kullan. Bu örnek üretim ortamına kurulacak güvenlik servisi değildir.

```bash
python3 api_demo.py
```

## Test matrisi

| Senaryo | Beklenen | Neden |
|---|---|---|
| Valid training input | Kabul / eşleşme | Baseline |
| Wrong owner or header | Ret / eşleşmeme | Scope / structure |
| Truncated or missing field | Kontrollü hata | Input validation |
| Unrelated benign sample | Yanlış alarm yok | False-positive awareness |

## Alıştırmalar

1. Örneği çalıştır ve çıktıyı kaydet.
2. İlk varsayımını not et.
3. Olumlu senaryoyu doğrula.
4. Bir negatif senaryo ekle.
5. İkinci negatif senaryo ekle.
6. Bir sınır değeri dene.
7. İlgili kontrolü kaynak kodunda bul.
8. Gözlem ve çıkarımı ayrı yaz.
9. Tek bir kontrolü çalışma kopyasında değiştir.
10. Bütün senaryoları tekrar test et.
11. Sonuçların sınırlamalarını yaz.
12. Bir sayfalık kısa analiz raporu hazırla.

## Tekrar soruları

1. Bu labda hangi güven sınırı var?
2. Hangi veri kullanıcı tarafından kontrol ediliyor?
3. Olumlu testin amacı ne?
4. Negatif testin amacı ne?
5. Çıktı neyi gerçekten kanıtlıyor?
6. Çıktı neyi kanıtlamıyor?
7. En kritik input hangisi?
8. Bir sınır değeri örneği ver.
9. Fail-closed davranış nedir?
10. Bu labı prod ortamına doğrudan almak neden riskli?
11. Bir false positive senaryosu düşün.
12. Bir false negative senaryosu düşün.
13. Log hangi alanları taşımalı?
14. Hangi kişisel veri gereksiz?
15. Sürüm bilgisi niçin kaydedilir?
16. Kontrol değişince hangi testler tekrar koşulmalı?

## Mini projeler

1. Bir yeni negatif test ve beklenen çıktı ekle; çalıştırıp belgele.
2. Bir güvenlik varsayımını çalışma kopyasında boz; hangi testin yakaladığını açıkla.
3. Kaynak, hash, araç sürümü, komut, gözlem ve sınırlamalardan oluşan kısa rapor yaz.

## Özet

Kendi aracının gerçek davranışını ölç; sentetik örneği aşırı genelleme. Güvenlik kararı, izin ve adli çıkarım bağımsız doğrulama gerektirir.
