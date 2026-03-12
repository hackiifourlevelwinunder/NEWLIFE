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

round_results = {}
preview_numbers = {}

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


def generate_preview(round_id):

    seed = int(round_id[-4:])
    random.seed(seed)

    numbers = []

    for _ in range(21):
        numbers.append(random.randint(0,9))

    return numbers


def calculate_result(numbers):

    freq = {}

    for n in numbers:
        freq[n] = freq.get(n,0) + 1

    result = max(freq, key=freq.get)

    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    round_id, remaining = get_round_info()

    # preview start (40 sec)
    if remaining <= 40:

        if round_id not in preview_numbers:
            preview_numbers[round_id] = generate_preview(round_id)

        numbers = preview_numbers[round_id]

        if round_id not in round_results:
            round_results[round_id] = calculate_result(numbers)

        result = round_results[round_id]

    else:
        numbers = []
        result = None

    return jsonify({
        "round_id": round_id,
        "remaining": remaining,
        "preview_numbers": numbers,
        "result": result
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)
