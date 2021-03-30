#!/usr/bin/python3

import requests, urllib3
from twilio.rest import Client

client = Client("<INSERT>", "<INSERT>")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

zip_codes = ['<INSERT>']

stores_to_check = []

for zip in zip_codes: # I set this to 30mi radius, you can set lower, at least for time being PREF-112 URL query param should be kept to ensure location offers covid vax
        url = "https://www.riteaid.com/services/ext/v2/stores/getStores?address={0}".format(zip) + "&attrFilter=PREF-112&fetchMechanismVersion=2&radius=30"
        response = requests.get(url, verify = False)
        responsej = response.json()
        for s in range(0,len(responsej['Data']['stores'])):
                stores_to_check.append(responsej['Data']['stores'][s]['storeNumber'])
                
stores_to_check_dd = []

[stores_to_check_dd.append(x) for x in stores_to_check if x not in stores_to_check_dd] # remove dupes in overlap between zips

# from the stores in our geo range, let's check slot availaibility
for store in stores_to_check_dd:
    url = "https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber={0}".format(store)
    response = requests.get(url, verify = False)
    responsej = response.json()
    if (responsej["Data"]["slots"]["1"]) or (responsej["Data"]["slots"]["2"]):
        s = str(store)
        print("Found a match " + s)
        if len(s) == 4: # deal with padding of 0's
            s = "0" + s
        if len(s) == 3:
            s = "00" + s
        # send a sms telling open availability for appt
        message = "Opening found at Rite Aid store number " + s + " book at riteaid.com/pharmacy/covid-qualifier; store details at https://www.riteaid.com/locations/search.html?id=" + s
        client.messages.create(to="<INSERT>", from_="<INSERT>", body=message)
    else:
        print("No opening at store " + str(store))
