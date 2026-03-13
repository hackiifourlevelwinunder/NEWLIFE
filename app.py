import os
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, render_template

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30

round_results = {}

# Xoroshiro RNG
def xoroshiro(seed):
    s0 = seed & 0xFFFFFFFF
    s1 = (seed ^ 0x9E3779B9) & 0xFFFFFFFF

    while True:
        result = (s0 + s1) & 0xFFFFFFFF

        s1 ^= s0
        s0 = ((s0 << 24) | (s0 >> 8)) & 0xFFFFFFFF
        s0 ^= s1 ^ ((s1 << 16) & 0xFFFFFFFF)
        s1 = ((s1 << 37) | (s1 >> 27)) & 0xFFFFFFFF

        yield result


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

    seed = int(round_id[-4:])

    rng = xoroshiro(seed)

    numbers = []

    # generate 1000 numbers
    for _ in range(1000):
        numbers.append(next(rng) % 10)

    freq = {}

    for n in numbers:
        freq[n] = freq.get(n, 0) + 1

    result = max(freq, key=freq.get)

    return result


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    round_id, remaining = get_round_info()

    # preview at 40 sec
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
