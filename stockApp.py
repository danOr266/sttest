
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
import scenario_generation
import other_function as of
import decimal as dl

#Inc_Exp = st.sidebar.file_uploader('File uploader', type=["csv"]   ) #Inc_Exp = pd.read_csv(Inc_Exp)

st.title('Loan Comparison App')
st.sidebar.subheader('Input - Scenarios to run')

ZB_array = np.array([10, 15, 20])
BSV_ind_array = np.array([0, 1])

ZB_to_compare = st.sidebar.multiselect(
     'Select the Zinsbindung scenarios you would like to compare?',
     ZB_array )

BSV_to_compare = st.sidebar.radio(
     'Select wheather you wish to use BSV?', BSV_ind_array )
BSV_to_compare = int(BSV_to_compare)
scenario_df = pd.DataFrame(columns=['ZB','loan_amount','interest_rate','years','payments_year', 'start_date', 'BSV_ind', 'BSV_amount', 'BSV_loan_amount'], dtype='float')

if BSV_to_compare == 0:
     BSV_amount = 0
     BSV_loan_amount = 0
else:
     BSV_ind = 1
     BSV_amount = st.sidebar.number_input(label='Enter the BSV accumulated amount + loan amount to be borrowed')
     BSV_loan_amount =  st.sidebar.number_input(label='Enter the BSV  loan amount to be repayed')

scenarios_to_compare = st.sidebar.slider('select range of Interest rate shock',min_value = -0.5, max_value=5.0, value=(0.0,3.0), step=0.5)

scenario_vector = of.drange(min(scenarios_to_compare), max(scenarios_to_compare),jump= 0.5)
st.write(scenario_vector)

for ZB in ZB_to_compare:

     with st.form(key=f'my_form{ZB}'):
          st.write(f'For the{ZB}, enter the following load details')
          loan_amount = st.number_input(label='Enter the loan amount to be borrowed')
          interest_rate = st.number_input(label='Enter the interest_rate on the loan')
          years = st.number_input(label='Enter the loan repayment length in years')
          payments_year = st.number_input(label='Enter the number of payments in a year')
          start_date = st.date_input(label = 'Selection income start projection date', value =None, min_value = date.today(), )
          st.form_submit_button(label=f'Submit_{ZB}', )
          if BSV_to_compare == 0:
               temp_df = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
               temp_df.columns = scenario_df.columns
          else :
               temp_df1 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, 0, 0, 0 ]).T
               temp_df2 = pd.DataFrame( [ZB, loan_amount, interest_rate, years, payments_year, start_date, BSV_ind, BSV_amount, BSV_loan_amount ]).T
               temp_df = pd.concat([temp_df1,temp_df2])
          temp_df.columns = scenario_df.columns
     scenario_df = pd.concat([temp_df,scenario_df])
     
st.write(scenario_df)
st.sidebar.subheader('Income Projection Input Data')

income_projection_start_date = st.sidebar.date_input(label = 'Selection income start projection date1', 
                                                       value =None, min_value = date.today())

#income_projection_start_date = income_projection_start_date.datetime.date()
income_projection_table = pd.concat([income_table.income_table(start_date = income_projection_start_date, income_p1 = 3000, income_p2 = 1700, income_increase_rate = 1.015),
                                    income_table.income_table(start_date = income_projection_start_date, income_p1 = 3000, income_p2 = 1700, income_increase_rate = 1.015, BSV_ind = 0, BSV_extra = 0)])



Scenrios_table = scenario_generation.scenario_generation(scenario_df,scenario_vector)
st.write(Scenrios_table)

st.write(income_projection_table)


st.sidebar.subheader('Zinsbindung Selection')
st.write('You are comparing the following Zinsbindung Scenarios:',  print(ZB_to_compare))
S2Compare = np.array(ZB_to_compare)
     


st.sidebar.subheader('Bausparvertag Selection')
BSV_ind_to_compare = st.sidebar.multiselect(
     'Select the Bausparvertag scenarios you would like to compare?',
     income_projection_table.BSV_ind.unique())

st.write('You are comparing the following Bausparvertag Scenarios:',  print(BSV_ind_to_compare))
st.write("""
          
""")


if any([ZB_to_compare, BSV_ind_to_compare]) is not None:
     Inc_Exp1=income_projection_table.copy()
     Inc_Exp1=Inc_Exp1[(Inc_Exp1.BSV_ind.isin(BSV_ind_to_compare))].dropna()
     
     st.subheader('Scheduled payment Comparison')
     fig = px.line(Inc_Exp1, x="Payment_Date", y="cum_net_income", color="BSV_ind")
     st.plotly_chart(fig, use_container_width=True)
     
     
     st.subheader('Cumulative Interest Comparison')
     fig = px.line(Inc_Exp1, x="Payment_Date", y="living_exp", color="BSV_ind", 
                    #line_dash="BSV_ind",    hover_name="Scenario"
                    )
     
     st.plotly_chart(fig, use_container_width=True)
#else :
 #   pass
