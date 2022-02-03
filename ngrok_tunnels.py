import time
from pyngrok import ngrok
from twilio.rest import Client

import config

client = Client(config.account_sid, config.auth_token)

# def update_ngrok_urls():
    # while True:
http_tunnel = ngrok.connect(5001)

print(ngrok.get_tunnels())
url = http_tunnel.public_url

print(client.incoming_phone_numbers.list())


time.sleep(7.9*60*60)
ngrok.disconnect(http_tunnel.public_url)
