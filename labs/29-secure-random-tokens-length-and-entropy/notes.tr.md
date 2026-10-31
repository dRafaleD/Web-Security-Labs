# Gün 29 — Güvenli Rastgele Token'lar: Uzunluk ve Entropi

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Güvenli Rastgele Token'lar: Uzunluk ve Entropi** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Oturum kimlikleri ve sıfırlama token'ları kriptografik olarak güvenli bir rastgele kaynaktan gelmelidir.
2. Hesapları koruyan token'lar için 128 bit rastgelelik yaygın bir asgaridir.
3. Zaman damgası, sayaç veya tohumlanmış genel amaçlı bir üreteç gibi öngörülebilir değerler güvenli değildir.

## Kavramsal ayrımlar
- Uzunluk tek başına token'ı güvenli yapmaz; rastgelelik kaynağı yapar.
- Rastgele görünen bir token, bilinen bir tohumla tamamen belirlenebilir.
- Uzun ömürlü token'ların sunucuda yalnızca hash'lerini sakla.

## Lab uygulaması
Önce `token_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 token_demo.py
~~~


## Görevler
1. Hangi üretecin tekrarlanabilir token ürettiğini tahmin et.
2. Demoyu çalıştırıp iki çıktıyı karşılaştır.
3. 16 karakterlik bir hex token'ın kaç bit olduğunu hesapla.
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
