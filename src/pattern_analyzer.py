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
        if "Rising Wedge" in self.strategies:
            signals.append(self._rising_wedge_pattern(df))
        if "Falling Wedge" in self.strategies:
            signals.append(self._falling_wedge_pattern(df))
        if "Cup and Handle" in self.strategies:
            signals.append(self._cup_and_handle_pattern(df))
        if "Triple Top" in self.strategies:
            signals.append(self._triple_top_pattern(df))
        if "Triple Bottom" in self.strategies:
            signals.append(self._triple_bottom_pattern(df))
    def _cup_and_handle_pattern(self, df):
        # Cup and Handle: U-shaped bottom followed by a small consolidation (handle), then breakout
        if len(df) < 20:
            return 0
        closes = df['Close'].iloc[-20:]
        min_idx = closes.idxmin()
        min_pos = closes.index.get_loc(min_idx)
        # Cup: left and right sides higher than the middle
        if min_pos > 4 and min_pos < 15:
            left = closes.iloc[:min_pos]
            right = closes.iloc[min_pos+1:]
            if left.mean() > closes.iloc[min_pos] and right.mean() > closes.iloc[min_pos]:
                # Handle: last 3-5 bars slight dip, then breakout
                handle = closes.iloc[-5:]
                if handle.min() > closes.iloc[min_pos] and closes.iloc[-1] > handle.max() * 0.98:
                    return 2  # Buy signal
        return 0

    def _triple_top_pattern(self, df):
        # Triple Top: three peaks at similar levels, bearish reversal
        if len(df) < 15:
            return 0
        highs = df['High'].iloc[-15:]
        peaks = highs[(highs.shift(1) < highs) & (highs.shift(-1) < highs)]
        if len(peaks) >= 3:
            peaks = peaks.sort_values(ascending=False)[:3]
            if np.ptp(peaks.values) < 0.02 * peaks.mean():
                # Confirm with breakdown
                if df['Close'].iloc[-1] < df['Low'].iloc[-2]:
                    return 1  # Sell signal
        return 0

    def _triple_bottom_pattern(self, df):
        # Triple Bottom: three troughs at similar levels, bullish reversal
        if len(df) < 15:
            return 0
        lows = df['Low'].iloc[-15:]
        troughs = lows[(lows.shift(1) > lows) & (lows.shift(-1) > lows)]
        if len(troughs) >= 3:
            troughs = troughs.sort_values()[:3]
            if np.ptp(troughs.values) < 0.02 * troughs.mean():
                # Confirm with breakout
                if df['Close'].iloc[-1] > df['High'].iloc[-2]:
                    return 2  # Buy signal
        return 0

        if 2 in signals:
            return 2  # Buy if any strategy says BUY
        if 1 in signals:
            return 1  # Sell if any strategy says SELL
        return 0
    def _rising_wedge_pattern(self, df):
        # Rising wedge: price makes higher highs and higher lows, but the slope of the lows is steeper than the highs (bearish reversal)
        if len(df) < 6:
            return 0
        highs = df['High'].iloc[-6:]
        lows = df['Low'].iloc[-6:]
        # Calculate slopes
        x = np.arange(6)
        high_slope = np.polyfit(x, highs, 1)[0]
        low_slope = np.polyfit(x, lows, 1)[0]
        # Both slopes positive, but low_slope > high_slope
        if high_slope > 0 and low_slope > 0 and low_slope > high_slope * 1.2:
            # Confirm with a recent breakdown (close below last low)
            if df['Close'].iloc[-1] < lows.iloc[-2]:
                return 1  # Sell signal
        return 0

    def _falling_wedge_pattern(self, df):
        # Falling wedge: price makes lower highs and lower lows, but the slope of the highs is steeper than the lows (bullish reversal)
        if len(df) < 6:
            return 0
        highs = df['High'].iloc[-6:]
        lows = df['Low'].iloc[-6:]
        x = np.arange(6)
        high_slope = np.polyfit(x, highs, 1)[0]
        low_slope = np.polyfit(x, lows, 1)[0]
        # Both slopes negative, but high_slope < low_slope
        if high_slope < 0 and low_slope < 0 and high_slope < low_slope * 1.2:
            # Confirm with a recent breakout (close above last high)
            if df['Close'].iloc[-1] > highs.iloc[-2]:
                return 2  # Buy signal
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


