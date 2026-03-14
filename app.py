from flask import Flask, jsonify, render_template
from datetime import datetime
import os

app = Flask(__name__)

# ===== NUMBER FORMULA =====
def generate_number(period):

    p = str(period)

    last4 = int(p[-4:])
    last3 = int(p[-3:])
    last2 = int(p[-2:])
    last1 = int(p[-1])

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
def get_color(num):

    if num in [1,3,7,9]:
        return "Green"

    elif num in [2,4,6,8]:
        return "Red"

    else:
        return "Violet"


# ===== PERIOD =====
def generate_period():

    now = datetime.utcnow()

    date = now.strftime("%Y%m%d")

    minute = now.minute + 1

    period = f"{date}1000{minute:04d}"

    return int(period)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result")
def result():

    period = generate_period()

    number = generate_number(period)

    size = big_small(number)

    color = get_color(number)

    return jsonify({
        "period": period,
        "number": number,
        "size": size,
        "color": color
    })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
