from playwright.sync_api import expect

def set_level(page, level):
    page.goto("/security.php")
    page.select_option("select[name='security']", level)
    page.click("input[name='seclev_submit']")

def test_set_medium(logged_in_page, browser_name):        # positive
    p = logged_in_page
    set_level(p, "medium")
    expect(p.locator("body")).to_contain_text("Security level set to medium")
    p.screenshot(path=f"screenshots/{browser_name}_security_medium.png")

def test_set_high(logged_in_page, browser_name):          # positive
    p = logged_in_page
    set_level(p, "high")
    expect(p.locator("body")).to_contain_text("Security level set to high")
    p.screenshot(path=f"screenshots/{browser_name}_security_high.png")

def test_security_page_requires_login(page):              # negative
    page.goto("/security.php")
    expect(page).to_have_url("http://localhost:8080/login.php")