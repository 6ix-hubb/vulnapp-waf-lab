# Vulnerable Web App — WAF Lab Target

A deliberately vulnerable Flask + SQLite web application built as a target for testing a Web Application Firewall (Nginx + ModSecurity + OWASP CRS). This project demonstrates two of the most common web vulnerabilities — SQL Injection and Cross-Site Scripting (XSS) — and will later show how a WAF detects and blocks them.

## Purpose

This app was built intentionally insecure to serve as a controlled target for a Web Application Firewall lab. It is not intended for production use.

## Tech Stack

- Python 3 / Flask
- SQLite3
- HTML (Jinja2 templating)

## Vulnerabilities

### 1. SQL Injection — `/login`

The login route builds its SQL query using raw string formatting instead of parameterized queries:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

This allows an attacker to manipulate the query logic. For example, entering `' OR '1'='1` as the password bypasses authentication entirely, since the resulting query always evaluates to true.

**Proof of concept:**
- Username: (anything)
- Password: `' OR '1'='1`
- Result: Logged in without valid credentials

### 2. Cross-Site Scripting (XSS) — `/search`

The search route concatenates user input directly into the HTML response, bypassing Flask's Jinja2 auto-escaping:

```python
return render_template_string('''...<p>You searched for: ''' + query + '''</p>''', query=query)
```

**Proof of concept:**


Executes arbitrary JavaScript in the browser instead of displaying the input as text.

## Setup

```bash
git clone https://github.com/6ix-hubb/vulnapp-waf-lab.git
cd vulnapp-waf-lab
python3 -m venv venv
source venv/bin/activate
pip install flask
python app.py
```

App runs at `http://127.0.0.1:3000/`

## Default Credentials

| Username | Password        |
|----------|-----------------|
| admin    | supersecret123  |

## Next Steps

This app will be placed behind an Nginx reverse proxy running ModSecurity v3 with the OWASP Core Rule Set (CRS) v4.7, tested first in Detection mode and then in Prevention mode, to demonstrate WAF-based mitigation of these vulnerabilities.

## Disclaimer

Built for educational purposes as part of a Network & System Security coursework project. Do not deploy this application outside an isolated lab environment.
