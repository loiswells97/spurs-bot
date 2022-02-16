import datetime
from flask import Flask, request, redirect
import threading
from twilio.twiml.messaging_response import MessagingResponse

from global_vars import time_to_unmute
from ngrok_tunnels import update_ngrok_urls
from spurs_bot import spurs_bot

app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/sms", methods=['GET', 'POST'])
def reply():
    body = request.values.get('Body', None)
    response = MessagingResponse()
    now = datetime.datetime.now()

    if body.upper() == "MUTE":
        time_to_unmute = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + datetime.timedelta(days=1)
        response.message("Notifications muted until tomorrow")
    elif body.upper() == "UNMUTE":
        time_to_unmute = now
        response.message("Notifications unmuted")
    else:
        response.message("Reply with 'MUTE' to mute notifications until tomorrow or 'UNMUTE' to unmute notifications")

    return str(response)

# def flask_app():
#     global time_to_unmute
#     print("Running Flask app...")
#     print(threading.current_thread().name)
#     app.run()

if __name__ == "__main__":
    global time_to_unmute

    print("Starting Spurs Bot...")
    threading.Thread(target = spurs_bot).start()
    print("Enabling muting...")
    threading.Thread(target = update_ngrok_urls).start()
    print("Running Flask app...")
    app.run()
    # threading.Thread(target = flask_app).start()
