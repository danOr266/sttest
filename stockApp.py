
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import numpy_financial as npf
from datetime import *
#import plotly.figure_factory as ff
import tester
import amortisation_table
import income_table

#import urllib
#import pyodbc
#from sqlalchemy import create_engine


#Setting up Database Connection
#conn = pyodbc.connect('''Driver={ODBC Driver 17 for SQL Server};Server=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;''')
#cursor = conn.cursor()
#quoted = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;Database=Zuhause;Trusted_Connection=yes;")
#engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))



st.title('Loan Comparison App')


#Inc_Exp = st.sidebar.file_uploader('File uploader', type=["csv"]   )
#Inc_Exp = pd.read_csv(Inc_Exp)

ZB_array = np.array([10, 15, 20])


st.sidebar.subheader('Income Projection Input Data')

income_projection_start_date = st.sidebar.date_input(label = 'Selection income start projection date', 
                                                       value =None, min_value = date.today())
income_projection_table = income_table.income_table(start_date = income_projection_start_date, income_p1 = 3000, income_p2 = 1700, income_increase_rate = 1.015)

st.write(income_projection_table)

#if Inc_Exp is not None:
    
#st.sidebar.subheader('Interest Shock Selection')
#shock_to_compare = st.sidebar.multiselect(
 #    'Select the Interest Shock scenarios you would like to compare?',
  #   Inc_Exp.Shock.unique())

#st.write('You are comparing the following shock Scenarios:', print(shock_to_compare))
     

st.sidebar.subheader('Zinsbindung Selection')
ZB_to_compare = st.sidebar.multiselect(
     'Select the Zinsbindung scenarios you would like to compare?',
     ZB_array )

st.write('You are comparing the following Zinsbindung Scenarios:',  print(ZB_to_compare))

S2Compare = np.array(ZB_to_compare)
     
if S2Compare is not None :
     imported = tester.multikulti(S2Compare)
     st.write(imported)
st.write("""
          
""")


st.sidebar.subheader('Bausparvertag Selection')
BSV_ind_to_compare = st.sidebar.multiselect(
     'Select the Bausparvertag scenarios you would like to compare?',
     income_projection_table.BSV_ind.unique())

st.write('You are comparing the following Bausparvertag Scenarios:',  print(BSV_ind_to_compare))
st.write("""
          
""")


st.write(Inc_Exp)

if any([ZB_to_compare, BSV_ind_to_compare]) is not None:
     Inc_Exp1=income_projection_table.copy()
     Inc_Exp1=Inc_Exp1[(Inc_Exp1.BSV_ind.isin(BSV_ind_to_compare))].dropna()
     
     st.subheader('Scheduled payment Comparison')
     fig = px.line(Inc_Exp1, x="Payment_Date", y="tot_Income", color="BSV_ind", 
                    #line_dash="BSV_ind", 
                    hover_name="Scenario")
     
     st.plotly_chart(fig, use_container_width=True)
     
     
     st.subheader('Cumulative Interest Comparison')
     fig = px.line(Inc_Exp1, x="Payment_Date", y="living_exp", color="BSV_ind", 
                    #line_dash="BSV_ind",
                    hover_name="Scenario")
     
     st.plotly_chart(fig, use_container_width=True)
#else :
 #   pass
