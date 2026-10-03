# Day 7 — SQL Injection Foundations, Parameterized Queries and Input Boundaries

[🇬🇧 English](notes.md) | [🇹🇷 Türkçe](notes.tr.md)

## Goal

Understand **why SQL injection exists**, how application input reaches a database, why string concatenation creates a dangerous code/data boundary, and how parameterized queries prevent user-controlled data from becoming SQL syntax.

This day intentionally combines several related topics:

1. application → database data flow,
2. SQL query structure,
3. SQL injection root cause,
4. parameterized queries,
5. input validation and type boundaries,
6. database least privilege,
7. error handling and logging,
8. local testing and code review.

All exercises target the included local Flask + SQLite training application.

## 1. Where the database sits

A common web flow is:

```text
browser
   ↓ HTTP
route / controller
   ↓
application logic
   ↓
database query
   ↓
database
   ↓
result
   ↓
HTTP response
```

A request parameter is initially just untrusted input.

The dangerous transition happens when application code accidentally treats that input as part of a query's **syntax**.

## 2. Code and data must stay separate

Imagine:

```python
sql = "SELECT ... WHERE name = '" + user_input + "'"
```

The application is constructing one SQL program from trusted text plus attacker-controlled text.

Conceptually:

```text
SQL code + user data
       ↓ concatenation
one SQL string
       ↓
database parser cannot know developer intent
```

The root problem is not merely “bad characters.”

The root problem is mixing **code structure** with **untrusted data**.

## 3. SQL injection

SQL injection occurs when untrusted input can alter the intended structure/meaning of a SQL statement.

For this course, focus first on recognizing the vulnerable programming pattern rather than memorizing payloads.

Look for:

- string concatenation,
- f-strings containing request data,
- manual quoting,
- dynamically assembled conditions,
- raw query APIs fed with user-controlled syntax.

## 4. Included local application

Install Flask if needed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

Run:

```bash
python safe_sql_demo.py
```

It listens only on:

```text
127.0.0.1:5000
```

The in-memory database contains harmless product records.

## 5. Establish normal behavior

Try:

```bash
curl 'http://127.0.0.1:5000/unsafe-search?q=Book'
```

Then:

```bash
curl 'http://127.0.0.1:5000/safe-search?q=Book'
```

Both can return the expected book records for ordinary input.

That is important:

> Vulnerable code can appear to work correctly during normal functional testing.

Security review asks what happens when input violates the developer's assumptions.

## 6. The vulnerable query

The unsafe route contains:

```python
sql = f"SELECT id, name, category, price FROM products WHERE name LIKE '%{q}%'"
```

Draw the trust boundary:

```text
request.args["q"]
       ↓
untrusted string
       ↓
inserted directly into SQL source text
       ↓
database parses the combined text
```

That direct insertion is the design flaw.

## 7. Parameterized query

The safe route uses:

```python
sql = "SELECT id, name, category, price FROM products WHERE name LIKE ?"
rows = db.execute(sql, (f"%{q}%",)).fetchall()
```

Now the query structure and value travel separately.

Conceptually:

```text
SQL template       parameter value
     ↓                    ↓
fixed structure       untrusted data
        \              /
         database API
             ↓
data stays data
```

This is the central defense.

## 8. Parameterization is not escaping

Do not reduce the lesson to:

> “Put backslashes around dangerous characters.”

Escaping is context-sensitive and easy to implement incorrectly.

Parameterized APIs are designed to preserve the distinction between query syntax and values.

Prefer the database library/framework's supported parameter binding mechanism.

## 9. Validation still matters

Parameterized queries solve the SQL code/data boundary, but validation still serves application rules.

The `/product` route expects an integer:

```python
product_id = int(raw_id)
```

If the input is not an integer, the route returns `400`.

This creates two separate layers:

```text
validation
  -> "is this value acceptable for the application?"

parameterization
  -> "can this value become SQL syntax?"
```

Use both for their correct purposes.

## 10. Allowlist validation

When input belongs to a small known set, allowlists are useful.

Example:

```text
sort = price | name
direction = asc | desc
```

SQL identifiers such as column names often cannot be bound as ordinary value parameters.

Instead of accepting arbitrary identifier text, map a small user choice to trusted SQL fragments.

Conceptual example:

```python
allowed = {
    "name": "name",
    "price": "price",
}
column = allowed.get(user_choice)
```

The user selects a key; the application chooses the actual trusted SQL fragment.

## 11. Dynamic SQL requires extra care

Sometimes query structure really must change.

Example:

