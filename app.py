from flask import Flask, jsonify, render_template
import time
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

ROUND_TIME = 60
PREVIEW_TIME = 40

# LCG parameters
A = 1103515245
C = 12345
M = 2**31


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

    return f"{date}10001{round_number:04d}"


def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


def lcg(seed):

    return (A * seed + C) % M


def generate_number(period):

    seed = int(period[-4:])  # last 4 digits (example 1064)

    value = lcg(seed)

    return value % 10


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()

    time_left = get_time_left()

    number = generate_number(period)

    if time_left > PREVIEW_TIME:
        number = None

    return jsonify({
        "period": period,
        "time_left": time_left,
        "number": number
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
