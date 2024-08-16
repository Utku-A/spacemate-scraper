from flask import Flask
from map_adress import get_location_details
from database import get_items_data_db, set_items_listing_id_db
from datetime import datetime
import requests, os, pytz

app = Flask(__name__)
file_path = f'{str(app.static_folder)}/img/'
file_path = file_path.replace("\\","/").replace("/model","")

def get_token_headers(): 
    session = requests.Session()
    res_csrf_token = session.get("https://test.spacemate.io/api/auth/csrf")
    csrf_token = res_csrf_token.json()['csrfToken']

    credentials_form_data = {
        "email"         : "SM4@spacemate.io",
        "password"      : "test1",
        "redirect"      : "false",
        "csrfToken"     : csrf_token,
        "callbackUrl"   : "https://test.spacemate.io/auth/signin?callbackUrl=/",
        "json"          : "true"
    }

    res_credentials = session.post("https://test.spacemate.io/api/auth/callback/credentials",data=credentials_form_data)
    res_session = session.get("https://test.spacemate.io/api/auth/session")
    token = res_session.json()['user']['accessToken']
    return token


def add_listing(link, img_links):
    data = get_items_data_db(link)
    utc_now = datetime.now(pytz.utc)
    formatted_utc_now = utc_now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
    location_data = get_location_details(data["Maps_X"],data["MAPS_Y"])

    headers = {
        "authorization"     : get_token_headers(),
        "content-type"      : "application/json",
        "accept-language"   : "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        "origin"            : "https://test.spacemate.io",
        "priority"          : "u=1, i",
        "referer"           : "https://test.spacemate.io/",
        "sec-ch-ua"         : '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile"  : "?0",
        "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    listing_data = {
        "listingStartDate"  : formatted_utc_now,
        "title"             : data["Title"],
        "description"       : data["Detail_Text"],
        "price"             : float(data["Price"]) if data["Price"] else 0.0,
        "currency"          : data["Currency"],
        "listingType"       : 5,
        # "space"             : None,
        "country"           : location_data['ülke'],
        "streetName"        : location_data['sokak'],
        "city"              : location_data['semt_mahalle'],
        "state"             : location_data['bölge'],
        "postcode"          : location_data['posta_kodu'],
        "locationLatitude"  : data["Maps_X"],
        "locationLongitude" : data["MAPS_Y"],
        "hostTimezone"      : location_data['saat_bölgesi'],
        "listingSource"     : link,
        "rawAddress"        : location_data['ham_adres'],
        "userId"            : 365,
        "space"             : "3",
        "listingType"       : 5,
        "features"          : "",
        "unitNo"            : "",
        "accessType"        : "0",
        "accessTimeText"    : "",
        "accessTimes"       : 2,
        "width"             : 0,
        "height"            : 0,
        "length"            : 0,
        "status"            : 7
    }


    listing_response = requests.post("https://test-api.spacemate.io/listing",headers=headers ,json=listing_data)
    if listing_response.ok: 
        listing_id = listing_response.json()['id']
        set_items_listing_id_db(link,listing_id)
        count = 0
        for img in img_links:
            count += 1
            img_name = f"img-{listing_id}-{count}.jpg"
            download_img_file(img,img_name)
            upload_img(listing_id,img_name)
            delete_local_img(img_name)
        return True 

    else: return False


def dell_listing(id):
    response = requests.delete(f"https://test-api.spacemate.io/bo/listing/{id}",headers={"authorization": get_token_headers()})
    if response.ok: return True
    else: return False


def download_img_file(url,name):
    response = requests.get(url)
    response.raise_for_status()
    with open(f"{file_path}{name}", "wb") as file:
            file.write(response.content)


def delete_local_img(file_name):
    os.remove(file_path+file_name)


def upload_img(id,file_name):
    upload_file_path = f"{file_path}{file_name}"
    files = {
        'files': open(upload_file_path, 'rb') 
    }
    
    listing_response = requests.post(f"https://test-api.spacemate.io/listingImage/multiple?listingId={id}",headers={"authorization": get_token_headers()} ,files=files)
    if listing_response.ok: return True 
    else: return False
