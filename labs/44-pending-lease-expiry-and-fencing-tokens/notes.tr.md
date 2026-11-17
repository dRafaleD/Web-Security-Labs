# Gün 44 — Bekleyen İşlem Kiraları ve Fencing Token

[English](notes.md) · [Türkçe](notes.tr.md) · [Python uygulaması](lease_fencing_demo.py)

## 43. günden devam
Önceki gün `PENDING` durumunda kalan isteğin tekrar gönderilmesi halinde ne yapılacağını öğrendik. Ya işlemi yürüten worker çökerse ve kayıt sonsuza kadar beklemede kalırsa?

**Lease (süreli hak):** worker'a belirli zamana kadar verilen işleme hakkı. **Fencing token:** yeni worker geldiğinde artırılan sıra numarası; eski worker'ın sonradan sonuç yazmasını engellemeye yardım eder.

Örnekte ilk worker token 1 alır. Süresi dolunca ikinci worker token 2 alır. Eski worker'ın sonuç yazma girişimi **STALE_WORKER** olarak reddedilir. Yeni worker güncellemeyi yapar; aynı isteğin sonraki tekrarları **REPLAY** olur.

## Çalıştırma
~~~bash
python3 labs/44-pending-lease-expiry-and-fencing-tokens/lease_fencing_demo.py
~~~

## Sorular
Süre dolunca eski worker neden hâlâ tehlikeli olabilir? Fencing token neden artmalı? Gerçek veritabanında güncelleme ve idempotency kaydı neden birlikte atomik yapılmalı?

## Sınırlar
Kod gerçek concurrency/transaction sağlamaz. İşlem sırasını bellekte gösteren eğitim modelidir.
