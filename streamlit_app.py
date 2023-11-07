import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
import plotly.express as px
from pymongo import MongoClient
from stream.add_ons import (load_data,popularity_cal,load_mal,popularity_mal)

st.set_page_config(layout="wide")
st.title("Adversary EDA")
st.markdown("This dashboard is part of an ongoing attempt to visualise MITRE ATT&CK data for finding popular Attack Patterns used by different adversaries.")

platforms=['Linux', 'macOS', 'Windows', 'Network', 'Office 365', 'Azure AD', 'IaaS', 'Google Workspace','All']
sub_type=['Yes','No']
platforms_mal=['Linux', 'Windows', 'macOS', 'Android','All']
#sub_type_mal=['intrusion-set','campaign','Both']


def plot_bottom_center(data):
    colors = ['lightslategray',] * 10
    colors[0] = 'crimson'
    fig = px.bar(data, 
                x='popularity_percentage',
                y='attack_name', 
                orientation='h', 
                title='Top Attack Patterns used by Adversaries')
    
    # Set axis titles
    fig.update_yaxes(title_text='')
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig.update_traces(texttemplate='%{x:.1f}%', textposition='outside',marker_color=colors)
    fig.update_xaxes(showline=False, showgrid=False, zeroline=False)
    fig.update_layout(
        title_x=0.5, 
        title_y=1.0,  
        width=1000,  
        height=400,
        margin=dict(t=20),
        xaxis = go.XAxis(title = '',
        showticklabels=False)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    

def plot_bottom_center_mal(data_ad_mal):
    colors = ['lightslategray',] * 10
    colors[0] = 'crimson'
    
    fig = px.bar(data_ad_mal, 
                x='popularity_percentage',
                y='name', 
                orientation='h', 
                title='Top Malwares used by Adversaries')
    
    # Set axis titles
    fig.update_yaxes(title_text='')
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig.update_traces(texttemplate='%{x:.1f}%', textposition='outside',marker_color=colors)
    fig.update_xaxes(showline=False, showgrid=False, zeroline=False)
    fig.update_layout(
        title_x=0.5, 
        title_y=1.0,  
        width=1000,  
        height=400,
        margin=dict(t=20),
        xaxis = go.XAxis(title = '',
        showticklabels=False)
    )
    st.plotly_chart(fig, use_container_width=True)

    
tab1, tab2 = st.tabs(["Attack-Patterns", "Malwares"])

with tab1:
    col1, col2 , col3 ,col4 , col5= st.columns([3,3,1,1,5])
    with col1:
        filter_platform_key = st.selectbox("Platform",platforms, key=1 )
    with col2:
        filter_type_key = st.selectbox("Is subtechnique",sub_type , key=2 )
    df=load_data('data.csv',filter_platform_key,filter_type_key)
    # col_a = st.columns([6,1,2])
    # with col_a[0]:
    plot_bottom_center(df)
    # with col_a[2]:
    #     st.markdown('_Markdown_')
    
        


with tab2:
    col1, col2 , col3 = st.columns([3,5,2])
    with col1:
        filter_platform_key_mal = st.selectbox("Platform",platforms_mal, key=3 )
    # col_g = st.columns([6,1,2])
    # with col_g[0]:
    data_ad_mal=load_mal(filter_platform_key_mal)
    plot_bottom_center_mal(data_ad_mal)
    # with col_g[2]:
    #     st.markdown('_Markdown_')




    