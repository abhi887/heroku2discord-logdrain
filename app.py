import os
import requests
import re
from dotenv import load_dotenv
from flask import Flask,render_template,request,jsonify

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logs',methods=["GET","POST"])
def logs():
    LOGS = request.data.decode("utf-8")
    print(f"LOGS = {LOGS}")
    # logs = '''\
    #     83 <40>1 2012-11-30T06:45:29+00:00 host app web.3 - State changed from starting to up
    #     119 <40>1 2012-11-30T06:45:26+00:00 host app web.3 - Starting process with command `bundle exec rackup config.ru -p 24405`'''
    for i in LOGS.split('\n'):
        pass
        send_discord_message(re.split(">[a-zA-Z0-9]* ",i.strip())[1])
    return jsonify({"status":"Logged !"})


def send_discord_message(message):
    payload = {"content" : message}
    headers={"Authorization" : f"Bot {BOT_TOKEN}"}
    r = requests.post(f"https://discord.com/api/v8/channels/{CHANNEL_ID}/messages",data=payload,headers=headers)
    return 1


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False,host='0.0.0.0', port=port)