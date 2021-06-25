
import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#import plotly.figure_factory as ff
import tester

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



if Inc_Exp is not None:
    
    st.sidebar.subheader('Interest Shock Selection')
    shock_to_compare = st.sidebar.multiselect(
         'Select the Interest Shock scenarios you would like to compare?',
         Inc_Exp.Shock.unique())
    
    st.write('You are comparing the following shock Scenarios:', print(shock_to_compare))
    if shock_to_compare is not None:
        imported = tester.multikulti(list(shock_to_compare))
        st.write(imported)
    
    
    st.sidebar.subheader('Zinsbindung Selection')
    ZB_to_compare = st.sidebar.multiselect(
         'Select the Zinsbindung scenarios you would like to compare?',
         Inc_Exp.ZB.unique())
    
    st.write('You are comparing the following Zinsbindung Scenarios:',  print(ZB_to_compare))
    st.write("""
             
    """)
    
    
    st.sidebar.subheader('Bausparvertag Selection')
    BSV_ind_to_compare = st.sidebar.multiselect(
         'Select the Bausparvertag scenarios you would like to compare?',
         Inc_Exp.BSV_ind.unique())
    
    st.write('You are comparing the following Bausparvertag Scenarios:',  print(BSV_ind_to_compare))
    st.write("""
             
    """)
    
    
    st.write(Inc_Exp)
    
    if any([ZB_to_compare, BSV_ind_to_compare, shock_to_compare]) is not None:
        Inc_Exp1=Inc_Exp.copy()
        Inc_Exp1=Inc_Exp1[(Inc_Exp1.Shock.isin(shock_to_compare))&(Inc_Exp1.ZB.isin(ZB_to_compare))&(Inc_Exp1.BSV_ind.isin(BSV_ind_to_compare))].dropna()
        
        st.subheader('Scheduled payment Comparison')
        fig = px.line(Inc_Exp1, x="Payment_Date", y="Sched_Payment", color="Scenario", 
                      line_dash="BSV_ind", hover_name="Scenario")
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.subheader('Cumulative Interest Comparison')
        fig = px.line(Inc_Exp1, x="Payment_Date", y="Cum_Interest", color="Scenario", 
                      line_dash="BSV_ind", hover_name="Scenario")
        
        st.plotly_chart(fig, use_container_width=True)
else :
    pass
