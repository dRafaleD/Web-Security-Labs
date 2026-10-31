# Gün 32 — Web Loglarında Hassas Veri Karartma

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Web Loglarında Hassas Veri Karartma** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Sorgu dizeleri, başlıklar ve gövdeler sık sık token ve parola içerir; bunları olduğu gibi loglama.
2. Bilinen hassas anahtarlar için alan adına göre, token benzeri değerler için desene göre karart.
3. Gizlenecek alanların kara listesi yerine loglanacak alanların izin listesini tercih et.

## Kavramsal ayrımlar
- Sonradan karartma bir emniyet ağıdır; veriyi en baştan toplamaktan kaçın.
- URL yolları da sıfırlama token'ı gibi sırlar taşıyabilir.
- Karartmayı sentetik sırlarla test et.

## Lab uygulaması
Önce `log_redact_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 log_redact_demo.py
~~~


## Görevler
1. Karartılmış log satırını tahmin et.
2. Demoyu çalıştırıp hiçbir sır kalmadığını doğrula.
3. Karartıcının tanımadığı bir başlık ekle ve ne olduğuna bak.
4. Bir güvenlik özelliği için assertion ekle.
5. Bir negatif senaryo ve bir yanlış pozitif ihtimali yaz.
6. Bağımsız bir doğrulama yöntemi öner.

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
