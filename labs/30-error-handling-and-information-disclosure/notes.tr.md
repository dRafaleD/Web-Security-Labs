# Gün 30 — Hata Yönetimi ve Bilgi İfşası

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Hata Yönetimi ve Bilgi İfşası** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Kullanıcıya genel bir mesaj ve bir korelasyon kimliği göster; yığın izlerini, SQL'i ve yolları sunucu loglarında tut.
2. Var olan ve olmayan hesaplar için ayrı hata mesajları hangi hesapların var olduğunu sızdırır.
3. Üretimde debug modunu kapat ve hata yollarını test et.

## Kavramsal ayrımlar
- Korelasyon kimliği, iç detayı açmadan kullanıcı bildirimini log ile bağlar.
- Sadece mesaj değil, tutarlı zamanlama da hesap numaralandırma için önemlidir.
- Ham istisna metnini asla istemciye yansıtma.

## Lab uygulaması
Önce `errors_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 errors_demo.py
~~~


## Görevler
1. Her hata için kullanıcının ne göreceğini tahmin et.
2. Demoyu çalıştırıp yanıtı sunucu logu ile karşılaştır.
3. Yeni bir hata türü ekle ve onun da genel kaldığını doğrula.
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
