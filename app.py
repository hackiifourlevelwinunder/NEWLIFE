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


# 🔐 Locked Formula RNG
def calculate_digit(period):

    period = int(period[-5:])  # last digits

    last1 = period % 10
    last2 = period % 100
    last3 = period % 1000
    last4 = period % 10000

    value = (
        (last1*97) +
        (last2*89) +
        (last3*83) +
        (last4*79) +
        (period % 101) +
        (period % 97) +
        (period % 89) +
        (period % 83) +
        (period % 79) +
        (period % 73) +
        (period % 71) +
        (period % 67) +
        (period % 61) +
        (period % 59) +
        (period % 53) +
        (period % 47) +
        (period % 43) +
        (period % 41) +
        (period % 37) +
        (period % 31) +
        (period % 29) +
        (period % 23) +
        (period % 19) +
        (period % 17) +
        (period % 13) +
        (period % 11) +
        (period % 7)
    )

    digit = value % 10
    return digit


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()
    time_left = get_time_left()

    number = calculate_digit(period)

    return jsonify({
        "period": period,
        "time_left": time_left,
        "number": number
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
