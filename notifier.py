from bs4 import BeautifulSoup
from datetime import datetime
import requests
import schedule
import time
from twilio.rest import Client

import config

client = Client(config.account_sid, config.auth_token)

def generate_match_alert():

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/tottenham-hotspur/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    selected_date=soup.find("li", class_="sp-c-date-picker-timeline__item--selected")
    print(selected_date)

    is_today=(selected_date.find("span", class_="gel-long-primer-bold").string == "TODAY")

    print(is_today)

    today=datetime.today()

    if is_today and today.weekday() != 6:
        next_match=soup.find("div", class_="qa-match-block")

        competition=next_match.find_all("h3")[0].string

        time_string=next_match.find("span", class_="sp-c-fixture__number--time").string
        teams=next_match.find_all("span", class_="qa-full-team-name")

        if teams[0].string=="Tottenham Hotspur":
            home_or_away="at home"
            opposition=teams[1].string
        else:
            home_or_away="away"
            opposition=teams[0].string

        message=f"Tottenham are playing {opposition} {home_or_away} today at {time_string} in the {competition}."
        text = client.messages.create(
            body = message,
            from_ = "+18506053624",
            to = "+447854324768"
        )

schedule.every().day.at("10:00").do(generate_match_alert)

while True:
    schedule.run_pending()
    time.sleep(1)
