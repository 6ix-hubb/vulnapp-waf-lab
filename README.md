# Vulnerable Web App + WAF Lab (Nginx + ModSecurity + OWASP CRS)

A deliberately vulnerable Flask + SQLite web application, deployed behind a Web Application Firewall (Nginx + ModSecurity v3 + OWASP Core Rule Set v4.7), demonstrating both attack exploitation and WAF-based detection/prevention.

## Purpose

Built as a hands-on lab for Network & System Security coursework. Demonstrates the full lifecycle of a web application vulnerability: exploit it unprotected, deploy a WAF in Detection mode to observe how it's caught, then switch to Prevention mode to confirm it's blocked — without breaking legitimate traffic.

## Architecture

#Browser-> Nginx->Modsecurity(port 80)->Flask App(port 3000)


The WAF inspects every request before it reaches the application. Malicious payloads are logged (Detection mode) or blocked with a 403 (Prevention mode) before the vulnerable code ever executes.

## Tech Stack

- Python 3 / Flask
- SQLite3
- Nginx
- ModSecurity v3
- OWASP Core Rule Set (CRS) v4.7
- Ubuntu 22.04 LTS

## Vulnerabilities in the Target App

### 1. SQL Injection — `/login`

Raw string formatting builds the SQL query directly from user input:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```
**Proof of concept:** password field `' OR '1'='1` bypasses authentication entirely.

### 2. Cross-Site Scripting (XSS) — `/search`

User input is concatenated directly into the HTML response, bypassing Flask's Jinja2 auto-escaping:
```python
return render_template_string('''...<p>You searched for: ''' + query + '''</p>''', query=query)
```
**Proof of concept:** `/search?q=<script>alert('XSS')</script>` executes arbitrary JavaScript.

## WAF Testing Results

Tested five attack categories against the app, first with the WAF in **Detection mode** (logs only), then in **Prevention mode** (actively blocks).

| Attack | CRS Rule(s) | Detection Mode | Prevention Mode |
|---|---|---|---|
| SQL Injection | 942100, 942190, 942270, 942360 | Logged | 403 Blocked |
| XSS | 941100, 941110, 941160, 941180, 941390 | Logged | 403 Blocked |
| Path Traversal | 930100 | Logged | 403 Blocked |
| Scanner Detection (Nikto UA) | 913100 | Logged | 403 Blocked |
| Log4Shell / JNDI Injection | 944150 | Logged | 403 Blocked |

Legitimate traffic (`/login` with valid credentials) continued returning `200 OK` in Prevention mode — confirming no false positives.

## Setup

**1. Clone and run the target app:**
```bash
git clone https://github.com/6ix-hubb/vulnapp-waf-lab.git
cd vulnapp-waf-lab
python3 -m venv venv
source venv/bin/activate
pip install flask
python app.py
```
App runs at `http://127.0.0.1:3000/`

**2. WAF setup (Nginx + ModSecurity + CRS):**
```bash
sudo apt install -y nginx libmodsecurity3 libmodsecurity-dev libnginx-mod-http-modsecurity
sudo mkdir -p /etc/nginx/modsec
sudo git clone --depth 1 -b v4.7.0 https://github.com/coreruleset/coreruleset.git /etc/nginx/modsec/crs
sudo cp /etc/nginx/modsec/crs/crs-setup.conf.example /etc/nginx/modsec/crs/crs-setup.conf
```
Configure `/etc/nginx/modsec/modsecurity.conf` and Nginx site config to enable ModSecurity and proxy to port 3000. See lab writeup for full config.

## Default Credentials

| Username | Password        |
|----------|-----------------|
| admin    | supersecret123  |

## Key Takeaways

- **Detection mode is a mandatory first step**, not optional — it validates rule accuracy and surfaces false positives against real application traffic before any blocking is enabled, preventing legitimate users from being locked out.
- A WAF is a compensating control, not a substitute for fixing the underlying vulnerable code — the SQLi and XSS flaws in this app still exist; the WAF only prevents them from being exploited externally.
- Anomaly scoring (CRS's approach) reduces false positives compared to single-rule blocking, since multiple weaker signals must combine before a request is flagged.

## Disclaimer

Built for educational purposes as part of Network & System Security coursework. Do not deploy this application or configuration outside an isolated lab environment.
