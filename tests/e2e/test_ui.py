import subprocess
import time
import requests
from playwright.sync_api import sync_playwright


def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url)
            return True
        except Exception:
            time.sleep(0.2)
    return False


def test_ui_flow(tmp_path):
    # start server
    proc = subprocess.Popen(['python', 'app.py'], cwd=str(tmp_path.parent.parent), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        assert wait_for_server('http://127.0.0.1:5000/ui', timeout=5)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://127.0.0.1:5000/ui')
            # create user
            page.fill('#nameInput', 'E2E User')
            page.fill('#emailInput', f'e2e{int(time.time())}@example.com')
            page.click('#createForm button[type=submit]')
            page.wait_for_timeout(500)
            assert page.locator('text=E2E User').count() >= 1
            # open detail
            page.click('a:has-text("E2E User")')
            page.wait_for_load_state('networkidle')
            # edit
            page.fill('#name', 'E2E User 2')
            page.click('button:has-text("保存")')
            page.wait_for_timeout(300)
            assert page.locator('text=保存成功').count() >= 1
            # delete
            page.click('#deleteBtn')
            page.on('dialog', lambda dialog: dialog.accept())
            page.wait_for_timeout(500)
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
