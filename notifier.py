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
