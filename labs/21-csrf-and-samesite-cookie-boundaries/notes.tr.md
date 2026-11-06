# Gün 21 — CSRF, SameSite Çerezleri ve Origin Doğrulaması

[English](notes.md) · [Türkçe](notes.tr.md)

## Hedef
**CSRF (Cross-Site Request Forgery)** saldırı sınıfını ve tarayıcının otomatik gönderdiği oturum çerezleri nedeniyle neden risk oluştuğunu öğrenmek. Güvenlik kontrollerinin birbirini nasıl tamamladığını incelemek.

## Temel kavramlar
- Oturum çerezi tarayıcı tarafından otomatik eklenebilir; istek gerçekten kullanıcı tarafından başlatılmış olmayabilir.
- **SameSite=Lax/Strict**, bazı çapraz site isteklerinde çerez gönderimini kısıtlar. Tek başına evrensel CSRF koruması değildir.
- **CSRF token'ı**, sunucuda oturuma bağlı olarak doğrulanan tahmin edilmesi zor değerdir.
- **Origin kontrolü**, isteğin kaynak kökenini denetler. Başlık yoksa nasıl davranılacağına ilişkin açık politika gerekir.
- **XSS**, CSRF korumalarını zayıflatabilir; iki açık aynı şey değildir.

## Güvenli pratik
Bu uygulama internete bağlanmaz; yalnızca sentetik istek değerlerini sınar:

```bash
python3 csrf_demo.py
```

## Görevler
1. Hangi bilgiyi tarayıcı, hangisini sunucu belirliyor?
2. Yanlış token veya farklı Origin olduğunda sonucu tahmin et.
3. Origin başlığı eksik bir durum ekle.
4. SameSite ve CSRF token'larının farkını yaz.
5. Modelin gerçek HTTP sunucusunu neden tam temsil etmediğini açıkla.

## Sınır
Gerçek sisteme istek gönderilmez; yalnızca eğitim amaçlı doğrulama simülasyonudur.
