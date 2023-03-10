import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
from django.conf import settings
django.setup()
import requests
from string import ascii_lowercase
from bs4 import BeautifulSoup
from tqdm import tqdm
from ufc_scraper.models import Fighter
import json
from datetime import datetime

# Scrape all fighter links
def get_all_fighters_url():
    '''Get pandas table of all UFC fighters (Name, Height, Weight, Reach, Record, etc.)'''
    all_fighters_URL = []
    for c in tqdm(ascii_lowercase):
        URL = "http://ufcstats.com/statistics/fighters?char={}&page=all".format(c)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        rows = soup.find_all("tr", class_="b-statistics__table-row")
        for row in rows:
            links = row.find_all("a")
            if len(links) > 0 :
                all_fighters_URL.append(links[0]["href"])
    return all_fighters_URL

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


def get_all_fighter_info():
    list_of_all_fighters_info = []
    all_fighters_URL = get_all_fighters_url()
    for fighter_url in tqdm(all_fighters_URL):
        page = requests.get(fighter_url)
        soup = BeautifulSoup(page.content, "html.parser")
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

        all_event_dicts = []


        #find all events
        eventRows = soup.find_all("tr", class_= "b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click")
        for event in eventRows:
            all_event_dicts.append(parse_event_info(event))
        #"Aug. 27, 2006"
        #fighter dict
        fighter = {}
        fighter["details"] = details
        f,created = Fighter.objects.get_or_create(
            name = details["Name"],
            record = details["Record"],
            height = details["Height"],
            weight = details["Weight"],
            reach = details["Reach"],
            stance = details["STANCE"],
            dob = datetime.strptime(details["DOB"], "%b %d, %Y").date() if details["DOB"] != "--" else "2023-03-04"
        )
        fighter["events"] = all_event_dicts
        for e in all_event_dicts:
            f.event_set.create(
                opponent = e["Fighter2"],
                result = e["W/L"],
                kd1 = e["KD1"] if e["KD1"] != "--" else 0,
                kd2 = e["KD2"] if e["KD2"] != "--" else 0,
                str1 = e["STR1"] if e["STR1"] != "--" else 0,
                str2 = e["STR2"] if e["STR2"] != "--" else 0,
                td1 = e["TD1"] if e["TD1"] != "--" else 0,
                td2 = e["TD2"] if e["TD2"] != "--" else 0,
                sub1 = e["SUB1"] if e["SUB1"] != "--" else 0,
                sub2 = e["SUB2"] if e["SUB2"] != "--" else 0,
                event = e["Event"],
                date = datetime.strptime(e["Date"], "%b. %d, %Y").date() if e["Date"] != "--" else "2023-03-04",
                method = e["Method"],
                move = e["Move"],
                round = e["Round"],
                time = e["Time"]
            )
        list_of_all_fighters_info.append(fighter)

    return list_of_all_fighters_info

def write_list(a_list):
    print("Started writing list data into a json file")
    with open("fighters.json", "w") as fp:
        json.dump(a_list, fp)
        print("Done writing JSON data into .json file")

# Read list to memory
def read_list():
    # for reading also binary mode is important
    with open('names.json', 'rb') as fp:
        n_list = json.load(fp)
        return n_list


write_list(get_all_fighter_info())
# r_names = read_list()
# print('List is', r_names)
