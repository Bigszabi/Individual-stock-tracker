"""Individual stock tracker project using the Alpha Vantage API."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

#CHANGE THESE V
STOCK = "TSLA"
NOTIFY_PERCENT = 2
#CHANGE THESE ^

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"

alphavantage_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "1min",
    "apikey": ALPHAVANTAGE_API_KEY
}

response = requests.get(ALPHAVANTAGE_ENDPOINT, params=alphavantage_params)
response.raise_for_status()
data = response.json()

dates = list(data["Time Series (Daily)"].keys())
yesterday = data["Time Series (Daily)"][dates[0]]
before_yesterday = data["Time Series (Daily)"][dates[1]]

symbol = "🔺" if float(yesterday["4. close"]) - float(before_yesterday["4. close"]) > 0 else "🔻"
difference = round(abs(float(yesterday["4. close"]) - float(before_yesterday["4. close"])) / float(yesterday["4. close"]) * 100)

if difference > NOTIFY_PERCENT:
    print(f"{STOCK}: {symbol}{difference}%")
