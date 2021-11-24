from bs4 import BeautifulSoup
from datetime import datetime
import re
import requests
import schedule
import time

def generate_match_alert():

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
        home_or_away="at home"
        opposition=teams[1].string
    else:
        home_or_away="away"
        opposition=teams[0].string

    print(opposition)
    print(home_or_away)

    is_today=(match_datetime.date()==today.date())
    print(is_today)

    if is_today:
        message=f"Tottenham are playing {opposition} {home_or_away} today at {time_string}."
        print(message)

schedule.every().day.at("10:00").do(generate_match_alert)

while True:
    schedule.run_pending()
    time.sleep(1)
