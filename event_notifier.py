from bs4 import BeautifulSoup
import requests

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
    try:
        match_status=summary_header.find("span", class_="sp-c-fixture__status").find("abbr").string
    except Exception:
        match_status="In Progress"

    return {"home": {"team": home_team}, "away": {"team":away_team}, "status": match_status}
