import pytest

BASE = "http://localhost:8080"

def do_login(page, user="admin", pwd="password"):
    page.goto("/login.php")
    page.fill("input[name='username']", user)
    page.fill("input[name='password']", pwd)
    page.click("input[name='Login']")

@pytest.fixture
def logged_in_page(page):
    do_login(page)
    page.context.add_cookies([{"name": "security", "value": "low", "url": BASE}])
    return page