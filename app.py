import os
import random
import time
from datetime import datetime, timedelta
import pytz
from flask import Flask, jsonify, render_template

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


# ---- Multiple RNG engines ----

def rng1(): return random.randint(0,9)
def rng2(): return random.SystemRandom().randint(0,9)
def rng3(): return int(time.time()*1000) % 10
def rng4(): return (random.randint(0,1000)*7) % 10
def rng5(): return (random.randint(0,9999)+3) % 10
def rng6(): return (random.randint(0,8888)*5) % 10
def rng7(): return (random.randint(0,7777)+time.time_ns()) % 10
def rng8(): return random.getrandbits(4) % 10
def rng9(): return (random.randint(0,5000)*11) % 10
def rng10(): return (random.randint(0,999)+9) % 10

rng_list = [rng1,rng2,rng3,rng4,rng5,rng6,rng7,rng8,rng9,rng10]


def generate_result():

    freq = [0]*10

    for _ in range(100000):

        r = random.choice(rng_list)

        n = int(r())

        freq[n] += 1

    return freq.index(max(freq))


@app.route("/")
def home():
    return render_template("index.html")


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
    app.run(host="0.0.0.0",port=port)
