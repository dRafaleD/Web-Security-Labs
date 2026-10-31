# Gün 28 — Content-Type Doğrulama ve MIME Sniffing

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Content-Type Doğrulama ve MIME Sniffing** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Yüklenen dosyaların `Content-Type` başlığına veya uzantısına güvenme; ilk baytları da kontrol et.
2. Kullanıcı içeriğini açık bir tür ve `X-Content-Type-Options: nosniff` ile sun; tarayıcılar tahmin etmesin.
3. Bildirilen türü tespit edilenle karşılaştır ve uyuşmazlıkları reddet.

## Kavramsal ayrımlar
- Magic byte'lar hızlı bir kontroldür, dosyanın tam doğrulaması değil.
- Yüklemedeki HTML veya SVG gibi aktif içerik ayrı ele alınmalıdır.
- Mümkünse yüklemeleri ayrı bir origin'den sun.

## Lab uygulaması
Önce `mime_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 mime_demo.py
~~~


## Görevler
1. Hangi yüklemelerin reddedileceğini tahmin et.
2. Demoyu çalıştırıp nedenleri not et.
3. Resim olarak bildirilmiş bir HTML dosyası ekle ve sonucu kontrol et.
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
