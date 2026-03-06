import os
import hashlib
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, render_template

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30


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


# 🔥 Advanced RNG
def generate_result(round_id):

    seed = round_id + datetime.now(IST).strftime("%Y%m%d%H%M")

    hash_val = hashlib.sha256(seed.encode()).hexdigest()

    base = int(hash_val,16) % 10

    minute = datetime.now(IST).minute

    # live frequency logic
    if minute % 5 == 0:
        high_freq = [7,7,9,9,1,3]
    elif minute % 4 == 0:
        high_freq = [6,6,8,8,2,4]
    elif minute % 3 == 0:
        high_freq = [5,5,0,0]
    else:
        high_freq = [base]

    selector = int(hash_val[5:10],16) % 10

    if selector < 7:
        idx = int(hash_val[10:15],16) % len(high_freq)
        number = high_freq[idx]
    else:
        number = base

    return number


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():

    round_id, remaining = get_round_info()

    if remaining <= 40:
        result = generate_result(round_id)
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
