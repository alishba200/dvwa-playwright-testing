from playwright.sync_api import expect

def open_guestbook(page):
    page.goto("/vulnerabilities/xss_s/")

def test_sign_guestbook(logged_in_page, browser_name):        # positive
    p = logged_in_page
    open_guestbook(p)
    p.fill("input[name='txtName']", "Tester")
    p.fill("textarea[name='mtxMessage']", "Hello from Playwright")
    p.click("input[name='btnSign']")
    expect(p.locator("#guestbook_comments").first).to_be_visible()
    expect(p.locator("body")).to_contain_text("Hello from Playwright")
    p.screenshot(path=f"screenshots/{browser_name}_guestbook_entry.png")

def test_name_field_max_length(logged_in_page):               # negative (too much input)
    p = logged_in_page
    open_guestbook(p)
    p.locator("input[name='txtName']").press_sequentially("A" * 50)
    assert len(p.input_value("input[name='txtName']")) <= 10

def test_script_in_message_executes(logged_in_page, browser_name):   # negative / security
    p = logged_in_page
    alerts = []

    def on_dialog(dialog):
        alerts.append(dialog.message)
        dialog.accept()

    p.on("dialog", on_dialog)
    open_guestbook(p)
    p.fill("input[name='txtName']", "Hacker")
    p.fill("textarea[name='mtxMessage']", "<script>alert('xss')</script>")
    p.click("input[name='btnSign']")
    p.wait_for_load_state("load")      # let the form submission finish
    open_guestbook(p)                  # load the guestbook again so the stored script runs
    p.wait_for_load_state("load")
    assert "xss" in alerts             # proves the input is not sanitized
    p.screenshot(path=f"screenshots/{browser_name}_guestbook_xss.png")