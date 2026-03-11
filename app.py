import os
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, render_template

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30

# result storage
round_results = {}

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

    now = datetime.now(IST)

    minute = now.minute
    second = now.second

    rng1 = (minute + second + int(round_id[-1])) % 10
    rng2 = (minute * 2 + second + int(round_id[-2])) % 10
    rng3 = (minute + second * 2 + int(round_id[-3])) % 10

    numbers = [rng1, rng2, rng3]

    small = [n for n in numbers if n <= 4]
    big = [n for n in numbers if n >= 5]

    if len(small) > len(big):
        group = [0,1,2,3,4]
    elif len(big) > len(small):
        group = [5,6,7,8,9]
    else:
        group = [0,1,2,3,4,5,6,7,8,9]

    index = (minute + second + sum(numbers)) % len(group)

    return group[index]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    round_id, remaining = get_round_info()

    # result generate only once
    if remaining <= 40:

        if round_id not in round_results:
            round_results[round_id] = generate_result(round_id)

        result = round_results[round_id]

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
