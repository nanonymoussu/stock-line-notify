import time
import requests
import yfinance as yf


def get_stock_price(ticker):
    stock_data = yf.download(tickers=ticker, interval="1m", period="1d")
    return stock_data["Close"].iloc[-1].to_dict()


def send_notice(message):
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "Bearer ABNxcL1UkGx6eAaH78MwhV49LIvgddenXjoqwztTbpx",
    }
    data = {"message": message}
    requests.post(
        url="https://notify-api.line.me/api/notify", headers=headers, data=data
    )


tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META"]
previous_price = {}

while True:
    current_price = get_stock_price(tickers)

    for ticker, price in current_price.items():
        print(f"{ticker}:")
        if ticker in previous_price:
            change = price - previous_price[ticker]
            symbol = "+" if change >= 0 else "-"
            print(f" - Previous price: ${previous_price[ticker]:,.2f}")
            print(f" - Current price: ${price:,.2f}")
            print(f" - Difference: {symbol}{abs(change):,.2f}")
        else:
            print(f" - Price: ${price:,.2f}")

    previous_price = current_price.copy()
    time.sleep(60 * 15)
