# Gün 26 — Oturum Boşta Kalma ve Mutlak Zaman Aşımı

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Oturum Boşta Kalma ve Mutlak Zaman Aşımı** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Boşta kalma zaman aşımı, etkinlik olmayan bir süreden sonra oturumu bitirir; mutlak zaman aşımı etkinlikten bağımsız olarak sabit bir ömürden sonra bitirir.
2. İkisini de her istekte sunucuda kontrol et; yalnızca çerezin süresinin dolması uygulama değildir.
3. Yetki değişimlerinde oturum kimliğini yenile ve çıkışta sunucudaki kaydı sil.

## Kavramsal ayrımlar
- Boşta kalma zaman aşımı, başında kimse olmayan cihazlarda çalınmış oturumun etkisini sınırlar; mutlak zaman aşımı sürekli kullanılan çalıntı oturumun etkisini sınırlar.
- Zaman aşımları güvenlik ile kullanıcı sürtünmesi arasında bir tercihtir; veri hassasiyetine göre seç.
- İstemci saati güvenilmezdir; sunucu zamanını kullan.

## Lab uygulaması
Önce `timeout_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 timeout_demo.py
~~~


## Görevler
1. Demoyu çalıştırmadan önce her isteğin sonucunu tahmin et.
2. Çalıştırıp hangi isteklerin neden reddedildiğini not et.
3. Boşta kalma süresini 60 saniye yap ve etkisini anlat.
4. Etkinliğin oturumu mutlak sınırın ötesine uzatamadığını doğrulayan bir assertion ekle.
5. Çalıntı oturum kimliğine sahip bir saldırganın her zaman aşımı türünden nasıl yararlandığını anlat.
6. Bağımsız bir kontrol öner (oturumu cihaz sinyallerine bağlamak veya hassas işlemlerde yeniden kimlik doğrulama).

## Kısa sınav
1. Girdi nereden geliyor ve onu kim kontrol ediyor?
2. Doğrudan gözlenen ile çıkarım yapılan arasındaki fark nedir?
3. Hangi varsayımlar gerçek sistemde geçerli olmayabilir?
4. Hangi kanıt tek başına yetersiz kalır?
5. Bir otomatik test neyi kontrol etmeli?

## Etik ve sınırlamalar
Yalnızca izinli sistemlerde ve sentetik verilerle çalış. Bu örnek tam bir tespit veya koruma ürünü değildir.
