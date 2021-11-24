from bs4 import BeautifulSoup
import requests

request=requests.get("https://www.bbc.co.uk/sport/football/teams/tottenham-hotspur/scores-fixtures")
soup=BeautifulSoup(request.content, "html.parser")

next_match=soup.find("div", class_="qa-match-block")

# print(next_match)

date_string=next_match.find_all("h3")[0].string
competition=next_match.find_all("h3")[1].string

print(date_string)
print(competition)

time=next_match.find("span", class_="sp-c-fixture__number--time").string
teams=next_match.find_all("span", class_="qa-full-team-name")

print(time)

if teams[0].string=="Tottenham Hotspur":
    is_home=True
    opposition=teams[1].string
else:
    is_home=False
    opposition=teams[0].string

print(opposition)
print(is_home)
