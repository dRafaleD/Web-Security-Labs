# Gün 4 — XSS Temelleri: Output Encoding ve DOM Context

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Amaç
Untrusted data'nın neden executable markup olarak HTML'e yerleştirilmemesi gerektiğini, XSS'in temel mantığını, source/sink/context ayrımını ve local ortamda güvenli rendering yaklaşımını öğrenmek.

## 1. XSS nedir?
Cross-Site Scripting (XSS), untrusted data'nın browser tarafından zararsız veri yerine executable script/markup olarak yorumlanabileceği bir context'e güvenli olmayan şekilde ulaşmasıyla ortaya çıkan web vulnerability sınıfıdır.

```text
untrusted input
      ↓
unsafe rendering
      ↓
browser active content olarak yorumlar
```

## 2. Data ve code ayrımı
Kullanıcı şunu girsin:
```text
<b>Hello</b>
```

Uygulama bunu text olarak ele alırsa karakterler ekranda görünür. HTML olarak inject ederse browser markup'ı yorumlar.

Temel güvenlik amacı untrusted data'yı **data** olarak tutmak, code haline getirmemektir.

## 3. Source ve sink
**Source**, verinin ilgili akışa girdiği yerdir: URL parameter, form field, API response veya database'den gelen stored value gibi.

**Sink**, veriyi potansiyel olarak tehlikeli execution/rendering context'ine yerleştiren işlemdir.

DOM örneği:
```javascript
element.textContent = userValue; // text render eder
element.innerHTML = userValue;   // HTML parse eder
```

Her `innerHTML` kullanımı otomatik exploitable değildir. Risk, attacker-controlled data'nın buraya ulaşıp ulaşmadığına ve diğer kontrollere bağlıdır.

## 4. Context önemlidir
HTML text, HTML attribute, JavaScript, URL ve CSS farklı context'lerdir. Bir context için doğru escaping başka bir context için doğru olmayabilir.

Bu yüzden birkaç special character'ı her yerde değiştirmek tam bir output-encoding stratejisi değildir.

## 5. Güvenli local lab
`safe_demo.html` dosyasını local aç.

Sayfa input'taki değeri `textContent` ile render eder.

Şunu dene:
```text
<b>training</b>
```

Beklenen: yeni bold element oluşması yerine markup literal text olarak görünür.

## 6. DevTools ile inceleme
Elements ve Sources üzerinden:
- input element,
- output element,
- JavaScript event handler,
- rendering sonrası DOM

alanlarını incele.

Browser yeni markup mı oluşturdu yoksa sadece text node mu?

## 7. Reflected, stored ve DOM-based XSS
Kavramsal olarak:

- **Reflected XSS** — untrusted input immediate response içinde unsafe browser context'ine ulaşır.
- **Stored XSS** — untrusted içerik persist edilir ve daha sonra unsafe biçimde render edilir.
- **DOM-based XSS** — client-side JavaScript attacker-controlled data'yı dangerous DOM sink'e taşır.

Gerçek uygulamalarda akışlar daha karmaşık olabilir.

## 8. Output encoding
Temel defensive prensip context'e uygun output encoding/escaping kullanmaktır.

Framework'ler template value'larını çoğu zaman default escape eder. Raw-HTML özellikleri, unsafe DOM API'leri veya custom rendering logic bu korumayı bypass edebilir.

## 9. CSP defense in depth'dir
Content Security Policy doğru yapılandırıldığında bazı script-injection sorunlarının etkisini azaltabilir fakat doğru output handling'in yerine geçmemelidir.

```text
önce safe rendering
       +
ek browser policy olarak CSP
```

## 10. Code review soruları
1. Bu value nereden geliyor?
2. User kontrol edebiliyor mu?
3. Hangi rendering/execution context'ine gidiyor?
4. Framework bunu escape ediyor mu?
5. Unsafe API bu korumayı bypass ediyor mu?

## Alıştırmalar
1. `safe_demo.html` dosyasını aç.
2. Normal text ve ardından `<b>training</b>` gir.
3. DevTools'ta output node'u incele.
4. `textContent` assignment'ını bul.
5. Browser'ın markup'ı yorumlamak yerine neden karakterleri gösterdiğini açıkla.
6. Web application için üç input source örneği yaz.
7. CSP'nin neden safe rendering'in yerine geçen bir çözüm değil defense-in-depth olduğunu açıkla.

## Sorular
1. XSS'in temel nedeni nedir?
2. Source nedir?
3. Sink nedir?
4. `textContent` ile `innerHTML` kavramsal olarak nasıl farklıdır?
5. Output context neden önemlidir?
6. Reflected, stored ve DOM-based XSS nasıl ayrılır?
7. Raw-HTML framework özellikleri untrusted input ile neden riskli olabilir?

## Ana çıkarım
```text
untrusted data
      ↓
source'u takip et
      ↓
rendering context/sink'i belirle
      ↓
context-safe output handling
      ↓
browser executable content değil data alır
```
