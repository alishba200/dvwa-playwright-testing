import re
from playwright.sync_api import expect

SQLI_URL = re.compile(r".*/vulnerabilities/sqli/\?id=.*")

def test_server_error_500(logged_in_page, browser_name):
    p = logged_in_page
    errors = []
    p.on("pageerror", lambda e: errors.append(str(e)))

    p.route(SQLI_URL, lambda route: route.fulfill(
        status=500,
        content_type="text/html",
        body="<h1>Internal Server Error</h1>"))

    p.goto("/vulnerabilities/sqli/?id=1&Submit=Submit")
    expect(p.locator("h1")).to_have_text("Internal Server Error")
    assert errors == []          # no JavaScript crash
    p.screenshot(path=f"screenshots/{browser_name}_mock_500.png")

def test_empty_response(logged_in_page, browser_name):
    p = logged_in_page
    errors = []
    p.on("pageerror", lambda e: errors.append(str(e)))

    p.route(SQLI_URL, lambda route: route.fulfill(
        status=200,
        content_type="text/html",
        body=""))

    p.goto("/vulnerabilities/sqli/?id=1&Submit=Submit")
    expect(p.locator("pre")).to_have_count(0)    # no results shown
    assert errors == []                          # page didn't break
    p.screenshot(path=f"screenshots/{browser_name}_mock_empty.png")