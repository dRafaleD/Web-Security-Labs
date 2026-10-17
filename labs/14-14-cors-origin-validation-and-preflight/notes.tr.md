# Gün 14 — CORS Origin Doğrulama, Preflight ve Credential Sınırları

[English](notes.md) · [Türkçe](notes.tr.md)

## Hedef
CORS Origin Doğrulama, Preflight ve Credential Sınırları konusunu tamamen yerel ve zararsız örneklerle öğrenmek. Gözlemlenen bulguyu yorumdan ayırmak ve kesin olmayan sonuçları abartmamak.

## Temel kavramlar
1. **same-origin policy versus CORS:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
2. **Origin and Access-Control-Allow-Origin:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
3. **preflight OPTIONS request:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
4. **credentials and allowlisted origins:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
5. **Vary: Origin:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.
6. **CORS is not server-side authorization:** Kavramın amacını, güven sınırını, olası hatalarını ve hangi durumda kullanılacağını açıklayın.

## Uygulama
Lab klasöründe `cors_demo.py` dosyasını inceleyin ve şu komutları sırasıyla uygulayın:

```bash
python3 cors_demo.py
```

```bash
curl -i -H 'Origin: http://localhost:3000' http://127.0.0.1:8081/
```

```bash
curl -i -H 'Origin: https://untrusted.example' http://127.0.0.1:8081/
```

```bash
curl -i -X OPTIONS -H 'Origin: http://localhost:3000' -H 'Access-Control-Request-Method: GET' http://127.0.0.1:8081/
```

**Beklenen sonuç:** Allowlisted Origin receives CORS response headers; unrelated origins do not.

## Analiz defteri
Kullandığınız araç sürümünü, komutu, girdiyi, gördüğünüz çıktıyı, beklenmeyen olayları ve olası açıklamaları kaydedin. Ölçülen veri ile çıkarımı ayrı başlıklar altında yazın.

## Uygulama görevleri
1. Orijinal örneği çalıştırıp çıktıyı kaydedin.
2. Zararsız bir girdiyi değiştirerek sonucu önceden tahmin edin.
3. Bir negatif test ekleyin ve gerçekten hangi kontrolün başarısız olduğunu belirleyin.
4. Başlangıç dosyasına dönüp regresyon testi yapın.
5. İki olası yanlış pozitif açıklaması üretin.
6. Sonucu doğrulayacak bağımsız bir kanıt kaynağı önerin.
7. Belirsizlikleri açıkça yazan kısa bir rapor hazırlayın.

## Tekrar soruları
1. same-origin policy versus CORS nedir, ne işe yarar, neyi garanti etmez?
2. Origin and Access-Control-Allow-Origin nedir, ne işe yarar, neyi garanti etmez?
3. preflight OPTIONS request nedir, ne işe yarar, neyi garanti etmez?
4. credentials and allowlisted origins nedir, ne işe yarar, neyi garanti etmez?
5. Vary: Origin nedir, ne işe yarar, neyi garanti etmez?
6. CORS is not server-side authorization nedir, ne işe yarar, neyi garanti etmez?
7. Sonucun güvenilirliğini nasıl artırırsınız?
8. Hangi kontrolü otomatik regresyon testine dönüştürürsünüz?

## Kapsam
Bu lab yalnızca izinli, sentetik veriler içindir. Tek bir bulguyu kesin saldırı kanıtı saymayın.
