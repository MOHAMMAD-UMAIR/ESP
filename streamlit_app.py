import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
import plotly.express as px
from pymongo import MongoClient
from stream.add_ons import (load_data,popularity_cal,load_mal,popularity_mal)


platforms=['Linux', 'macOS', 'Windows', 'Network', 'Office 365', 'Azure AD', 'IaaS', 'Google Workspace','None']
sub_type=['Yes','No']
platforms_mal=['Linux', 'Windows', 'macOS', 'Android']
sub_type_mal=['No','Yes']
st.set_page_config(layout="wide")


with st.sidebar:
 
    st.title("Sidebar Title")
    st.markdown("Version 1")
    
st.title("Adversery EDA")
st.markdown("Version 1")


def plot_bottom_center(data):
    colors = ['lightslategray',] * 10
    colors[0] = 'crimson'
    fig = px.bar(data, 
                x='popularity_percentage',
                y='attack_name', 
                orientation='h', 
                title='Top Attack Patterns')
    
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
                title='Top Malwares')
    
    # Set axis titles
    fig.update_xaxes(title_text='Popularity')
    fig.update_yaxes(title_text='Malware')
    fig.update_traces(texttemplate='%{x:.1f}%', textposition='outside',marker_color=colors)
    fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
    fig.update_traces(texttemplate='%{x}%', textposition='inside',marker_color=colors)
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

data_ad_mal= load_mal('relation.csv','malware.csv')      
tab1, tab2 = st.tabs(["Attack", "Malware"])

with tab1:
    col1, col2 , col3 ,col4 , col5= st.columns([3,3,1,1,5])
    with col1:
        filter_platform_key = st.selectbox("Filter by Platform",platforms, key=1 )
    with col2:
        filter_type_key = st.selectbox("Filter by Sub Group",sub_type , key=2 )
    df=load_data('data.csv',filter_platform_key,filter_type_key)
    plot_bottom_center(df)
        


with tab2:
    col1, col2 , col3 ,col4 , col5= st.columns([3,3,1,1,5])
    with col1:
        filter_platform_key_mal = st.selectbox("Filter by Platform",platforms_mal, key=3 )
    with col2:
        filter_type_key_mal = st.selectbox("Filter by Sub Group",sub_type_mal  ,key=4 )
    plot_bottom_center_mal(data_ad_mal)
    




    