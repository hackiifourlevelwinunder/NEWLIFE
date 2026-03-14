from flask import Flask, jsonify
import time
from datetime import datetime

app = Flask(__name__)

# ===== NUMBER GENERATE FORMULA =====
def generate_number(period):

    last4 = int(str(period)[-4:])
    last3 = int(str(period)[-3:])
    last2 = int(str(period)[-2:])
    last1 = int(str(period)[-1])

    digit = (
        (last4 * 19) +
        (last3 * 17) +
        (last2 * 13) +
        (last1 * 11) +
        (period % 31)
    ) % 10

    return digit


# ===== BIG SMALL =====
def big_small(num):
    if num <= 4:
        return "Small"
    else:
        return "Big"


# ===== COLOR =====
def color(num):
    if num in [1,3,7,9]:
        return "Green"
    elif num in [2,4,6,8]:
        return "Red"
    else:
        return "Violet"


# ===== PERIOD =====
def get_period():

    now = datetime.utcnow()

    date = now.strftime("%Y%m%d")

    minute = now.hour * 60 + now.minute

    period = f"{date}1000{minute:04d}"

    return int(period)


# ===== RESULT API =====
@app.route("/result")
def result():

    period = get_period()

    number = generate_number(period)

    size = big_small(number)

    clr = color(number)

    return jsonify({
        "period": period,
        "number": number,
        "size": size,
        "color": clr
    })


# ===== RUN SERVER =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
