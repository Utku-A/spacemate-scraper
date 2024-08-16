from playwright.sync_api import sync_playwright
from database import add_search_marketplace_data, update_items
from spacemate import add_listing, upload_img
import time, re, os

Base_Url = 'https://www.facebook.com'
Title_Filter = ["storage","space","garage","parking"]


def title_check_category(text):
    text_lower = text.lower()
    title_filter = ["storage","space","garage","parking"]
    return any(keyword.lower() in text_lower for keyword in title_filter)


def search_facebook_marketplace(location, search_query):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.new_context().set_default_timeout(60000)
            page = browser.new_page()
            page.set_default_navigation_timeout(60000)
            # page = goto_marketplace_page(page,"brisbane","storage space for rent")
            page = goto_marketplace_page(page,location,search_query)
            facebook_login(page,"halisutkualadag9@gmail.com", "space_321123")
            time.sleep(5)
            page = goto_marketplace_page(page,location,search_query)

            search_pages_scroll_scanner(page,location,search_query)

            time.sleep(10)
            browser.close()
    except Exception as error:
        print(f"Web control error: {str(error)}")
        return False


def scennar_page_detail(link):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.new_context().set_default_timeout(60000)
            page = browser.new_page()
            page.set_default_navigation_timeout(60000)
            page.goto(f"{Base_Url}{link}")
            get_detail_page_data(page, link)
            browser.close()
    except Exception as error:
        print(f"scennar_page_detail: {str(error)}")


def element_visibile(page,locator_selector):
    locator = page.locator(locator_selector)
    locator.wait_for(state='visible', timeout=15000)
    return locator


def get_selector_text(page, selector):
    try:
        return page.query_selector(selector).inner_text() if page.query_selector(selector) else None
    except:
        return None


def facebook_login(page, user_mail, passwd):
    element_visibile(page,'#login_popup_cta_form [name="email"]').type(user_mail)
    element_visibile(page,'#login_popup_cta_form [name="pass"]').type(passwd)
    time.sleep(5)
    element_visibile(page,'#login_popup_cta_form [name="pass"]').press('Enter')


def goto_marketplace_page(page,location,search):
    page.goto(f"https://www.facebook.com/marketplace/{location}/search/?query="+search, timeout=15000, wait_until="load")
    return page


def parse_currency_value(text):
    pattern = r'([A-Z\$]+)([\d.,]+)'
    match = re.search(pattern, text)
    if match:
        currency = match.group(1)
        value = match.group(2).replace(',', '')  
        value = float(value)
        return currency, value
    else:
        return None, None


def search_pages_scroll_scanner(page,location,search_query):
    title_locator   = '.xzsf02u .x1lliihq.x6ikm8r.x10wlt62.x1n2onr6'
    price_locator   = '> div > a > div :nth-child(2) > div:nth-child(1) span:nth-child(1) > div > span:nth-child(1)'
    last_height     = page.evaluate("document.body.scrollHeight")

    while True:

        if os.environ['Agent_List_Scanner'] == "Stoped": break

        items = page.query_selector_all('[data-virtualized="false"] > div ')
        try:
            for item in items[-20:]:
                link    = item.query_selector('a').get_attribute("href")
                link    = str(link).split("?")
                link    = link[0]
                title   = item.query_selector(title_locator).inner_text()
                price   = item.query_selector(price_locator).inner_text()
                currency, price = parse_currency_value(price)
                if currency == "AU$": currency = "AUD"
                if title_check_category(title):
                    add_search_marketplace_data(location,search_query,title,link,price,currency)
                else:
                    print(f"{link} Hatalı kategori")
        except:
            print("Liste hatası")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        time.sleep(3)
        new_height = page.evaluate("document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    return True



def get_detail_page_data(page, link):
    element_visibile(page,'[aria-label="Kapat"]').click()
    maps_x, maps_y = get_maps_data(page)
    title = page.inner_text('h1 span')
    element_visibile(page,'.x126k92a span > :nth-child(1)').click()
    description = page.inner_text('.x126k92a')
    description = description.replace("Daha az gör","") if description else ""
    img_links   = get_img_links(page)
    update_items(link, title, description, float(maps_x), float(maps_y))
    if add_listing(link, img_links):
        print("Spacemate tarafına data yüklendi")
    else:
        print("Bir sorun oluştu")


def get_img_links(page):
    img_links = []
    items = page.query_selector_all('[style="display: inline;"] img')
    for item in items:
        img_link = item.get_attribute("src")
        img_links.append(img_link)

    return img_links



def get_maps_data(page):
    maps_locator_1 = '[style="height: 120px; width: 328px;"] > div:nth-child(1)'
    maps_locator_2 = '[style="padding-top: calc(36.5854%);"] > div:nth-child(1)'
    try:
        element = page.wait_for_selector(maps_locator_1, timeout=5000)
    except:
        element = page.wait_for_selector(maps_locator_2, timeout=5000)

    style = element.get_attribute('style')
    harita_link = str(style).replace('background-image: url("','').replace('");','')
    coordinates = extract_coordinates(harita_link)
    return coordinates[0], coordinates[1]


def extract_coordinates(url):
    pattern = re.compile(r'center=(-?\d+\.\d+)%2C(-?\d+\.\d+)')
    match = pattern.search(url)
    if match:
        return match.groups()
    return None