- optional filters,
- sorting,
- pagination,
- reporting.

Do not respond by concatenating everything.

Separate:

```text
dynamic but trusted structure
            +
parameterized untrusted values
```

ORMs/query builders can help, but they are not magic. Raw-query escape hatches can reintroduce unsafe construction.

## 12. Database least privilege

Even correctly written applications should not normally connect as an all-powerful database administrator.

Ask:

- Does this app need schema modification?
- Does a read-only component need write access?
- Does one service need access to every table?

Least privilege reduces impact if an application bug occurs.

```text
application role
      ↓
only required database permissions
```

Parameterization prevents one class of bug; least privilege limits consequences.

## 13. Error handling

The unsafe demo deliberately returns the SQLite error so you can learn locally.

Production applications should usually avoid exposing detailed database errors to users.

Detailed errors can reveal:

- table/column names,
- SQL syntax,
- database technology,
- internal assumptions.

A better production pattern:

```text
client -> generic appropriate error
server log -> diagnostic detail with sensitive-data controls
```

## 14. Logging

Useful fields may include:

- route,
- request/correlation ID,
- error category,
- timing,
- authenticated subject where appropriate.

Avoid logging:

- passwords,
- session tokens,
- full secrets,
- unnecessary sensitive query values.

Security visibility should not create a new data leak.

## 15. Testing the boundary safely

For this lab, you do not need a catalog of attack payloads.

Instead, test **classes of unexpected input** against your own local app:

- empty string,
- punctuation,
- quotes,
- Unicode,
- very long text,
- wrong type for numeric input.

Observe whether:

1. unsafe construction changes/breaks query syntax,
2. parameterized construction continues treating input as data,
3. validation rejects values outside the expected domain.

This teaches the mechanism instead of payload memorization.

## 16. Code-review checklist

When reviewing database code, ask:

```text
1. Where does input originate?
2. Which values are user-controlled?
3. Is SQL text assembled manually?
4. Are values parameterized?
5. Are dynamic identifiers allowlisted?
6. Is type/domain validation present?
7. What permissions does the DB account have?
8. What errors reach the client?
9. What sensitive data reaches logs?
10. Are negative tests present?
```

## 17. Authentication/authorization connection

Previous days covered identity and access control.

A secure database call may still be logically unauthorized.

For example:

```text
parameterized query
       ↓
no SQL injection
       ↓
but user requests another user's private object
       ↓
authorization bug may still exist
```

Security layers solve different problems.

## 18. XSS connection

SQL injection and XSS look different but share a useful design lesson:

```text
untrusted data crosses into an interpreter/context
                   ↓
keep data separate or encode for that exact context
```

For SQL: parameterization.

For HTML: context-appropriate output encoding/safe DOM APIs.

Do not treat “sanitize everything” as one universal operation.

## 19. Mini challenge

Create a new local endpoint:

```text
/category?name=books
```

Requirements:

- only `books` and `hardware` are accepted,
- invalid categories return `400`,
- SQL values are parameterized,
- no raw database error is returned,
- empty result is handled cleanly.

Then explain which part is:

- validation,
- parameterization,
- error handling.

## 20. Exercises

1. Run the local app.
2. Compare normal output from unsafe and safe search.
3. Identify the exact trust boundary in the unsafe route.
4. Rewrite the unsafe route using parameter binding.
5. Test empty, quoted, Unicode and long input locally.
6. Explain why parameterization is different from escaping.
7. Add integer validation to a new numeric filter.
8. Implement the category mini challenge.
9. Write a hypothetical least-privilege DB role for this app.
10. List which database errors should stay server-side.
11. Review all three endpoints using the checklist.
12. Explain how an endpoint can be injection-safe but authorization-unsafe.

## Questions

1. What is the root cause of SQL injection?
2. Why can normal functional tests miss it?
3. What does a parameterized query separate?
4. Is parameterization the same as input validation?
5. Why is escaping not the preferred primary defense?
6. How should dynamic column names be handled?
7. Why does DB least privilege matter?
8. Why can detailed DB errors be risky?
9. Can an ORM still be used unsafely?
10. How is SQL injection conceptually related to XSS?
11. Can a parameterized query still expose unauthorized data?
12. What should a negative test verify?

## Main takeaway

```text
untrusted request data
        ↓
validate application meaning
        ↓
parameterized database API
        ↓
fixed SQL structure + separate values
        ↓
least-privilege database role
        ↓
safe error/log handling
```

Do not memorize SQL injection as a bag of strings. Understand the boundary that allows data to become code, then design so that boundary stays intact.
