import schedule
import time

import notifier

schedule.every().day.at("10:00").do(notifier.generate_match_alert)
# for team in config.teams:
#     if is_playing_today(team):


while True:
    schedule.run_pending()
    time.sleep(1)
