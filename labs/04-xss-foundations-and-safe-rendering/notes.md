# Day 4 — XSS Foundations: Output Encoding and DOM Context

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal
Understand why untrusted data must not be inserted into HTML as executable markup, learn the basic idea of XSS, distinguish source/sink/context, and practice safe rendering locally.

## 1. What is XSS?
Cross-Site Scripting (XSS) is a class of web vulnerability where untrusted data reaches a browser context in a way that can be interpreted as executable script/markup rather than harmless data.

At a high level:
```text
untrusted input
      ↓
unsafe rendering
      ↓
browser interprets it as active content
```

## 2. Data vs code
Suppose a user enters:
```text
<b>Hello</b>
```

If an application treats this as text, the characters should be displayed. If it injects the value as HTML, the browser interprets the markup.

The security goal is generally to keep untrusted data as **data**, not code.

## 3. Source and sink
A **source** is where data enters the relevant flow, such as a URL parameter, form field, API response, or stored database value.

A **sink** is an operation that places data into a potentially dangerous execution/rendering context.

DOM examples:
```javascript
element.textContent = userValue; // renders text
element.innerHTML = userValue;   // parses HTML
```

This does not mean every use of `innerHTML` is automatically exploitable. Risk depends on whether attacker-controlled data reaches it and on surrounding controls.

## 4. Context matters
HTML text, HTML attributes, JavaScript, URLs and CSS are different contexts. Escaping appropriate for one context may not be correct for another.

This is why "replace a few special characters everywhere" is not a complete output-encoding strategy.

## 5. Safe local lab
Create `safe_demo.html` and open it locally.

The page reads text from an input and renders it using `textContent`.

Try entering:
```text
<b>training</b>
```

Expected result: the literal markup is shown as text rather than becoming a bold element.

## 6. Inspect with DevTools
Use Elements and Sources to inspect:
- the input element,
- the output element,
- the JavaScript event handler,
- the DOM after rendering.

Ask: did the browser create new markup, or only a text node?

## 7. Reflected, stored and DOM-based XSS
At a conceptual level:

- **Reflected XSS** — untrusted input is included in an immediate response and reaches an unsafe browser context.
- **Stored XSS** — untrusted content is persisted and later rendered unsafely.
- **DOM-based XSS** — client-side JavaScript moves attacker-controlled data into a dangerous DOM sink.

These labels describe where the unsafe data flow occurs; real applications can have more complex combinations.

## 8. Output encoding
A strong defensive principle is context-appropriate output encoding/escaping.

Frameworks often escape template values by default. Developers can accidentally bypass that protection by using raw-HTML features, unsafe DOM APIs, or custom rendering logic.

## 9. CSP as defense in depth
Content Security Policy can reduce the impact of some script-injection problems when configured well, but it should not replace correct output handling.

Think:
```text
safe rendering first
       +
CSP as additional browser policy
```

## 10. Security review questions
When reviewing code, ask:
1. Where does this value originate?
2. Can a user control it?
3. Which rendering/execution context receives it?
4. Is the framework escaping it?
5. Is an unsafe API bypassing that protection?

## Exercises
1. Open `safe_demo.html`.
2. Enter ordinary text and then `<b>training</b>`.
3. Inspect the output node in DevTools.
4. Find the `textContent` assignment.
5. Explain why the browser displays markup characters instead of interpreting them.
6. List three possible input sources in a web application.
7. Explain why CSP is defense in depth rather than a replacement for safe rendering.

## Questions
1. What is the basic cause of XSS?
2. What is a source?
3. What is a sink?
4. How do `textContent` and `innerHTML` differ conceptually?
5. Why does output context matter?
6. What distinguishes reflected, stored and DOM-based XSS?
7. Why can raw-HTML framework features be dangerous with untrusted input?

## Main takeaway
```text
untrusted data
      ↓
trace source
      ↓
identify rendering context/sink
      ↓
context-safe output handling
      ↓
browser receives data, not executable content
```
