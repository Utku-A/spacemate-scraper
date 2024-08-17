import requests, json

with open('timezone.json','r',  encoding='utf-8') as file:
    json_data = file.read()

timezone = json.loads(json_data)['countries']


def get_timezone_int(area):
    for list in timezone:
        if list['timezone'] == area:
            return list['timezone_int']


def get_location_details(lat, lon):
    api_key = "321daa579d2b497fadbf50b13e7c9b14"
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&format=json&apiKey={api_key}"
    response = requests.get(url)
    if response.ok:
        response_data = response.json()
        adres_1 = response_data['results'][0]['address_line1'] if 'address_line1' in response_data['results'][0] else ""
        adres_2 = response_data['results'][0]['address_line2'] if 'address_line2' in response_data['results'][0] else ""

        timezone = response_data['results'][0]['timezone']['offset_STD']
        timezone = f"GMT{timezone}",

        data = {
            "ülke"            : response_data['results'][0]['country'] if 'country' in response_data['results'][0] else None,
            "ülke_kodu"       : response_data['results'][0]['country_code'] if 'country_code' in response_data['results'][0] else None,
            "bölge"           : response_data['results'][0]['state'] if 'state' in response_data['results'][0] else None,
            "il"              : response_data['results'][0]['province'] if 'province' in response_data['results'][0] else None,
            "sokak"           : response_data['results'][0]['street'] if 'street' in response_data['results'][0] else None,
            "ilce"            : response_data['results'][0]['county'] if 'county' in response_data['results'][0] else None,
            "semt_mahalle"    : response_data['results'][0]['city'] if 'city' in response_data['results'][0] else None,
            "posta_kodu"      : response_data['results'][0]['postcode'] if 'postcode' in response_data['results'][0] else None,
            "saat_bölgesi"    : timezone, 
            "ham_adres"       : f"{adres_1} {adres_2}"
        }

        if data['il'] == None:
            data['il'] = response_data['results'][0]['state'] if 'state' in response_data['results'][0] else None

        return data
    else: return False