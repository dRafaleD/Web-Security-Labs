# Gün 31 — Bağımlılık Sabitleme ve Güvenlik Duyurusu Kontrolleri

[English](notes.md) · [Türkçe](notes.tr.md)

## Dersin amacı
Bu gün **Bağımlılık Sabitleme ve Güvenlik Duyurusu Kontrolleri** konusunu kontrollü, zararsız bir örnekte öğreniyoruz. Kavramları anlamak, hipotez kurmak ve gözlemi yorumdan ayırmak öncelikli.

## Temel bilgiler
1. Derlemeler tekrarlanabilir olsun diye bağımlılık sürümlerini tam olarak sabitle ve bir lock dosyası kullan.
2. Sabitlenmiş sürümleri sadece bir kez değil, her derlemede bir güvenlik duyurusu listesiyle karşılaştır.
3. `>=1.0` gibi sürüm aralıkları gerçekte neyin kurulu olduğunu gizler.

## Kavramsal ayrımlar
- Bir duyuru savunmasız bir sürümün var olduğunu söyler, kodunun savunmasız fonksiyona ulaştığını değil.
- Geçişli bağımlılıklar doğrudan olanlar kadar önemlidir.
- Körü körüne güncellemek davranışı bozabilir; her güncellemeden sonra test çalıştır.

## Lab uygulaması
Önce `deps_demo.py` dosyasını incele. Komutları lab klasöründen çalıştır:

~~~bash
python3 deps_demo.py
~~~


## Görevler
1. Sabitlenmiş hangi paketlerin bir duyuruyla eşleştiğini tahmin et.
2. Demoyu çalıştırıp düzeltme sürümlerini not et.
3. Sabitlenmemiş bir gereksinim ekle ve kontrolün onu reddettiğini izle.
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
