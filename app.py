from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random
import pytz

app = Flask(__name__)

IST = pytz.timezone("Asia/Kolkata")

FIXED_PART = "10001"
RESET_HOUR = 5
RESET_MINUTE = 30

round_results = {}

def get_current_time():
    return datetime.now(IST)

def get_today_reset(now):
    reset_time = now.replace(hour=RESET_HOUR, minute=RESET_MINUTE, second=0, microsecond=0)
    if now < reset_time:
        reset_time -= timedelta(days=1)
    return reset_time

def get_round_info():
    now = get_current_time()
    reset_time = get_today_reset(now)

    diff_minutes = int((now - reset_time).total_seconds() // 60)
    running_round = diff_minutes + 1

    date_part = now.strftime("%Y%m%d")
    round_id = f"{date_part}{FIXED_PART}{running_round:04d}"

    seconds_in_minute = now.second
    remaining = 60 - seconds_in_minute

    return round_id, remaining

def generate_result(round_id):
    if round_id not in round_results:
        round_results[round_id] = random.randint(0, 9)
    return round_results[round_id]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    round_id, remaining = get_round_info()

    if remaining <= 40:
        result = generate_result(round_id)
    else:
        result = None

    history = list(round_results.items())[-2:]

    return jsonify({
        "round_id": round_id,
        "remaining": remaining,
        "result": result,
        "history": history
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
