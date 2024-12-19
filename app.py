from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        rate_sats = int(request.form["rate_sats"])
        hours = int(request.form["hours"])
        btc_price = get_btc_price_in_nzd()
        total_sats = rate_sats * hours
        total_btc = total_sats / 100_000_000
        total_nzd = total_btc * btc_price
        result = {"sats": total_sats, "nzd": round(total_nzd, 2), "btc_price": btc_price}
    return render_template("index.html", result=result)

def get_btc_price_in_nzd():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "nzd"}
    response = requests.get(url, params=params)
    return response.json()["bitcoin"]["nzd"]

if __name__ == "__main__":
    app.run(debug=True)
