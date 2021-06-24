
import yfinance as yf
import streamlit as st
import pandas as pd


st.title('My First App')
st.write("""
""")

tickerSymbol = 'GOOGL'
tickerData =  yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period = 'id', start = '2010-05-01', end = '2021-06-01')
tickerDf


st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
