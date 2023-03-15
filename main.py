import requests
import json
import os

# url = 'https://seatgeek.com/api/event_listings_v2?_include_seats=1&aid=225&client_id=MTY2MnwxMzgzMzIwMTU4&event_page_view_id=a3bd1cd9-0a41-408e-943b-a9200ee8620b&id=5758248&sixpack_client_id=df3dceb1-4b10-47fb-8ce4-5a63f1eb2de8'
#id for clippers game = 5758248
def get_listings(id):
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

    resp_dict = json.loads(resp.text)
    listings = resp_dict['listings']
    return listings

file_path = os.path.join(os.getcwd(), "scrape.txt")

game_ids = [5758248, 5757782, 5757781]


#listings = get_listings(5758248)
# with open('scrape.txt', 'w') as f:
#     # write the prettified HTML to the file
#     f.write(str(listings))



# with open(file_path, "r") as f:
#     listings = f.read()

seats_to_view = []

for id in game_ids:
    listings = get_listings(id)
    for listing in listings:
        if listing["s"][0] == "1" and int(listing["pf"]) < 75 and int(listing["q"]) > 1:
            print("Section =", listing["s"],"Row =", listing["r"],"Price =", listing["pf"], "Quantity =", listing["q"], "id = ", id)
            #seats_to_view.append("Section = {}, Row = {}, Price = {}, Quantity = {}, id = {}".format(listing["s"], listing["r"], listing["pf"], listing["q"], id))
#print(seats_to_view)
# print(listings[0])