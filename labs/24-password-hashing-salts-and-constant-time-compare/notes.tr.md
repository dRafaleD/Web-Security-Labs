# Gün 24 — Parola Hashleme, Salt ve Sabit Zamanlı Karşılaştırma

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Parola Hashleme, Salt ve Sabit Zamanlı Karşılaştırma** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Parolalar scrypt gibi yavaş ve salt'lı bir hash gerektirir; hızlı genel amaçlı hash yetersizdir.
2. Parola başına benzersiz rastgele salt, aynı parolaların farklı hash üretmesini sağlar.
3. Digest'leri sabit zamanlı bir fonksiyonla karşılaştır.

## Kavramsal ayrımlar
- Bir verinin bulunması, o veriye dayanarak kurulan bütün iddiaları doğrulamaz.
- Önce güven sınırını ve hangi girdiye kimin hükmettiğini belirle.
- Pozitif ve negatif kontrolleri birlikte çalıştır; bir ölçümün sınırlarını kaydet.

## Lab uygulaması
Önce `password_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 password_demo.py
~~~

## Görevler
1. Kodu inceleyerek beklediğin çıktıyı tahmin et.
2. Çalıştırıp girdileri ve gerçek çıktıları not et.
3. Zararsız bir girdiyi değiştir; farkı ve sebebini açıkla.
4. İlk güvenlik özelliği için assertion ekle.
5. Bir negatif senaryo ve bir yanlış pozitif ihtimali yaz.
6. İkinci bir bağımsız doğrulama yöntemi öner.

## Kısa sınav
1. Bu örnekte giriş verisi nereden geliyor?
2. Hangi davranış doğrudan gözlendi?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
