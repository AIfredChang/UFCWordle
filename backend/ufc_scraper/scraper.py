import requests
from bs4 import BeautifulSoup

URL = "http://ufcstats.com/fighter-details/f4c49976c75c5ab2"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
fighter_details = soup.find_all("li", class_= "b-list__box-list-item")
for fighter_detail in fighter_details:
    print(" ".join(fighter_detail.text.split()))

