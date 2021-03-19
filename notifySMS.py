#!/usr/bin/python3

import requests, urllib3
from twilio.rest import Client
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add your notification phone here for SMS messages
notify_phone = "+15555551212"

# Add your Twilio number (which will be the sender)
sender_phone = "+15555551234"

# Add your own Twilio creds here
client = Client("BLANK", "BLANK")

# Add your nearby stores (five digit numbers)
stores_to_check =   ("12345","09876")

for store in stores_to_check:
    url = "https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber={0}".format(store)
    response = requests.get(url, verify = False)
    responsej = response.json()
    if (responsej["Data"]["slots"]["1"]) or (responsej["Data"]["slots"]["2"]):
        print("Found a match " + store)
        message = "Opening found at Rite Aid store number " + store + " book at riteaid.com/pharmacy/covid-qualifier"
        client.messages.create(to=notify_phone, from_=sender_phone, body=message)
    else:
        print("No opening at store " + store)
