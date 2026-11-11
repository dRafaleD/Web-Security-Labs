# Gün 39 — PATCH İsteklerinde Alan Yetkisi ve Sürüm Kontrolü

[English](notes.md) · [Türkçe](notes.tr.md) · [Çevrimdışı Python uygulaması](patch_guard_demo.py)

## 38. günden devam
38. günde geçerli JSON'un bile is_admin veya owner gibi **korunan alanları** değiştirmeye çalışabileceğini görmüştük. Şimdi **PATCH**, yani bir nesnenin yalnızca bazı alanlarını güncelleme işlemine geçiyoruz.

Örnek istek: kullanıcı kendi profilindeki display_name alanını değiştirmek istiyor. Ama aynı isteğe role=admin eklerse uygulama bu alanı kabul etmemelidir. Üstelik kullanıcının başka birine ait nesneyi değiştirmesi de ayrı bir **BOLA/IDOR** problemidir.

## Koruma katmanları
1. **Kimlik:** İşlemi kimin yaptığı güvenilir oturum bilgisinden gelir; JSON gövdesindeki owner alanından değil.
2. **Nesne yetkisi:** İstenen nesnenin sahibi o kullanıcı mı?
3. **Alan yetkisi:** Sadece display_name ve notifications_enabled değiştirilebilir. role, owner, version veya bilinmeyen alanlar reddedilir.
4. **Değer kontrolü:** display_name boş olamaz ve uzunluğu sınırlıdır; notifications_enabled gerçek boolean olmalıdır.
5. **Sürüm:** İstek mevcut sürümü bilmiyorsa (eski form/iki sekme), başka değişiklikleri ezmemesi için reddedilir. Buna **optimistic concurrency** denir.
6. **Atomiklik:** Gerçek veritabanında sürüm kontrolü ve yazma **tek atomik işlemde** yapılmalı; bu eğitim örneğindeki sözlük modeli tek başına yeterli değildir.

## Uygulama
~~~bash
python3 patch_guard_demo.py
~~~

İki kurgu kullanıcının belgeleri bulunur. Program geçerli güncellemeyi kabul eder; role alanını, başka kullanıcının belgesini, eski sürümü ve geçersiz alan değerini reddeder. Ardından izinli bir boolean güncelleme yapar. Her karar assert ile kontrol edilir.

## Görevler
1. Korunan alanı sessizce atlamak yerine tüm isteği reddetmek neden faydalıdır?
2. Geçerli JSON şeması, neden nesne yetkisi anlamına gelmez?
3. Yalnızca dark/light olabilen bir theme alanı ekle.
4. İki sunucu aynı sürümü okuyup eşzamanlı yazarsa hangi yarış durumu oluşur?
5. PATCH ile PUT arasındaki temel fark nedir? Neden HTTP metodu tek başına yetki sağlamaz?
6. Güncellemenin sonucunu gizli alanları kaydetmeden nasıl loglarsın?

## Sınırlar
Bu kod HTTP sunucusu, gerçek kimlik doğrulama veya RFC JSON Patch uygulaması değildir. Veritabanında koşullu atomik güncelleme, gerçek erişim kontrolleri ve uygun hata yönetimi ayrıca gerekir.
