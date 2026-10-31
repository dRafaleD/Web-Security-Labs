# Gün 27 — Request Smuggling: Başlık Belirsizliği Kontrolleri

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Request Smuggling: Başlık Belirsizliği Kontrolleri** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Bir istekte hem `Content-Length` hem `Transfer-Encoding` varsa iki sunucu isteğin nerede bittiği konusunda anlaşamayabilir.
2. Hangi başlığın geçerli olduğunu tahmin etmek yerine belirsiz istekleri uçta reddet.
3. Yinelenen veya bozuk uzunluk başlıkları da aynı şekilde reddedilir.

## Kavramsal ayrımlar
- Bu lab savunmaya yönelik bir doğrulayıcıdır; ön yüz ve arka uç ayrıştırıcılarını tutarlı tut.
- Uçtan uca HTTP/2'ye geçmek bu belirsizliklerin çoğunu ortadan kaldırır.
- Canlı trafikle değil, sentetik başlık listeleriyle test et.

## Lab uygulaması
Önce `ambiguity_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 ambiguity_demo.py
~~~


## Görevler
1. Hangi başlık kümelerinin reddedileceğini tahmin et.
2. Demoyu çalıştırıp ret nedenlerini not et.
3. Negatif Content-Length içeren bir istek ekle.
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
