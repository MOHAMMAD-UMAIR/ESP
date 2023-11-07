import streamlit as st
import pandas as pd
import ast
import plotly.express as px
from pymongo import MongoClient

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://st.secrets.db_username:st.secrets.db_pswd@st.secrets.cluster_name.n4ycr4f.mongodb.net/?retryWrites=true&w=majority")
#from stream.add_ons import load_data ,
#import json
#container = st.beta_container()

platforms=['Linux', 'macOS', 'Windows', 'Network', 'Office 365', 'Azure AD', 'IaaS', 'Google Workspace','None']
sub_type=['Yes','No']

st.set_page_config(layout="wide")


with st.sidebar:
 
    st.title("Sidebar Title")
    st.markdown("Version 1")
    #filter_option = st.selectbox("Select Filter Option", ["Option 1", "Option 2", "Option 3"])
    
    # Add more widgets as needed
st.title("Adversery EDA")
st.markdown("Version 1")
# Add content to the main container
#container.title("Main Content")
#container.write("This is the main content of the page.")
# Add a dropdown select box
# Create two columns
col1, col2 , col3 ,col4 , col5= st.columns([3,3,1,1,5])

# Place a dropdown in the first column
with col1:
    filter_platform_key = st.selectbox("Filter by Platform",platforms )
    
with col2:
    filter_type_key = st.selectbox("Filter by Sub Group",sub_type )

# with st.container():
#     filter_platform_key = st.selectbox("Filter by Platform",platforms )
#     filter_type_key = st.selectbox("Filter by Sub Group",sub_type )



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
    data_La = pd.read_csv("attack.csv")
    data=pd.read_csv(path)
    #data = data[~data['adversary_details'].apply(lambda x: x == '[]')]
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






def plot_bottom_center(data):
    
    fig = px.bar(data, 
                 x='attack_name',
                 y='popularity', 
                 orientation='v', 
                 title='Top Attack Patterns')
    # Set axis titles
    fig.update_xaxes(title_text='Attack Pattern')
    fig.update_yaxes(title_text='Popularity')

    # Set data labels
    fig.update_traces(texttemplate='%{y}', textposition='inside')
    fig.update_layout(bargap=0.1, bargroupgap=0.6)
    fig.update_layout(
        width=800,  # Adjust the width as needed
        height=400  # Adjust the height as needed
    )
    st.plotly_chart(fig, use_container_width=True)
    
def load_mal(file_rel, file_mal):
    data_rel=pd.read_csv('relationship.csv')
    data_mal=pd.read_csv('malware.csv')
    data_ad_to_tool=data_rel[data_rel['relationship_type']=='uses']
    data_mal_to_attack = data_ad_to_tool[data_ad_to_tool['target_ref'].str.contains('malware')]
    data_mal_to_attack = data_mal_to_attack[data_mal_to_attack['source_ref'].str.contains('intrusion-set') | data_mal_to_attack['source_ref'].str.contains('campaign')]
    d=data_mal_to_attack.groupby('target_ref').size().reset_index(name='popularity')
    popularity_df = d.sort_values(by='popularity', ascending=False)
    popularity_df.columns=['id','popularity']
    popularity_df = popularity_df.merge(data_mal[['id', 'name']], on='id')
    popular_names = popularity_df.drop('id', axis=1).reset_index(drop=True)
    top_mal = popular_names.head(5)
    return top_mal
    
    
    
def plot_bottom_center_mal(data_ad_mal):
    
    fig = px.bar(data_ad_mal, 
                 x='name',
                 y='popularity', 
                 orientation='v', 
                 title='Top Malwares Used')
    # Set axis titles
    fig.update_xaxes(title_text='Malware')
    fig.update_yaxes(title_text='Popularity')

    # Set data labels
    fig.update_traces(texttemplate='%{y}', textposition='inside')
    fig.update_layout(bargap=0.1, bargroupgap=0.6)
    fig.update_layout(
        width=300,  # Adjust the width as needed
        height=400  # Adjust the height as needed
    )
    st.plotly_chart(fig, use_container_width=True)



df=load_data('data.csv',filter_platform_key,filter_type_key)
data_ad_mal= load_mal('relation.csv','malware.csv')

    
            
tab1, tab2, tab3 = st.tabs(["Attack", "Malware","Data"])
with tab1:
    plot_bottom_center(df)
    #st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    plot_bottom_center_mal(data_ad_mal)
    #st.plotly_chart(fig, theme=None, use_container_width=True)
with tab3:
    with st.expander("Data Preview"):
            st.dataframe(df)
    