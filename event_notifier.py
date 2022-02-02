from bs4 import BeautifulSoup
import re
import requests
import time
from twilio.rest import Client

from app import time_to_unmute
import config
import sentiment_analyser

client = Client(config.account_sid, config.auth_token)

def generate_event_alerts(team):
    latest_match_state=get_match_data(team)
    while latest_match_state["status"]=="Upcoming":
        sleep(10)
        latest_match_state=get_match_data(team)
    # latest_match_state={"home": {"team": "Tottenham Hotspur", "score": 0, "goals": [], "red_cards": []}, "away": {"team": "Liverpool", "score": 0, "goals": [], "red_cards": []}, "status": "In Progress"}

    home_team=latest_match_state["home"]["team"]
    home_score=latest_match_state["home"]["score"]
    away_team=latest_match_state["away"]["team"]
    away_score=latest_match_state["away"]["score"]
    while latest_match_state["status"]!="FT" and time_to_unmute<=datetime.now():
        current_match_state=get_match_data(team)
        home_score=current_match_state["home"]["score"]
        away_score=current_match_state["away"]["score"]

        # Home team has scored
        if current_match_state["home"]["goals"]!=latest_match_state["home"]["goals"]:
            for goal in current_match_state["home"]["goals"]:
                if goal not in latest_match_state["home"]["goals"]:
                    message=f"{goal['scorer'].upper()} HAS SCORED FOR {home_team.upper()} ({goal['time']})! {sentiment_analyser.get_sentiment()} The score is now {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )
                    # print(message)

        # Away team has scored
        if current_match_state["away"]["goals"]!=latest_match_state["away"]["goals"]:
            for goal in current_match_state["away"]["goals"]:
                if goal not in latest_match_state["away"]["goals"]:
                    message=f"{goal['scorer'].upper()} HAS SCORED FOR {away_team.upper()} ({goal['time']})! {sentiment_analyser.get_sentiment()} The score is now {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )
                    # print(message)
        # Home player sent off
        if current_match_state["home"]["red_cards"]!=latest_match_state["home"]["red_cards"]:
            print(length(current_match_state["home"]["red_cards"]))
            for red_card in current_match_state["home"]["red_cards"]:
                if red_card not in latest_match_state["home"]["red_cards"]:
                    message=f"{red_card['player'].upper()} HAS BEEN SENT OFF FOR {home_team.upper()} FOR A {red_card['type']} CARD ({goal['time']})! {sentiment_analyser.get_sentiment()} {home_team} are down to {11-len(current_match_state['home']['red_cards'])} men with the scores at {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )
                    # print(message)

        # Away player sent off
        if current_match_state["away"]["red_cards"]!=latest_match_state["away"]["red_cards"]:
            for red_card in current_match_state["away"]["red_cards"]:
                if red_card not in latest_match_state["away"]["red_cards"]:
                    message=f"{red_card['player'].upper()} HAS BEEN SENT OFF FOR {away_team.upper()} FOR A {red_card['type'].upper()} CARD ({goal['time']})! {sentiment_analyser.get_sentiment()} {away_team} are down to {11-len(current_match_state['away']['red_cards'])} men with the scores at {home_team} {home_score}-{away_score} {away_team}."
                    text = client.messages.create(
                        body = message,
                        from_ = config.twilio_from_number,
                        to = config.twilio_to_number
                    )
                    # print(message)

        # Half time
        if current_match_state["status"]!=latest_match_state["status"] and current_match_state["status"]=="HT":
            message=f"HALF TIME: {home_team} {home_score}-{away_score} {away_team} {sentiment_analyser.get_sentiment()}"
            text = client.messages.create(
                body = message,
                from_ = config.twilio_from_number,
                to = config.twilio_to_number
            )
            sleep(15*60)

        latest_match_state=current_match_state
        time.sleep(10)

    message=f"FULL TIME: {home_team} {home_score}-{away_score} {away_team} {sentiment_analyser.get_sentiment()}"
    if time_to_unmute<=datetime.now():
        text = client.messages.create(
            body = message,
            from_ = config.twilio_from_number,
            to = config.twilio_to_number
        )
    # print(message)

def get_match_link(team):
    team=team.lower()
    team_slug=team.replace(" ", "-")

    request=requests.get(f"https://www.bbc.co.uk/sport/football/teams/{team_slug}/scores-fixtures")
    soup=BeautifulSoup(request.content, "html.parser")

    match_link=soup.find("a", class_="sp-c-fixture__block-link")["href"]

    return match_link

def get_match_data(team):

    request=requests.get(f"https://www.bbc.co.uk/{get_match_link(team)}")
    # request=requests.get("https://www.bbc.co.uk/sport/football/59625603")

    soup=BeautifulSoup(request.content, "html.parser")

    summary_header=soup.find("section", class_="sp-c-fixture--live-session-header")

    teams=summary_header.find_all("span", class_="qa-full-team-name")
    home_team=teams[0].string
    away_team=teams[1].string
    try:
        scores=summary_header.find_all("span", class_="sp-c-fixture__number")
        home_score=int(scores[0].string)
        away_score=int(scores[1].string)
    except Exception:
        match_status = "Not started"
        return {"home": {"team": home_team}, "away": {"team":away_team}, "status": match_status}


    scorer_data=summary_header.find_all("ul", class_="sp-c-fixture__scorers")
    home_goals=[]
    home_red_cards=[]
    away_goals=[]
    away_red_cards=[]

    for home_scorer in scorer_data[0].find_all("li"):
        home_scorer_data=home_scorer.find_all("span")
        name=home_scorer_data[0].string
        for i in [i for i in range(len(home_scorer_data)) if i%5==3]:
            try:
                time=home_scorer_data[i].string
                goal={"scorer": name, "time": time}
                minute=get_minute(goal)
                home_goals.append(goal)
            except Exception:
                if home_scorer.find("i", class_="sp-c-booking-card--yellow-red") is not None:
                    type = "second yellow"
                else:
                    type = "straight red"
                time = home_scorer_data[i+1].string
                red_card = {"player": name, "time": time, "type": type}
                home_red_cards.append(red_card)

            # home_goals.append( {"scorer": name, "time": time} )
    home_goals.sort(key=get_minute)

    for away_scorer in scorer_data[1].find_all("li"):
        away_scorer_data=away_scorer.find_all("span")
        name=away_scorer_data[0].string
        for i in [i for i in range(len(away_scorer_data)) if i%5==3]:
            try:
                time=away_scorer_data[i].string
                goal={"scorer": name, "time": time}
                minute=get_minute(goal)
                away_goals.append( goal )
            except Exception:
                if away_scorer.find("i", class_="sp-c-booking-card--yellow-red") is not None:
                    type = "second yellow"
                else:
                    type = "straight red"
                time = away_scorer_data[i+1].string
                red_card = {"player": name, "time": time, "type": type}
                away_red_cards.append(red_card)

            # away_goals.append( {"scorer": name, "time": time} )
    away_goals.sort(key=get_minute)

    try:
        match_status=summary_header.find("span", class_="sp-c-fixture__status").find("abbr").string
    except Exception:
        match_status="In Progress"

    return {"home": {"team": home_team, "score": home_score, "goals": home_goals, "red_cards": home_red_cards}, "away": {"team":away_team, "score": away_score, "goals": away_goals, "red_cards": away_red_cards}, "status": match_status}

def get_minute(goal):
    time=goal["time"]
    if "+" in time:
        split_time=time.split("+")
        return float(split_time[0][:-1])+0.01*float(split_time[1])
    else:
        return float(time[:-1])
