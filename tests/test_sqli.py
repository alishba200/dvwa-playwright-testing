from playwright.sync_api import expect

def submit_id(page, value):
    page.goto("/vulnerabilities/sqli/")
    page.fill("input[name='id']", value)
    page.click("input[name='Submit']")

def test_valid_user_id(logged_in_page, browser_name):                    # positive
    submit_id(logged_in_page, "1")
    expect(logged_in_page.locator("pre")).to_contain_text("First name: admin")
    logged_in_page.screenshot(path=f"screenshots/{browser_name}_sqli_valid_id.png")

def test_empty_id_shows_no_results(logged_in_page):                      # negative
    submit_id(logged_in_page, "")
    expect(logged_in_page.locator("pre")).to_have_count(0)

def test_sql_injection_returns_all_users(logged_in_page, browser_name):  # negative / security
    submit_id(logged_in_page, "' OR '1'='1")
    assert logged_in_page.locator("pre").count() > 1
    logged_in_page.screenshot(path=f"screenshots/{browser_name}_sqli_injection.png")