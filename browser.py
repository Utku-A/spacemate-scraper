from playwright.sync_api import sync_playwright
import time

Base_Url = 'https://www.facebook.com'


def setup_browser():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            browser.new_context().set_default_timeout(60000)
            page = browser.new_page()
            page.goto(Base_Url)



            time.sleep(10)
            browser.close()
    except Exception as error:
        print(f"Web control error: {str(error)}")
        return False


def facebook_login(page, user_mail, passwd):
    page.query_selector('[name="email"]').type(user_mail)
    page.query_selector('#pass').type(passwd)


setup_browser()