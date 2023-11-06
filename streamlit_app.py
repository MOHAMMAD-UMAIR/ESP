import streamlit as st
import pandas as pd
import ast
import plotly.express as px
#import json

st.set_page_config(layout="wide")

st.title("Dash Board in the making")

st.markdown("Version 1")



@st.cache_data
def load_data(path:str):
    data = pd.read_json(path)
    data=data.to_csv("dat.csv",index=False)
    data=pd.read_csv("dat.csv")
    data = data[~data['adversary_details'].apply(lambda x: x == [])]
    data['adversary_details'] = data['adversary_details'].apply(ast.literal_eval)
    popularity_df = data.explode('adversary_details').groupby('attack_id').size().reset_index(name='popularity')
    # Sort the DataFrame by popularity in descending order
    popularity_df = popularity_df.sort_values(by='popularity', ascending=False)
    popularity_df = popularity_df.merge(data[['attack_id', 'attack_name']], on='attack_id')
    popular_names = popularity_df.drop('attack_id', axis=1).reset_index(drop=True)
    return popular_names


def plot_bottom_center():
    data=load_data('attack_pattern_to_adversery.json')
    
    fig = px.bar(data, 
                 x='popularity', 
                 y='attack_name', 
                 orientation='h', 
                 title='Top 48 Attack Patterns')

    st.plotly_chart(fig, use_container_width=True)


df=load_data('attack_pattern_to_adversery.json')
#print(df.head)
with st.expander("Data Preview"):
    st.dataframe(df)
    
    
plot_bottom_center()