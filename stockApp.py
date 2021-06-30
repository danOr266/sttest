
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
import input_columns

#Inc_Exp = st.sidebar.file_uploader('File uploader', type=["csv"]   ) #Inc_Exp = pd.read_csv(Inc_Exp)
st.set_page_config(layout="wide")
st.title('Loan Comparison App')
st.sidebar.subheader('Input - Scenarios to run')

ZB_array = np.array([10, 15, 20])
BSV_ind_array = np.array([0, 1])


start_date = st.sidebar.date_input(label = 'Selection income start projection date1', 
                                   value =None, min_value = date.today())
ZB_to_compare = st.sidebar.multiselect(
     'Select the Zinsbindung scenarios you would like to compare?',
     ZB_array )

BSV_to_compare = st.sidebar.radio(
     'Select wheather you wish to use BSV?', BSV_ind_array )
BSV_to_compare = int(BSV_to_compare)

if BSV_to_compare == 0:
     BSV_amount = 0
     BSV_ind = 0
     BSV_loan_amount = 0
else:
     BSV_ind = 1
     BSV_amount = st.sidebar.number_input(label='Enter the BSV accumulated amount + loan amount to be borrowed')
     BSV_loan_amount =  st.sidebar.number_input(label='Enter the BSV  loan amount to be repayed')

scenarios_to_compare = st.sidebar.slider('select range of Interest rate shock',min_value = -0.5, max_value=5.0, value=(0.0,3.0), step=0.5)

scenario_vector = np.array(list(of.drange(scenarios_to_compare[0],scenarios_to_compare[1],jump= 0.5)))*0.01
#st.write(scenario_vector)

if st.button('Input Loan Details', key = 'input_loan_details_key'):
     scenario_graphic1, scenario_graphic2, scenario_graphic3  = st.beta_columns(3)
     scenario_df = input_columns.input_columns(start_date, ZB_to_compare, BSV_to_compare, BSV_ind, BSV_amount, BSV_loan_amount)
     scenario_vector1 = pd.DataFrame(scenario_vector, columns=['Interest_increase'])
     with scenario_graphic1:
          st.form(key = 'scenario_graphic1')
          st.bar_chart(scenario_vector1, width= 5)
    

st.sidebar.subheader('Income Projection Input Data')



#income_projection_start_date = income_projection_start_date.datetime.date()

if st.button('Income Projection',  key = 'Income_Projection_key'):
     income_projection_table = pd.concat([income_table.income_table(start_date = start_date, income_p1 = 3000, income_p2 = 1700, income_increase_rate = 1.015),
                                    income_table.income_table(start_date = start_date, income_p1 = 3000, income_p2 = 1700, income_increase_rate = 1.015, BSV_ind = 0, BSV_extra = 0)])

if st.button('Generate loan scenario',  key = 'generate_loan_scenario_key'):
     mortgage_scenarios = scenario_generation.scenario_generation(scenario_df,scenario_vector)
     st.write(mortgage_scenarios)

     st.write(income_projection_table)


     st.sidebar.subheader('Zinsbindung Selection')
     ZB_to_compare = st.sidebar.multiselect(
          'Select the Zinsbindung scenarios you would like to compare?', ZB_to_compare)
     S2Compare_ZB = np.array(ZB_to_compare)
          

st.sidebar.subheader('Bausparvertag Selection')
BSV_ind_to_compare = st.sidebar.multiselect(
     'Select the Bausparvertag scenarios you would like to compare?',
     income_projection_table.BSV_ind.unique())
st.write("""
          
""")


if st.button('Income Projection') and st.button('Generate loan scenario') :
  
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

if any([mortgage_scenarios, income_projection_table]) is None:
     pass
else :
     income_expense = pd.merge(mortgage_scenarios, income_projection_table, how='inner',on=['Payment_Date', 'BSV_ind'])
     st.write(income_expense)
