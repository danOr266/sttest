
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#import plotly.figure_factory as ff


#import urllib
#import pyodbc
#from sqlalchemy import create_engine


#Setting up Database Connection
#conn = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};Server=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;''')
#cursor = conn.cursor()
#quoted = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;")
#engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))



st.title('Loan Comparison App')

Inc_Exp = st.sidebar.file_uploader('File uploader', type=["csv"]   )
Inc_Exp = pd.read_csv(Inc_Exp)
st.write("""
""")


st.write(Inc_Exp)


fig = px.line( data = Inc_Exp, x = 'Payment_Date', y = 'Cum_Interest', color="BSV_Ind", line_group="Scenario")
st.plotly_chart(fig, use_container_width=True)


tickerSymbol = 'GOOGL'
tickerData =  yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period = 'id', start = '2010-05-01', end = '2021-06-01')
tickerDf

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
