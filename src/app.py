import streamlit as st
import pandas as pd
import time
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
    ["7-Candle Pattern", "Momentum (2 Green/Red)"],
    default=["7-Candle Pattern"]
)

# START/STOP BUTTONS
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Start Trading"):
        st.session_state.running = True
with col2:
    if st.button("🛑 Stop Trading"):
        st.session_state.running = False

# DOWNLOAD BUTTON
st.download_button(
    label="💾 Download Trade Log",
    data="\n".join(st.session_state.trade_log),
    file_name=f"trade_log_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
    mime="text/plain",
    disabled=len(st.session_state.trade_log) == 0
)

placeholder = st.empty()

# Start the live session
if st.session_state.running:
    feed = MarketFeed(ticker, interval)
    portfolio = PortfolioManager(initial_cash=10000)
    engine = TradingEngine(portfolio, strategy_list=strategies)

    session_start = time.time()
    MAX_DURATION = 600  # seconds = 10 minutes

    while st.session_state.running and (time.time() - session_start < MAX_DURATION):
        df = feed.fetch_latest_data()
        signal = engine.process_market_data(df)
        latest_price = df['Close'].iloc[-1]
        portfolio_value = portfolio.portfolio_value(latest_price)
        log = portfolio.get_trade_log()
        st.session_state.trade_log = log

        with placeholder.container():
            st.subheader(f"📊 Ticker: {ticker}")
            st.metric("Current Price", f"${latest_price:.2f}")
            st.metric("Portfolio Value", f"${portfolio_value:.2f}")
            st.write("Trade Log:")
            st.json(log)

        time.sleep(30)  # Adjustable interval

    # Automatically stop after max duration
    st.session_state.running = False
    st.success("✅ Trading session ended.")

