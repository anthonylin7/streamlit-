#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:20:29 2020

@author: antho

TO RUN:
    streamlit run week13_streamlit.py
    
"""

import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time



@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2


st.title('North Carolina (NC) vs. Nationwide Hospital Statistics')





# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)
  

st.write(':smile:') 
  
# Load the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()





## test testname = df_hospital_2[df_hospital_2['state<-columnname'] == 'NY'] <-- make specific 


hospitals_nc = df_hospital_2[df_hospital_2['state'] == 'NC']

#BAR CHART NC
st.subheader('Hospital Type - NC')
bar1 = hospitals_nc['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.subheader('Hospital Type - NC | PIE CHART:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

#BAR CHART
st.subheader('Hospital Type - Nationwide')
bar1 = df_hospital_2['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in the United States are *Acute Care*, followed by *Critical Access*')


st.subheader('Hospital Type - Nationwide | PIE CHART:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

st.markdown('A vast majority of hospitals in the US are acute Care, almost tripling those of Critical Access')

#OWNERSHIP BAR CHART AND PIE CHART 
ownership = df_hospital_2[df_hospital_2['hospital_ownership'] == 'Voluntary non-profit - Private']

st.subheader('Hospital Ownership - NC')
bar2 = hospitals_nc['hospital_ownership'].value_counts().reset_index()
st.dataframe(bar2)

st.subheader('Hospital Ownership - NC | PIE CHART')
fig = px.pie(bar2, values='hospital_ownership', names='index')
st.plotly_chart(fig)

#NC^ 

st.subheader('Hospital Ownership - Nationwide')
bar2 = df_hospital_2['hospital_ownership'].value_counts().reset_index()
st.dataframe(bar2)

st.subheader('Hospital Ownership - Nationwide | PIE CHART')
fig = px.pie(bar2, values='hospital_ownership', names='index')
st.plotly_chart(fig)


###----------------------------------


st.subheader('Map of NC Hospital Locations')

hospitals_nc_gps = hospitals_nc['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_nc_gps['lon'] = hospitals_nc_gps['lon'].str.strip('(')
hospitals_nc_gps = hospitals_nc_gps.dropna()
hospitals_nc_gps['lon'] = pd.to_numeric(hospitals_nc_gps['lon'])
hospitals_nc_gps['lat'] = pd.to_numeric(hospitals_nc_gps['lat'])

st.map(hospitals_nc_gps)


st.subheader('Map of Hospital Locations')

hospitals_gps = df_hospital_2['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_gps['lon'] = hospitals_gps['lon'].str.strip('(')
hospitals_gps = hospitals_gps.dropna()
hospitals_gps['lon'] = pd.to_numeric(hospitals_gps['lon'])
hospitals_gps['lat'] = pd.to_numeric(hospitals_gps['lat'])

st.map(hospitals_gps)


#----------------------
#BAR GRAPH
#Timeliness of Care
st.subheader('NC Hospitals - Timelieness of Care')
bar2 = hospitals_nc['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this bar chart, the majority of hospitals in NC have timeliness of care the same as the national average\
        while an almost equal percentage is below the national average')


st.subheader('NC Hospitals - Safety of Care')
bar2 = hospitals_nc['safety_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='safety_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this bar chart, the safety of care in NC for the majority of hospitals are above the national average')
#---------------------

#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('INPATIENT DATA - NC')


inpatient_nc = df_inpatient_2[df_inpatient_2['provider_state'] == 'NC']
total_inpatient_count = sum(inpatient_nc['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )





##Common D/C 

common_discharges = inpatient_nc.groupby('drg_definition')['total_discharges'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)



st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.beta_columns(2)

col1.header('Top 10 DRGs')
col1.dataframe(top10)

col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)

