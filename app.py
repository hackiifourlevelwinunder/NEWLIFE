from flask import Flask, jsonify, render_template
import time
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")
ROUND_TIME = 60


def get_now():
    return datetime.now(IST)


def get_reset_time():

    now = get_now()

    reset = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if now < reset:
        reset -= timedelta(days=1)

    return reset


def get_round():

    now = get_now()
    reset = get_reset_time()

    diff = now - reset

    minutes = int(diff.total_seconds() // 60) + 1

    return minutes


def get_period():

    date = get_now().strftime("%Y%m%d")

    round_number = get_round()

    period = f"{date}10001{round_number:04d}"

    return period


def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


# ===== FIXED FORMULA =====

def generate_number(period):

    period = int(period)

    p = str(period)

    last4 = int(p[-4:])
    last3 = int(p[-3:])
    last2 = int(p[-2:])
    last1 = int(p[-1])

    digit = (
        (last4 * 19) +
        (last3 * 17) +
        (last2 * 13) +
        (last1 * 11) +
        (period % 31)
    ) % 10

    return digit


def get_big_small(num):

    if num <= 4:
        return "Small"
    else:
        return "Big"


def get_color(num):

    if num in [1,3,7,9]:
        return "Green"

    elif num in [2,4,6,8]:
        return "Red"

    else:
        return "Violet"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()

    time_left = get_time_left()

    number = generate_number(period)

    return jsonify({
        "period": period,
        "time_left": time_left,
        "number": number,
        "size": get_big_small(number),
        "color": get_color(number)
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
