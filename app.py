import os
import random
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30

last_round = None
last_result = None


def get_reset_time(now):
    reset = now.replace(hour=RESET_HOUR, minute=RESET_MINUTE, second=0, microsecond=0)
    if now < reset:
        reset -= timedelta(days=1)
    return reset


def get_round_info():
    now = datetime.now(IST)
    reset_time = get_reset_time(now)

    minutes = int((now - reset_time).total_seconds() // 60)
    round_no = minutes + 1

    date_part = now.strftime("%Y%m%d")
    round_id = f"{date_part}{FIXED_PART}{round_no:04d}"

    remaining = 60 - now.second

    return round_id, remaining


def generate_result():

    freq = [0]*10

    randint = random.randint

    for _ in range(500000):
        n = randint(0,9)
        freq[n] += 1

    return freq.index(max(freq))


@app.route("/")
def home():

    round_id, remaining = get_round_info()

    return f"""
    <h2>Live RNG</h2>
    <p>Round ID: {round_id}</p>
    <p>Time Left: {remaining}s</p>
    <p>Result will show at 40 sec</p>
    """


@app.route("/api")
def api():

    global last_round
    global last_result

    round_id, remaining = get_round_info()

    if remaining <= 40:

        if last_round != round_id:
            last_result = generate_result()
            last_round = round_id

        result = last_result

    else:
        result = None

    return jsonify({
        "round_id": round_id,
        "remaining": remaining,
        "result": result
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0", port=port)
