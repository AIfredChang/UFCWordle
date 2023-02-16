import requests
from bs4 import BeautifulSoup

URL = "http://ufcstats.com/fighter-details/f4c49976c75c5ab2"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")


# Parse fighter info from this format eg:"Key: Value" and return strings key and value
def parse_fighter_info(info):
    return info.text.split(":")[0].strip(), info.text.split(":")[1].strip()

CATEGORIES = ["W/L", "Fighter1", "Fighter2", "KD1", "KD2", "STR1", "STR2", "TD1", "TD2", "SUB1", "SUB2", "Event", "Date", "Method", "Move", "Round", "Time"]
# Parse event info and return a dictionary of event info
def parse_event_info(event):
    event_dict = {}
    categories_iter = iter(CATEGORIES)
    for col in event.findAll('p'):
        event_dict[next(categories_iter)]= col.text.strip()
    return event_dict

details = {}
#name
details["Name"] = soup.find_all("span", class_= "b-content__title-highlight")[0].text.strip()
#record
record = soup.find_all("span", class_= "b-content__title-record")[0]
key, value  = parse_fighter_info(record)
details[key] = value
#details
fighter_details = soup.find_all("li", class_= "b-list__box-list-item")
#
for fighter_detail in fighter_details[:5]:
    key, value = parse_fighter_info(fighter_detail)
    details[key] = value

print(details)

all_event_dicts = []


#find all events
eventRows = soup.find_all("tr", class_= "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
for event in eventRows:
    all_event_dicts.append(parse_event_info(event))

print(all_event_dicts)

