import numpy as np

class PatternAnalyzer:
    def __init__(self, strategies):
        self.strategies = strategies  # list of selected strategies

    def analyze(self, df):
        if len(df) < 4:
            return 0

        signals = []
        if "7-Candle Pattern" in self.strategies:
            signals.append(self._seven_candle_pattern(df))
        if "Momentum (2 Green/Red)" in self.strategies:
            signals.append(self._momentum_pattern(df))

        if 2 in signals:
            return 2  # Buy if any strategy says BUY
        if 1 in signals:
            return 1  # Sell if any strategy says SELL
        return 0

    def _seven_candle_pattern(self, df):
        try:
            current_pos = df.index.get_loc(df.index[-1])
            c1 = df['High'].iloc[current_pos] > df['High'].iloc[current_pos-1]
            c2 = df['High'].iloc[current_pos-1] > df['Low'].iloc[current_pos]
            c3 = df['Low'].iloc[current_pos] > df['High'].iloc[current_pos-2]
            c4 = df['High'].iloc[current_pos-2] > df['Low'].iloc[current_pos-1]
            c5 = df['Low'].iloc[current_pos-1] > df['High'].iloc[current_pos-3]
            c6 = df['High'].iloc[current_pos-3] > df['Low'].iloc[current_pos-2]
            c7 = df['Low'].iloc[current_pos-2] > df['Low'].iloc[current_pos-3]
            if all([c1, c2, c3, c4, c5, c6, c7]):
                return 2
            c1 = df['Low'].iloc[current_pos] < df['Low'].iloc[current_pos-1]
            c2 = df['Low'].iloc[current_pos-1] < df['High'].iloc[current_pos]
            c3 = df['High'].iloc[current_pos] < df['Low'].iloc[current_pos-2]
            c4 = df['Low'].iloc[current_pos-2] < df['High'].iloc[current_pos-1]
            c5 = df['High'].iloc[current_pos-1] < df['Low'].iloc[current_pos-3]
            c6 = df['Low'].iloc[current_pos-3] < df['High'].iloc[current_pos-2]
            c7 = df['High'].iloc[current_pos-2] < df['High'].iloc[current_pos-3]
            if all([c1, c2, c3, c4, c5, c6, c7]):
                return 1
        except:
            return 0
        return 0

    def _momentum_pattern(self, df):
        if len(df) < 3:
            return 0
        c1 = df['Close'].iloc[-1] > df['Close'].iloc[-2]
        c2 = df['Close'].iloc[-2] > df['Close'].iloc[-3]
        if c1 and c2:
            return 2
        if not c1 and not c2:
            return 1
        return 0


