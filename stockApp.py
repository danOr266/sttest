
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

st.sidebar.subheader('Scenario Selection')
shock_to_compare = st.sidebar.multiselect(
     'How would you like to be contacted?',
     Inc_Exp.Shock.unique())

st.write('You selected:', option)
st.write("""
""")


st.write(Inc_Exp)


Inc_Exp1=Inc_Exp.copy().dropna()

st.subheader('Scheduled payment Comparison')
fig = px.line(Inc_Exp1[Inc_Exp1.Shock.isin(shock_to_compare)], x="Payment_Date", y="Sched_Payment", color="Scenario", 
              line_dash="BSV_ind", hover_name="Scenario")

st.plotly_chart(fig, use_container_width=True)


st.subheader('Cumulative Interest Comparison')
fig = px.line(Inc_Exp1[Inc_Exp1.Shock.isin(shock_to_compare)], x="Payment_Date", y="Cum_Interest", color="Scenario", 
              line_dash="BSV_ind", hover_name="Scenario")

st.plotly_chart(fig, use_container_width=True)
