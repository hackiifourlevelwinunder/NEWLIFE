from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
import pytz
import time
import os

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")
ROUND_TIME = 60


# ===== TIME =====
def get_now():
    return datetime.now(IST)


# ===== RESET 5:30 =====
def get_reset_time():

    now = get_now()

    reset = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if now < reset:
        reset -= timedelta(days=1)

    return reset


# ===== ROUND =====
def get_round():

    now = get_now()
    reset = get_reset_time()

    diff = now - reset

    minutes = int(diff.total_seconds() // 60) + 1

    return minutes


# ===== PERIOD =====
def get_period():

    date = get_now().strftime("%Y%m%d")
    round_number = get_round()

    return f"{date}10001{round_number:04d}"


# ===== COUNTDOWN =====
def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


# ===== LOCKED RNG FORMULA =====
def generate_number(period):

    p = int(period)

    last1 = p % 10
    last2 = p % 100
    last3 = p % 1000
    last4 = p % 10000

    value = (
        (last4 * 41) +
        (last3 * 37) +
        (last2 * 31) +
        (last1 * 29) +
        (p % 53) +
        (p % 23) +
        (p % 13) +
        (p % 9) +
        (p % 5)
    )

    digit = value % 10

    return digit


# ===== BIG SMALL =====
def get_size(num):

    if num >= 5:
        return "Big"
    else:
        return "Small"


# ===== COLOR =====
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

    preview = "--"

    if time_left <= 50:
        preview = number

    return jsonify({
        "period": period,
        "time_left": time_left,
        "preview": preview,
        "number": number,
        "size": get_size(number),
        "color": get_color(number)
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
