from bs4 import BeautifulSoup
import re
import requests
import time
from twilio.rest import Client

import config

client = Client(config.account_sid, config.auth_token)

# def generate_event_alert(match_url, previous_state):
#
#     home_team="Tottenham"
#     away_team="Arsenal"
#
#
#     if new_state["home_red_cards"]>previous_state["home_red_cards"]:
#         print(f"{home_team} have had {player_name} sent off!")
#
#     if new_state["away_red_cards"]>previous_state["away_red_cards"]:
#         print(f"{away_team} have had {player_name} sent off!")
#
#     if new_state["home_goals"]>previous_state["home_goals"]:
#         for goal in range(new_state["home_goals"]-previous_state["home_goals"])
#             print(f"{home_team.upper} HAVE SCORED! The goal was scored by {player} in the {minute}{ending} minute! The score is  now {home_team} {home_goals}:{away_goals} {away_team}.")
#
#     if new_state["away_goals"]>previous_state["away_goals"]:
#         print(f"{home_team.upper} HAVE SCORED! The goal was scored by {player} in the {minute}{ending} minute! The score is  now {home_team} {home_goals}:{away_goals} {away_team}.")
#
#
#
#     # new_state={'status': 'Upcoming/1st half/HT/2nd half/ET/Penalties/FT', 'home_score': 0, 'away_score': 0, 'home_red_cards': 0, 'away_red_cards': 0}
#     # if
#
#     return new_state

def generate_event_alerts(team):
    latest_match_state=get_match_data(team)
    # latest_match_state={"home": {"team": "Tottenham Hotspur", "score": 0, "goals": []}, "away": {"team": "West Ham United", "score": 0, "goals": []}, "status": "In Progress"}

    home_team=latest_match_state["home"]["team"]
    home_score=latest_match_state["home"]["score"]
    away_team=latest_match_state["away"]["team"]
    away_score=latest_match_state["away"]["score"]
    while latest_match_state["status"]!="FT":
        current_match_state=get_match_data(team)
        home_score=current_match_state["home"]["score"]
        away_score=current_match_state["away"]["score"]

        # Home team has scored
        if current_match_state["home"]["goals"]!=latest_match_state["home"]["goals"]:
            for goal in current_match_state["home"]["goals"]:
                if goal not in latest_match_state["home"]["goals"]:
                    message=f"{goal['scorer'].upper()} HAS SCORED FOR {home_team.upper()} ({goal['time']})! The score is now {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )


        # Away team has scored
        if current_match_state["away"]["goals"]!=latest_match_state["away"]["goals"]:
            for goal in current_match_state["away"]["goals"]:
                if goal not in latest_match_state["away"]["goals"]:
                    message=f"{goal['scorer'].upper()} HAS SCORED FOR {away_team.upper()} ({goal['time']})! The score is now {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )
        latest_match_state=current_match_state
        time.sleep(60)

    message=f"The full time score is {home_team} {home_score}-{away_score} {away_team}."
    text = client.messages.create(
        body = message,
        from_ = config.twilio_from_number,
        to = config.twilio_to_number
    )

def get_match_link(team):
    team=team.lower()
    team_slug=team.replace(" ", "-")

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/{team_slug}/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    match_link=soup.find("a", class_="sp-c-fixture__block-link")["href"]

    return match_link

def get_match_data(team):

    request=requests.get(f"https://www.bbc.co.uk/{get_match_link(team)}")
    # request=requests.get("https://www.bbc.co.uk/sport/football/59646904")

    soup=BeautifulSoup(request.content, "html.parser")

    summary_header=soup.find("section", class_="sp-c-fixture--live-session-header")

    teams=summary_header.find_all("span", class_="qa-full-team-name")
    home_team=teams[0].string
    away_team=teams[1].string
    scores=summary_header.find_all("span", class_="sp-c-fixture__number")
    home_score=scores[0].string
    away_score=scores[1].string

    scorer_data=summary_header.find_all("ul", class_="sp-c-fixture__scorers")
    home_goals=[]
    away_goals=[]

    for home_scorer in scorer_data[0].find_all("li"):
        home_scorer_data=home_scorer.find_all("span")
        name=home_scorer_data[0].string
        for i in [i for i in range(len(home_scorer_data)) if i%5==3]:
            time=home_scorer_data[i].string
            home_goals.append( {"scorer": name, "time": time} )
    home_goals.sort(key=get_minute)

    for away_scorer in scorer_data[1].find_all("li"):
        away_scorer_data=away_scorer.find_all("span")
        name=away_scorer_data[0].string
        for i in [i for i in range(len(away_scorer_data)) if i%5==3]:
            time=away_scorer_data[i].string
            away_goals.append( {"scorer": name, "time": time} )
    away_goals.sort(key=get_minute)

    try:
        match_status=summary_header.find("span", class_="sp-c-fixture__status").find("abbr").string
    except Exception:
        match_status="In Progress"

    return {"home": {"team": home_team, "score": home_score, "goals": home_goals}, "away": {"team":away_team, "score": away_score, "goals": away_goals}, "status": match_status}

def get_minute(goal):
    time=goal["time"]
    if "+" in time:
        split_time=time.split("+")
        return float(split_time[0][:-1])+0.01*float(split_time[1])
    else:
        return float(time[:-1])
