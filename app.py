import datetime
from flask import Flask
import threading
from twilio.twiml.messaging_response import MessagingResponse

from spurs_bot import spurs_bot

app = Flask(__name__)

time_to_unmute = datetime.datetime.now()
threading.Thread(target = spurs_bot).start()


@app.route("/")
def hello():
  return "Hello World!"

@app.route("/sms", methods=['POST'])
def reply():
    body = request.values.get('Body', None)
    repsonse = MessagingResponse()
    now = datetime.datetime.now()

    if body.upper == "MUTE":
        time_to_unmute = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        response.message("Notifications muted until tomorrow")
    elif body.upper == "UNMUTE":
        time_to_unmute = now
        response.message("Notifications unmuted")
    else:
        response.message("Reply with 'MUTE' to mute notifications until tomorrow or 'UNMUTE' to unmute notifications")

    return str(response)

if __name__ == "__main__":
  app.run()
