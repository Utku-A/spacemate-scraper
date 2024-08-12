from playwright.sync_api import sync_playwright
import time

Base_Url = 'https://www.facebook.com'


def search_facebook_marketplace(location, search_query):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            browser.new_context().set_default_timeout(60000)
            page = browser.new_page()
            page.set_default_navigation_timeout(60000)
            # page = goto_marketplace_page(page,"brisbane","storage space for rent")


            page = goto_marketplace_page(page,location,search_query)
            facebook_login(page,"halisutkualadag9@gmail.com", "space_321123")
            time.sleep(5)
            page = goto_marketplace_page(page,location,search_query)
            time.sleep(10)
            browser.close()
    except Exception as error:
        print(f"Web control error: {str(error)}")
        return False


def element_visibile(page,locator_selector):
    locator = page.locator(locator_selector)
    locator.wait_for(state='visible', timeout=15000)
    return locator



def facebook_login(page, user_mail, passwd):
    element_visibile(page,'#login_popup_cta_form [name="email"]').type(user_mail)
    element_visibile(page,'#login_popup_cta_form [name="pass"]').type(passwd)
    time.sleep(5)
    element_visibile(page,'#login_popup_cta_form [name="pass"]').press('Enter')


def goto_marketplace_page(page,location,search):
    page.goto(f"https://www.facebook.com/marketplace/{location}/search/?query="+search, timeout=15000, wait_until="load")
    return page


def search_pages_scroll_scanner(page):
    links = set()
    last_height = page.evaluate("document.body.scrollHeight")

    while True:
        anchors = page.locator('a.card-link')
        for anchor in anchors:
            href = anchor.get_attribute('href')
            if href and href not in links:
                links.add(href)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        time.sleep(3)
        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    for link in links:
        print(link)


    
    return True