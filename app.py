import os
import math
import requests
import re
from dotenv import load_dotenv
from flask import Flask,render_template,request,jsonify

load_dotenv()
app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Optional config var used for populating index.html at route '/'
APP_URL = os.getenv("APP_URL")

# change env var to false to skip sending a message divider after every log entry
# or to mitigate logplex overflow in case of high traffic apps.
MESSAGE_DIVIDER_ENABLED = os.getenv("MESSAGE_DIVIDER_ENABLED","true")
MESSAGE_DIVIDER_ENABLED = True if(MESSAGE_DIVIDER_ENABLED != "false" ) else False

LONG_LOGS_ENABLED = os.getenv("LONG_LOGS_ENABLED","false")
LONG_LOGS_ENABLED = True if(LONG_LOGS_ENABLED != "false" ) else False

# Do not change this value to be more than 2000, discord api has a limit of 2000 characters per message
LONG_LOG_CHARACTER_LENGTH = 2000

@app.route('/')
def index():
    return render_template("index.html",APP_URL=APP_URL)


@app.route('/logs',methods=["POST"])
async def logs():
    LOGS = request.data.decode("utf-8")
    if(LONG_LOGS_ENABLED):
        send_batch_logs(LOGS)
    else:
        send_unary_logs(LOGS)
    return jsonify({"status":"Logged !"})


def send_unary_logs(LOGS):
    for i in LOGS.split('\n'):
        try:
            send_discord_message(re.split(">[a-zA-Z0-9]* ",i.strip())[1])
            if(MESSAGE_DIVIDER_ENABLED):
                send_discord_message("------")
        except IndexError:
            pass
    return 0

def send_batch_logs(LOGS):
    for i in range(math.ceil(len(LOGS)/LONG_LOG_CHARACTER_LENGTH)):
        try:
            send_discord_message(LOGS[i*LONG_LOG_CHARACTER_LENGTH:(i+1)*LONG_LOG_CHARACTER_LENGTH])
        except IndexError:
            pass
    return 0

def send_discord_message(message):
    payload = {"content" : message}
    headers={"Authorization" : f"Bot {BOT_TOKEN}"}
    requests.post(f"https://discord.com/api/v8/channels/{CHANNEL_ID}/messages",data=payload,headers=headers)
    return 0


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False,host='0.0.0.0', port=port,threading=True)