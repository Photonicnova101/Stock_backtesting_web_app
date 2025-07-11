import streamlit as st
import pandas as pd
from datetime import datetime

from market_feed import MarketFeed
from portfolio_manager import PortfolioManager
from trading_engine import TradingEngine

st.set_page_config(page_title="AutoPattern Trader", layout="wide")

st.title("📈 AutoPattern Trader")

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False
if "trade_log" not in st.session_state:
    st.session_state.trade_log = []


ticker = st.text_input("Enter Ticker:", value="AAPL")
interval = st.selectbox("Select Interval:", ["1d", "1h", "5m"])
strategies = st.multiselect(
    "Choose Strategies to Run:",
    [
        "7-Candle Pattern",
        "Momentum (2 Green/Red)",
        "Rising Wedge",
        "Falling Wedge",
        "Cup and Handle",
        "Triple Top",
        "Triple Bottom"
    ],
    default=["7-Candle Pattern"]
)

# Date range selection for historical data
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime(2022, 1, 1))
with col2:
    end_date = st.date_input("End Date", value=datetime.now())


# HISTORICAL BACKTEST BUTTON
if st.button("Run Backtest on Historical Data"):
    with st.spinner("Downloading historical data from Yahoo Finance..."):
        import yfinance as yf
        df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        if df.empty:
            st.error("No data found for the selected ticker and date range.")
        else:
            df.reset_index(inplace=True)
            portfolio = PortfolioManager(initial_cash=10000)
            engine = TradingEngine(portfolio, strategy_list=strategies)
            # Simulate trading over historical data
            for i in range(10, len(df)):
                window = df.iloc[:i].copy()
                engine.process_market_data(window)
            latest_price = df['Close'].iloc[-1]
            portfolio_value = portfolio.portfolio_value(latest_price)
            log = portfolio.get_trade_log()
            st.session_state.trade_log = log
            st.subheader(f"📊 Ticker: {ticker} (Backtest)")
            st.metric("Final Price", f"${latest_price:.2f}")
            st.metric("Final Portfolio Value", f"${portfolio_value:.2f}")
            st.write("Trade Log:")
            st.json(log)

st.download_button(
    label="💾 Download Trade Log",
    data="\n".join(st.session_state.trade_log),
    file_name=f"trade_log_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
    mime="text/plain",
    disabled=len(st.session_state.trade_log) == 0
)

