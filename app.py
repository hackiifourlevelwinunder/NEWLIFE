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

    # next minute round logic
    running_round = total_minutes + 1

    date_part = now.strftime("%Y%m%d")
    round_id = f"{date_part}{FIXED_PART}{running_round:04d}"

    remaining = 60 - now.second

    return round_id, remaining, running_round


# Time + Round deterministic RNG
def generate_result(round_id):
    combined = round_id
    hash_value = hashlib.sha256(combined.encode()).hexdigest()
    return int(hash_value, 16) % 10


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    round_id, remaining, running_round = get_round_info()

    if remaining <= 40:
        result = generate_result(round_id)
    else:
        result = None

    # History (last 2 rounds)
    history = []
    now = datetime.now(IST)
    reset_time = get_reset_time(now)
    total_minutes = int((now - reset_time).total_seconds() // 60)

    for i in range(1, 3):
        prev_round = total_minutes - i + 1
        if prev_round >= 0:
            prev_id = f"{now.strftime('%Y%m%d')}{FIXED_PART}{prev_round:04d}"
            prev_result = generate_result(prev_id)
            history.append([prev_id, prev_result])

    return jsonify({
        "round_id": round_id,
        "remaining": remaining,
        "result": result,
        "history": history
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
