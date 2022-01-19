import datetime
import time

import config
import event_notifier
import notifier

while True:
    for team in config.teams:
        notifier.generate_team_match_alert(team)
        if notifier.is_playing_today(team):
            kick_off_time=notifier.get_kick_off_time(team)
            print(f"Sleeping for {(kick_off_time-datetime.datetime.now()).seconds} seconds until the game...")
            time.sleep((kick_off_time-datetime.datetime.now()).seconds)
            event_notifier.generate_event_alerts(team)

    today=datetime.datetime.now()
    if today.weekday() == 6:
        sleep_days=2
        print("Sleeping until Monday...")
    else:
        sleep_days=1
        print("Sleeping until tomorrow...")
    next_alert_datetime=datetime.datetime(today.year, today.month, today.day, 10, 0, 0)+datetime.timedelta(days=sleep_days)

    time.sleep((next_alert_datetime-datetime.datetime.now()).seconds)
