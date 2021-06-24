
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import urllib
import pyodbc
from sqlalchemy import create_engine


#Setting up Database Connection
conn = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};Server=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;''')
cursor = conn.cursor()
quoted = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;")
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))


## inport data from local DB
Inc_Exp = pd.read_sql_query('''SELECT HIP.[Payment_Date]
      ,[Scenario]
      ,HIP.[BSV_ind]
	  ,[tot_Income]
      ,[living_exp]
      ,[cum_net_income]
      ,[Sched_Payment]
      ,[Tot_Payment]
      ,[Curr_Balance]
      ,[Cum_Principle]
      ,[Cum_Interest]
      ,[Cum_tot_Payment]
	  , ([cum_net_income]-isnull([Cum_tot_Payment],0)) as Real_NET
      , ([living_exp]+isnull([Tot_Payment],0)) as tot_MonthlyExp
     -- , sum()
  FROM [Zuhause].[Finance].[HausIncomeProjection] as HIP
  full join 
   [Zuhause].[Finance].[MortgageScenario] as MS
  on HIP.[Payment_Date] = MS.[Payment_Date]
  and HIP.[BSV_ind] = MS.[BSV_ind]
  order by [Scenario], [BSV_ind], [Payment_Date]''', conn)





st.title('My First App')
st.write("""
""")

option = st.sidebar.selectbox(
    'Which number do you like best?',
     ['Apple', 'Banana'])

'You selected:', option


tickerSymbol = 'GOOGL'
tickerData =  yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period = 'id', start = '2010-05-01', end = '2021-06-01')
Inc_Exp

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)
