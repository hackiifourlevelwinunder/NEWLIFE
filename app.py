from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
import pytz
import time
import os

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")
ROUND_TIME = 60


# ===== CURRENT TIME =====
def get_now():
    return datetime.now(IST)


# ===== RESET TIME 5:30 AM =====
def get_reset_time():

    now = get_now()

    reset = now.replace(hour=5, minute=30, second=0, microsecond=0)

    if now < reset:
        reset -= timedelta(days=1)

    return reset


# ===== ROUND NUMBER =====
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

    period = f"{date}10001{round_number:04d}"

    return period


# ===== COUNTDOWN =====
def get_time_left():

    now = int(time.time())

    return ROUND_TIME - (now % ROUND_TIME)


# ===== FORMULA (NO BUG) =====
def generate_number(period):

    period_int = int(period)

    p = str(period_int)

    last4 = int(p[-4:])
    last3 = int(p[-3:])
    last2 = int(p[-2:])
    last1 = int(p[-1])

    calc = (
        last4 * 19 +
        last3 * 17 +
        last2 * 13 +
        last1 * 11 +
        (period_int % 31)
    )

    digit = calc % 10

    return digit


# ===== SIZE =====
def get_size(num):

    if num <= 4:
        return "Small"
    else:
        return "Big"


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

    preview = None

    # ===== 50 SECOND PREVIEW =====
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


# ===== SERVER START =====
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
