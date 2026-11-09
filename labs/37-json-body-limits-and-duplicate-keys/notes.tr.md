# Gün 37 — JSON İstek Sınırları, Yinelenen Anahtarlar ve Ayrıştırıcı Güvenliği

[English](notes.md) · [Türkçe](notes.tr.md) · [Çevrimdışı Python alıştırması](json_guard_demo.py)

## Problem
Bir API'ye gelen `application/json` başlığı, gövdenin gerçekten geçerli ya da güvenli olduğunu **kanıtlamaz**. Çok büyük istekler, aşırı iç içe nesneler, aynı anahtarın iki kez kullanılması ve standart dışı sayılar uygulamanın beklenmedik davranmasına neden olabilir.

Örnek: `{"role":"reader","role":"admin"}`. İki farklı JSON ayrıştırıcısı aynı veriyi farklı yorumlayabilir. Bu nedenle kullanıcıdan gelen JSON'u yalnızca `json.loads` ile okumak yeterli bir güvenlik politikası değildir.

## Katmanlı kontrol sırası
1. Medya türünü kontrol et: bu çalışmada yalnızca `application/json`.
2. JSON'u işlemeye başlamadan **ham bayt uzunluğunu** sınırla. UTF-8'de karakter sayısı ile bayt sayısı aynı olmayabilir.
3. Geçersiz UTF-8, hatalı JSON, `NaN` ve `Infinity` değerlerini reddet.
4. Aynı nesnede yinelenen anahtarları kabul etme.
5. İç içe yapı derinliğini ve toplam düğüm sayısını ölç.
6. **Ek olarak** iş mantığına göre alan türlerini, yetkiyi ve kaynak erişimini doğrula.

Önemli ayrım: Bu örnekte derinlik ve düğüm kontrolleri **JSON ayrıştırıldıktan sonra** çalışıyor. Dolayısıyla ayrıştırıcının kendi bellek/CPU tüketimini tümüyle engellemiyor. Gerçek uygulamada web sunucusu, ağ geçidi ve streaming parser düzeyinde de sınırlar gerekir.

## Çalıştır
Sunucu, internet veya harici Python paketi gerekmez:
```bash
python3 json_guard_demo.py
```
Kod; geçerli nesne, yanlış Content-Type, büyük gövde, tekrar eden anahtar, bozuk UTF-8, standart dışı sayı ve fazla iç içe yapı örneklerini dener. Kararları yazdırır ve `assert` ile kontrol eder.

## Görevler
1. `len(body)` neden karakter saymaktan farklıdır?
2. Tekrarlanan `role` anahtarı güvenliği nasıl etkileyebilir?
3. Derinlik sınırını 2 yapıp hangi örneklerin reddedildiğini gözlemle.
4. `id` sadece tamsayı, `action` sadece `read` veya `list` olacak şekilde şema kontrolü ekle.
5. İstek zaman aşımı, sıkıştırılmış gövde ve hız sınırını hangi katmanda denetlemek gerekir?

## Kısıtlar
Bu çalışma çevrimdışı bir **doğrulama modeli**dir; gerçek bir HTTP sunucusunun transfer, buffering ve parser maliyetini kapsamaz. Güvenli JSON biçimi, otomatik olarak yetkili işlem anlamına gelmez.
