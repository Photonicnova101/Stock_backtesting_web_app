from pattern_analyzer import PatternAnalyzer

class TradingEngine:
    def __init__(self, portfolio, strategy_list):
        self.analyzer = PatternAnalyzer(strategy_list)
        self.portfolio = portfolio

    def process_market_data(self, df):
        signal = self.analyzer.analyze(df)
        latest_close = df['Close'].iloc[-1]

        if signal == 2:
            self.portfolio.buy(latest_close)
        elif signal == 1:
            self.portfolio.sell(latest_close)

        return signal
