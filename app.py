from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import time
from threading import Thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alerts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for alerts
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    target = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alert {self.ticker} > {self.target}>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set-alert', methods=['POST'])
def set_alert():
    data = request.json
    ticker = data.get("ticker")
    target = data.get("target")

    if not ticker or target is None:
        return jsonify({"message": "❌ Missing ticker or price."}), 400

    new_alert = Alert(ticker=ticker.upper(), target=target)
    db.session.add(new_alert)
    db.session.commit()

    return jsonify({"message": f"✅ Alert saved for {ticker.upper()} > {target}"})


def get_btc_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        print("Error getting BTC price:", e)
        return None

def check_alerts_loop():
    print("🔄 Starting price checker...")

    while True:
        time.sleep(10)  # Check every 10 seconds

        with app.app_context():
            alerts = Alert.query.all()
            price = get_btc_price()

            if price:
                for alert in alerts:
                    if alert.ticker.upper() == "BTC" and price > alert.target:
                        print(f"🚨 BTC is now ${price}, which is above alert {alert.target}!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    Thread(target=check_alerts_loop).start()
    app.run(debug=True)
