import streamlit as st
import pandas as pd
import ast




def popularity_cal(data):
    """
    Calculate the popularity of attack patterns and return the top 10 most popular ones.

    Args:
        data (pandas.DataFrame): Input DataFrame containing attack data.

    Returns:
        pandas.DataFrame: DataFrame with the top 10 popular attack patterns.
    """
    data['adversary_details'] = data['adversary_details'].apply(ast.literal_eval)
    popularity_df = data.explode('adversary_details').groupby('attack_id').size().reset_index(name='popularity')
    # Sort the DataFrame by popularity in descending order
    popularity_df['popularity_percentage'] = round((popularity_df['popularity'] / 181) * 100,2)
    
    # Sort the DataFrame by popularity_percentage in descending order
    popularity_df = popularity_df.sort_values(by='popularity_percentage', ascending=False)
    
    popularity_df = popularity_df.merge(data[['attack_id', 'attack_name']], on='attack_id')
    popular_names = popularity_df.drop('attack_id', axis=1).reset_index(drop=True)
    print(popular_names)
    return popular_names





def load_data(path:str,filter_platform_key='None',filter_type_key='No' ):
    """
    Load and process attack data based on filtering options.

    Args:
        path (str): Path to the data file.
        filter_platform_key (str): Platform filter option.
        filter_type_key (str): Subtype filter option.

    Returns:
        pandas.DataFrame: DataFrame with filtered and processed attack data.
    """
    data_La = pd.read_csv("attack.csv")
    data=pd.read_csv(path)
    #data = data[~data['adversary_details'].apply(lambda x: x == '[]')]
    if filter_platform_key != "All" and filter_type_key == 'No':
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[filter_data['platforms'].apply(lambda x: filter_platform_key in x)]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity_percentage', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
        
    elif filter_platform_key != "All" and filter_type_key == 'Yes' :
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[
            (filter_data['platforms'].apply(lambda x: filter_platform_key in x)) &
            (filter_data['is_subtechnique'] == True)
             ]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity_percentage', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
        
        
    elif filter_platform_key == "All" and filter_type_key == 'Yes' :
        filter_data = data.merge(data_La[['attack_id', 'platforms']], on='attack_id')
        filtered_df = filter_data[filter_data['is_subtechnique'] == True]
        popular_names = popularity_cal(filtered_df)
        sorted_df = popular_names.sort_values(by='popularity_percentage', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
    
        
    else:
        popular_names = popularity_cal(data)
        sorted_df = popular_names.sort_values(by='popularity_percentage', ascending=False)
        # Get the top 10 values
        top_10_values = sorted_df.head(10)
        
    return top_10_values



def load_mal(mal_plat_key):
    """
    Load and process malware data based on relationships.

    Args:
        file_rel (str): Path to the relationship data file.
        file_mal (str): Path to the malware data file.

    Returns:
        pandas.DataFrame: DataFrame with top malware data.
    """
    data_rel=pd.read_csv('relationship.csv')
    data_mal=pd.read_csv('malware.csv')

    #making common key
    data_rel.rename(columns = {'target_ref':'id'}, inplace = True)
    data_rel=data_rel[data_rel['relationship_type']=='uses']
    data_rel = data_rel[data_rel['id'].str.contains('malware')]
    data_mal_plat= data_rel.merge(data_mal[['id', 'platforms']], on='id')

    if mal_plat_key != "All" :
        data_mal_plat = data_mal_plat.dropna(subset=['platforms'])
        filtered_df = data_mal_plat[data_mal_plat['platforms'].apply(lambda x: mal_plat_key in x)]
        filtered_df = data_mal_plat[data_mal_plat['source_ref'].str.contains('intrusion-set') | data_mal_plat['source_ref'].str.contains('campaign')]
        
    else :
        filtered_df = data_mal_plat[data_mal_plat['source_ref'].str.contains('intrusion-set') | data_mal_plat['source_ref'].str.contains('campaign')]
    
    records=popularity_mal(filtered_df,data_mal)
    return records


def popularity_mal(data,data_mal):
    """
    Calculate the popularity of malware and return the top 10 most popular ones.

    Args:
        data (pandas.DataFrame): DataFrame with relationship data.
        data_mal (pandas.DataFrame): DataFrame with malware data.

    Returns:
        pandas.DataFrame: DataFrame with the top 10 popular malware.
    """
    popularity_df = data.groupby('id').size().reset_index(name='popularity')
    # Sort the DataFrame by popularity in descending order
    popularity_df['popularity_percentage'] = round((popularity_df['popularity'] / 181) * 100,2)

    # Sort the DataFrame by popularity_percentage in descending order
    popularity_df = popularity_df.sort_values(by='popularity_percentage', ascending=False)

    popularity_df = popularity_df.merge(data_mal[['id', 'name']], on='id')
    popular_names = popularity_df.drop('id', axis=1).reset_index(drop=True)
    pop_names = popular_names.head(10)
    
    return pop_names