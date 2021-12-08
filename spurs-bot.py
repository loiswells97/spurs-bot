import schedule
import time

import notifier

schedule.every().day.at("10:00").do(notifier.generate_match_alert)

while True:
    schedule.run_pending()
    time.sleep(1)
