from flask import Flask, jsonify, render_template
import time
from datetime import datetime, timedelta
import pytz

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

    return f"{date}10001{round_number:04d}"


def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


# Formula
def calculate_digit(period):

    period = int(period[-5:])

    digit = (period % 10 + period % 9 + period % 8 + period % 7 + period % 5 + period % 3) % 10

    return digit


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()

    time_left = get_time_left()

    number = None

    # 40 second rule
    if time_left <= 40:
        number = calculate_digit(period)

    big_small = None
    if number is not None:
        big_small = "Big" if number >= 5 else "Small"

    return jsonify({
        "period": period,
        "time_left": time_left,
        "number": number,
        "big_small": big_small
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
