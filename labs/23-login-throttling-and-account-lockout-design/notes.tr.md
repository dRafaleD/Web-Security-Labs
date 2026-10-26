# Gün 23 — Giriş Sınırlama ve Hesap Kilitleme Tasarımı

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Giriş Sınırlama ve Hesap Kilitleme Tasarımı** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Başarısız girişleri kayan bir pencerede hem hesap hem kaynak IP bazında say.
2. Hangi kullanıcı adlarının var olduğunu belli etmemek için tek tip bir mesaj dön.
3. Kalıcı hesap kilidi, kurbanları dışarıda bırakmak için kötüye kullanılabilir; geçici pencere kullan ve IP sınırları ile MFA ile birleştir.

## Kavramsal ayrımlar
- Sınırlama tahmini yavaşlatır; güçlü parola ve MFA'nın yerini tutmaz.
- Yalnızca IP sınırı dağıtık denemelere karşı yetersizdir; yalnızca hesap sınırı kilitleme istismarına yol açar.
- Kilitli hesap, kilit süresi boyunca doğru parolayı bile reddetmelidir.

## Lab uygulaması
Önce `throttle_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 throttle_demo.py
~~~


## Görevler
1. Demoyu çalıştırmadan önce yazdırılacak üç mesajı tahmin et.
2. Çalıştırıp doğru parolanın ne zaman tekrar çalıştığını not et.
3. `window` değerini 60 saniyeye indir; saldırgan ve meşru kullanıcı için etkisini açıkla.
4. IP sınırının altında kaldıkça `alice` hatalarının aynı IP'den `bob`'u engellemediğini doğrulayan bir assertion ekle.
5. İki sınırın da altında kalan dağıtık bir saldırı anlat.
6. Destekleyici bir kontrol öner (MFA, sızdırılmış parola kontrolü, kilitleme artışı için alarm).

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
