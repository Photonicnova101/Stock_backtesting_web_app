class PortfolioManager:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0
        self.entry_price = None
        self.trade_log = []

    def buy(self, price, qty=1):
        cost = price * qty
        if self.cash >= cost:
            self.cash -= cost
            self.position += qty
            self.entry_price = price
            self.trade_log.append(f"BUY {qty} @ {price:.2f}")

    def sell(self, price, qty=1):
        if self.position >= qty:
            revenue = price * qty
            self.cash += revenue
            self.position -= qty
            self.trade_log.append(f"SELL {qty} @ {price:.2f}")

    def portfolio_value(self, current_price):
        return self.cash + (self.position * current_price)

    def get_trade_log(self):
        return self.trade_log
