import time
import requests
import yfinance as yf


access_token = "ABNxcL1UkGx6eAaH78MwhV49LIvgddenXjoqwztTbpx"


class Portfolio:
    def __init__(self, starting_cash):
        self.cash = starting_cash
        self.stocks = {}

    def buy_stock(self, ticker, price, quantity=10):
        total_cost = price * quantity
        if self.cash >= self.stocks:
            if ticker in self.stocks:
                total_qty = self.stocks[ticker]["qty"] + quantity
                avg_price = (
                    (self.stocks[ticker]["avg"] * self.stocks[ticker]["qty"])
                    + total_cost
                ) / total_qty
                self.stocks[ticker] = {"qty": total_qty, "avg": avg_price}
            else:
                self.stocks[ticker] = {"qty": quantity, "avg": price}
            self.cash -= total_cost
        else:
            print("Insufficient funds to buy.")

    def sell_stock(self, ticker, price, quantity=10):
        if ticker in self.stocks:
            if self.stocks[ticker]["qty"] >= quantity:
                self.cash += price * quantity
                self.stocks[ticker]["qty"] -= quantity
                if self.stocks[ticker]["qty"] == 0:
                    del self.stocks[ticker]
            else:
                print("Not enough shares to sell.")
        else:
            print("You don't own this stock.")

    def display_portfolio(self):
        print(f"Current Cash Balance: {self.cash}")
        print("Stocks:")
        if self.stocks:
            for ticker, info in self.stocks.items():
                print(
                    f"  {ticker}: Quantity: {info['quantity']}, Avg. Price: {info['avg_price']:.2f}"
                )
        else:
            print("  Portfolio is empty")


def get_stock_price(tickers):
    stock_data = yf.download(tickers=tickers, period="1d", interval="1m")
    return stock_data["Adj Close"].iloc[-1]


def send_notice(message):
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": f"Bearer {access_token}",
    }
    data = {"message": message}
    requests.post(
        url="https://notify-api.line.me/api/notify", headers=headers, data=data
    )


def trading_simulation(tickers, threshold=0.10):
    previous_price = {}

    while True:
        current_price = get_stock_price(tickers)

        for ticker, price in current_price.items():
            print(f"{ticker}:")
            if ticker in previous_price:
                change = (price - previous_price[ticker]) / previous_price[ticker]
                symbol = "+" if change >= 0 else "-"
                if abs(change) >= threshold:
                    if change > 0:
                        print("*** Buy Signal ***")
                        print(f" - Difference: {symbol}{abs(change):,.2f}")
                        portfolio.buy_stock(ticker, price)
                    else:
                        print("*** Sell Signal ***")
                        print(f" - Difference: {symbol}{abs(change):,.2f}")
                        portfolio.sell_stock(ticker, price)
                else:
                    print(f" - Previous price: ${previous_price[ticker]:,.2f}")
                    print(f" - Current price: ${price:,.2f}")
                    print(f" - Difference: {symbol}{abs(change):,.2f}")
            else:
                print(f" - Price: ${price:,.2f}")
        previous_price = current_price.copy()
        time.sleep(60 * 1)


if __name__ == "__main__":
    starting_cash = 1_000_000  # USD
    portfolio = Portfolio(starting_cash)

    tickers = ["AAPL", "GOOG", "NVDA"]
    trading_simulation(tickers)
