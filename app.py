import os
import random
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, render_template

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30

current_round = None
current_result = None


def get_reset_time(now):
    reset_time = now.replace(hour=RESET_HOUR, minute=RESET_MINUTE, second=0, microsecond=0)
    if now < reset_time:
        reset_time -= timedelta(days=1)
    return reset_time


def get_round_info():
    now = datetime.now(IST)
    reset_time = get_reset_time(now)

    total_minutes = int((now - reset_time).total_seconds() // 60)
    running_round = total_minutes + 1

    date_part = now.strftime("%Y%m%d")
    round_id = f"{date_part}{FIXED_PART}{running_round:04d}"

    remaining = 60 - now.second

    return round_id, remaining


def generate_result(round_id):

    random.seed(round_id)

    freq = {i: 0 for i in range(10)}

    for _ in range(70000):
        n = random.randint(0, 9)
        freq[n] += 1

    result = max(freq, key=freq.get)

    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    global current_round
    global current_result

    round_id, remaining = get_round_info()

    if remaining <= 40:

        if current_round != round_id:
            current_result = generate_result(round_id)
            current_round = round_id

        result = current_result

    else:
        result = None

    return jsonify({
        "round_id": round_id,
        "remaining": remaining,
        "result": result
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
