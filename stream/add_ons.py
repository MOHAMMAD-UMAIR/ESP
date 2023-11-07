import streamlit as st
import pandas as pd









def popularity_cal(data):
    data['adversary_details'] = data['adversary_details'].apply(ast.literal_eval)
    popularity_df = data.explode('adversary_details').groupby('attack_id').size().reset_index(name='popularity')
    # Sort the DataFrame by popularity in descending order
    popularity_df = popularity_df.sort_values(by='popularity', ascending=False)
    popularity_df = popularity_df.merge(data[['attack_id', 'attack_name']], on='attack_id')
    popular_names = popularity_df.drop('attack_id', axis=1).reset_index(drop=True)
    return popular_names




@st.cache_data
def load_data(path:str,filter_platform_key='None',filter_type_key='No' ):
    data_La = pd.read_csv("df_attack_LA.csv")
    data = pd.read_json(path)
    data=data.to_csv("dat.csv",index=False)
    data=pd.read_csv("dat.csv")
    data = data[~data['adversary_details'].apply(lambda x: x == '[]')]
    if filter_platform_key != "None" and filter_type_key == 'No':
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[filter_data['platforms'].apply(lambda x: filter_platform_key in x)]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
        
    elif filter_platform_key != "None" and filter_type_key == 'Yes' :
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[
            (filter_data['platforms'].apply(lambda x: filter_platform_key in x)) &
            (filter_data['is_subtechnique'] == True)
             ]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
        
        
    elif filter_platform_key == "None" and filter_type_key == 'Yes' :
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[filter_data['is_subtechnique'] == True]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
    
        
    else:
        popular_names = popularity_cal(data)
        sorted_df = popular_names.sort_values(by='popularity', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)

        
        
        
        
        
    return top_10_values