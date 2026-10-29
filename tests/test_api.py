import re
import requests

BASE = "http://localhost:8080"

def get_token(html):
    m = re.search(r"name=['\"]user_token['\"] value=['\"]([^'\"]+)", html)
    return m.group(1) if m else ""

def login_session():
    s = requests.Session()
    token = get_token(s.get(f"{BASE}/login.php").text)
    s.post(f"{BASE}/login.php", data={"username": "admin", "password": "password",
                                    "Login": "Login", "user_token": token})
    s.cookies.set("security", "low")
    return s

def test_read_pages_status_codes():                       # READ
    assert requests.get(f"{BASE}/login.php").status_code == 200
    assert requests.get(f"{BASE}/this_page_does_not_exist.php").status_code == 404

def test_create_guestbook_entry():                        # CREATE
    s = login_session()
    url = f"{BASE}/vulnerabilities/xss_s/"
    token = get_token(s.get(url).text)
    r = s.post(url, data={"txtName": "API", "mtxMessage": "api-created-entry",
                        "btnSign": "Sign Guestbook", "user_token": token})
    assert r.status_code == 200
    assert "api-created-entry" in s.get(url).text

def test_update_security_level():                         # UPDATE
    s = login_session()
    url = f"{BASE}/security.php"
    token = get_token(s.get(url).text)
    r = s.post(url, data={"security": "medium", "seclev_submit": "Submit", "user_token": token})
    assert r.status_code == 200
    assert "Security level set to medium" in r.text

def test_zz_delete_reset_database():                      # DELETE (runs last)
    s = login_session()
    url = f"{BASE}/setup.php"
    token = get_token(s.get(url).text)
    r = s.post(url, data={"create_db": "Create / Reset Database", "user_token": token})
    assert r.status_code == 200
    s2 = login_session()
    assert "api-created-entry" not in s2.get(f"{BASE}/vulnerabilities/xss_s/").text