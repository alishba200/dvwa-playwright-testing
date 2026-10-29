from playwright.sync_api import expect
from conftest import do_login

def test_login_valid(page, browser_name):                    # positive
    do_login(page, "admin", "password")
    expect(page).to_have_url("http://localhost:8080/index.php")
    expect(page.locator("#main_body")).to_contain_text("Welcome to Damn Vulnerable Web Application")
    page.screenshot(path=f"screenshots/{browser_name}_login_success.png")

def test_login_wrong_password(page, browser_name):           # negative
    do_login(page, "admin", "wrongpass")
    expect(page).to_have_url("http://localhost:8080/login.php")
    expect(page.locator("body")).to_contain_text("Login failed")
    page.screenshot(path=f"screenshots/{browser_name}_login_wrong_password.png")

def test_login_empty_fields(page, browser_name):             # negative
    do_login(page, "", "")
    expect(page.locator("body")).to_contain_text("Login failed")
    page.screenshot(path=f"screenshots/{browser_name}_login_empty_fields.png")