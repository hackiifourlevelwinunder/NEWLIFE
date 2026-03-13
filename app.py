from flask import Flask, jsonify, render_template
import hashlib
import time
from datetime import datetime, timedelta

app = Flask(__name__)

ROUND_TIME = 60
PREVIEW_TIME = 40

SERVER_SEED = "ankush_super_secret_salt"


def get_today_reset():

    now = datetime.now()

    reset = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if now < reset:
        reset -= timedelta(days=1)

    return reset


def get_round():

    reset = get_today_reset()

    now = datetime.now()

    diff = now - reset

    seconds = diff.total_seconds()

    round_number = int(seconds // 60) + 1

    return round_number


def get_period():

    date = datetime.now().strftime("%Y%m%d")

    round_number = get_round()

    period = f"{date}10001{round_number:04d}"

    return period


def get_time_left():

    t = int(time.time())

    return ROUND_TIME - (t % ROUND_TIME)


def generate_number(period):

    data = f"{SERVER_SEED}-{period}"

    h = hashlib.sha256(data.encode()).hexdigest()

    number = int(h, 16) % 10

    return number


def get_size(n):

    if n >= 5:
        return "Big"
    return "Small"


def get_color(n):

    if n in [1,3,7,9]:
        return "Green"

    if n in [2,4,6,8]:
        return "Red"

    if n == 0:
        return "Red + Violet"

    if n == 5:
        return "Green + Violet"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def api():

    period = get_period()

    time_left = get_time_left()

    if time_left <= PREVIEW_TIME:

        number = generate_number(period)

        color = get_color(number)

        size = get_size(number)

    else:

        number = None

        color = None

        size = None

    return jsonify({

        "period": period,
        "time_left": time_left,
        "number": number,
        "color": color,
        "size": size

    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
