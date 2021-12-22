from bs4 import BeautifulSoup
from datetime import datetime
import requests
import schedule
import string
import time
from twilio.rest import Client

import config

client = Client(config.account_sid, config.auth_token)

def generate_match_alert():
    for team in config.teams:
        generate_team_match_alert(team)

def generate_team_match_alert(team):
    team=team.lower()
    team_slug=team.replace(" ", "-")

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/{team_slug}/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    selected_date=soup.find("li", class_="sp-c-date-picker-timeline__item--selected")

    is_today=(selected_date.find("span", class_="gel-long-primer-bold").string == "TODAY")

    today=datetime.today()

    if is_today and today.weekday() != 6:
        next_match=soup.find("div", class_="qa-match-block")

        competition=next_match.find_all("h3")[0].string

        time_string=next_match.find("span", class_="sp-c-fixture__number--time").string
        teams=next_match.find_all("span", class_="qa-full-team-name")

        if teams[0].string==string.capwords(team):
            home_or_away="at home"
            opposition=teams[1].string
        else:
            home_or_away="away"
            opposition=teams[0].string

        message=f"{string.capwords(team)} are playing {opposition} {home_or_away} today at {time_string} in the {competition}."
        text = client.messages.create(
            body = message,
            from_ = config.twilio_from_number,
            to = config.twilio_to_number
        )
    else:
        print(f"{string.capwords(team)} are not playing today.")

def is_playing_today(team):
    team=team.lower()
    team_slug=team.replace(" ", "-")

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/{team_slug}/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    selected_date=soup.find("li", class_="sp-c-date-picker-timeline__item--selected")

    is_today=(selected_date.find("span", class_="gel-long-primer-bold").string == "TODAY")

    return is_today

def get_kick_off_time(team):
    team=team.lower()
    team_slug=team.replace(" ", "-")

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/{team_slug}/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    selected_date=soup.find("li", class_="sp-c-date-picker-timeline__item--selected")

    is_today=(selected_date.find("span", class_="gel-long-primer-bold").string == "TODAY")

    if not is_today:
        return
    else
        time_string=next_match.find("span", class_="sp-c-fixture__number--time").string
        return time_string
