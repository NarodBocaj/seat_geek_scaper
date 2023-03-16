import requests
import json
import os
import smtplib
from time import sleep
from private import MY_EMAIL, MY_PASS, MY_PHONE, JOHN_PHONE

def get_listings(id): #function to get listsings (the list of dicts) from the get requests
    url = 'https://seatgeek.com/api/event_listings_v2'
    data = {
        # "_include_seats": "1",
        # "aid": "225",
        "client_id": "MTY2MnwxMzgzMzIwMTU4",
        # "event_page_view_id": 'a3bd1cd9-0a41-408e-943b-a9200ee8620b',
        "id": str(id),
        'sixpack_client_id': 'df3dceb1-4b10-47fb-8ce4-5a63f1eb2de8'
    }
    resp = requests.get(url, params = data)
    print(resp.status_code)

    resp_dict = json.loads(resp.text)   #convert the text to dict
    listings = resp_dict['listings']    #get only the listings object which is a list of all tickets
    return listings


file_path = os.path.join(os.getcwd(), "scrape.txt") #get local path to scrape.txt

games = {
    5758248: "Clippers 4/1",    #clippers game 4/1
    5757782: "Hornets 3/23",    #hornets 3/23
    5757781: "Spurs 3/21"       #spurs 3/21
}



def scrape_game_list(game_ids, low_bowl_mx_price, floor_mx_price):
    seats_to_view = []
    for id in game_ids:
        listings = get_listings(id)
        for listing in listings:
            if listing["s"][0] == "1" and int(listing["pf"]) < low_bowl_mx_price and int(listing["q"]) > 1:    #check if section starts with 1, price is < 50, and more than 1 ticket
                info = "{}, Section: {}, Row: {}, ${} each for {} tickets".format(games[id], listing["s"], listing["r"], listing["pf"], listing["q"])
                seats_to_view.append(info)
            
            elif "floor" in listing["s"] and int(listing["pf"]) < floor_mx_price and int(listing["q"]) > 1:#checking courtside tix
                info = "{}, Section: {}, Row: {}, ${} each for {} tickets".format(games[id], listing["s"], listing["r"], listing["pf"], listing["q"])
                seats_to_view.append(info)
    return '\n'.join(seats_to_view)   



def text_mssg(mssg):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(MY_EMAIL,MY_PASS)
    server.sendmail("201999999", MY_PHONE, mssg)
    server.sendmail("201999999", JOHN_PHONE, mssg)
    print("Sent Text")
    server.quit()



#print(scrape_game_list(games.keys(), 60, 300))

while True:
    text_mssg(scrape_game_list(games.keys(), 60, 300))
    sleep(10800)    #sleeping for 3 hours