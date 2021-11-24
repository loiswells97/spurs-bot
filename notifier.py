from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests

request=requests.get("https://www.bbc.co.uk/sport/football/teams/tottenham-hotspur/scores-fixtures")
soup=BeautifulSoup(request.content, "html.parser")

next_match=soup.find("div", class_="qa-match-block")

# print(next_match)

date_string=next_match.find_all("h3")[0].string
competition=next_match.find_all("h3")[1].string

print(date_string)
print(competition)

time_string=next_match.find("span", class_="sp-c-fixture__number--time").string
teams=next_match.find_all("span", class_="qa-full-team-name")
today=datetime.now()

modified_date_string=re.sub(r'(\d)(st|nd|rd|th)', r'\1', date_string)
print(modified_date_string)

match_datetime=datetime.strptime(modified_date_string+" "+str(today.year)+ " "+time_string, "%A %d %B %Y %H:%M")

if teams[0].string=="Tottenham Hotspur":
    is_home=True
    opposition=teams[1].string
else:
    is_home=False
    opposition=teams[0].string

print(opposition)
print(is_home)
