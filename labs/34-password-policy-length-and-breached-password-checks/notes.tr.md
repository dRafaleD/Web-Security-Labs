# Gün 34 — Parola Politikası: Uzunluk ve Sızdırılmış Parola Kontrolleri

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Parola Politikası: Uzunluk ve Sızdırılmış Parola Kontrolleri** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Karmaşık bileşim kuralları yerine asgari bir uzunluğu (ör. 12 karakter) tercih et.
2. Bilinen sızdırılmış veya çok yaygın parolalar listesinde geçen parolaları reddet.
3. Kötü bir parolanın basit varyasyonları da yakalansın diye normalize edilmiş biçimde karşılaştır.

## Kavramsal ayrımlar
- Uzun bir parola da yeniden kullanılmış veya sızdırılmış olabilir; liste kontrolü bunu kapsar.
- Politika hız sınırlama ve MFA'yı tamamlar, onların yerini tutmaz.
- Kontrol ettiğin parolayı asla loglama.

## Lab uygulaması
Önce `policy_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 policy_demo.py
~~~


## Görevler
1. Beş paroladan hangilerinin kabul edileceğini tahmin et.
2. Demoyu çalıştırıp her nedeni not et.
3. Listedeki bir parolanın basit bir varyasyonunu ekle ve yakalanıp yakalanmadığına bak.
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
