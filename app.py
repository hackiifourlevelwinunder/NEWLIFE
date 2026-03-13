from flask import Flask, jsonify, render_template
import time
from datetime import datetime, timedelta
import pytz
from Crypto.Hash import keccak

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

ROUND_TIME = 60
PREVIEW_TIME = 40


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


# TRON style hash (Keccak256)
def tron_hash(data):

    k = keccak.new(digest_bits=256)

    k.update(data.encode())

    return k.hexdigest()


def generate_preview(period):

    h = tron_hash(period)

    # Preview 1 → last hex digit
    last_hex = h[-1]

    preview1 = int(last_hex, 16) % 10

    # Preview 2 → extract hash
    decimal_val = int(h, 16)

    preview2 = int(str(decimal_val)[-1])

    return preview1, preview2


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/result")
def result():

    period = get_period()

    time_left = get_time_left()

    p1, p2 = generate_preview(period)

    if time_left > PREVIEW_TIME:

        p1 = None
        p2 = None

    return jsonify({
        "period": period,
        "time_left": time_left,
        "preview1": p1,
        "preview2": p2
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
