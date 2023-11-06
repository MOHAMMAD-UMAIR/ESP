import os
from box.exceptions import BoxValueError
import yaml
from src.mlProject import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import pandas as pd



@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> dict:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return content


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def extract_objects(data, object_type, columns):
    objects = []
    if isinstance(data, list):
        for item in data:
            objects.extend(extract_objects(item, object_type, columns))
    elif isinstance(data, dict):
        type_value = data.get("type")
        if type_value == object_type:
            objects.append({key: data.get(key) for key in columns})
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                objects.extend(extract_objects(value, object_type, columns))
    #logger.info(f"Data extracted sucessfuly from json")
    return objects

@ensure_annotations
def load_create_df(path:Path):
    with open(path, 'r') as file:
        data = json.load(file)

        # Extract objects for 'attack-pattern'
        object_type1 = 'attack-pattern'
        columns1 = ['id', 'name', 'x_mitre_is_subtechnique']
        objects1 = extract_objects(data, object_type1, columns1)
        df_attack = pd.DataFrame(objects1)
        #print(df_attack)
        df_attack.columns = ['attack_id', 'attack_name', 'is_subtechnique']
        
        
     
        columns_La = ['x_mitre_platforms','id', 'x_mitre_is_subtechnique']
        objects_LA = extract_objects(data, object_type1, columns_La)
        df_attack_LA = pd.DataFrame(objects_LA)
        print(df_attack)
        df_attack_LA.columns = ['platforms', 'attack_id', 'is_subtechnique']
        df_attack_LA.to_csv('df_attack_LA.csv').reset_index(drop=True)
     

        # Extract objects for 'malware'
        object_type2 = 'malware'
        columns2 = ['id', 'name']
        objects2 = extract_objects(data, object_type2, columns2)
        df_malware = pd.DataFrame(objects2)
        logger.info(f"Data frame created for malwares ")

        # Extract objects for 'relationship'
        object_type3 = 'relationship'
        columns3 = ['relationship_type', 'source_ref', 'target_ref']
        objects3 = extract_objects(data, object_type3, columns3)
        df_relationship = pd.DataFrame(objects3)
        logger.info(f"Data frame created for relationship types ")
        
        # Extract objects for 'relationship'
        object_type4 = 'intrusion-set'
        columns4 = ['id', 'name']
        objects4 = extract_objects(data, object_type4, columns4)
        df_intrusion = pd.DataFrame(objects4)
        logger.info(f"Data frame created for intrusion-sets")
        
        
        # Extract objects for 'relationship'
        object_type5 = 'campaign'
        columns5 = ['id', 'name']
        objects5 = extract_objects(data, object_type5, columns5)
        df_campaign = pd.DataFrame(objects5)
        logger.info(f"Data frame created for campaign types ")
        
        logger.info(f"Data frames creation done ")
        
    return df_attack, df_campaign, df_intrusion, df_malware, df_relationship
    
@ensure_annotations
def attack_to_adversery(df_attack,df_relationship,df_intrusion,df_campaign,file):
    merge_1 = pd.merge(df_attack, df_relationship, left_on='attack_id', right_on='target_ref', how='left')
    merge_2 = merge_1.merge(df_intrusion, left_on='source_ref', right_on='id', how='left')\
    .merge(df_campaign, left_on='source_ref', right_on='id', how='left')
    merge_2.rename(columns={'id_x': 'intrusion_id', 'name_x': 'intrusion_name','id_y':'campaign_id','name_y':'campaign_name'}, inplace=True)
    merge_2.drop(columns=['source_ref','target_ref'])
    
    logger.info(f"Table operations performed ")
    
    def group_rows(group):
        attack_id = group['attack_id'].iloc[0]
        attack_name = group['attack_name'].iloc[0]
        is_subtechnique = group['is_subtechnique'].iloc[0]

        

        adversary_details = []

        for _, row in group.iterrows():
            if not pd.isna(row['intrusion_id']):
                adversary_details.append({
                    'intrusion_id': row['intrusion_id'],
                    'intrusion_name': row['intrusion_name']
                })

            if not pd.isna(row['campaign_id']):
                adversary_details.append({
                    'campaign_id': row['campaign_id'],
                    'campaign_name': row['campaign_name']
                })

        return adversary_details
    logger.info(merge_2)
    
    result_js = merge_2.groupby(['attack_id', 'attack_name', 'is_subtechnique']).apply(group_rows).reset_index()#.to_dict()
    result_js.rename(columns={0:'adversary_details'}, inplace=True)
    #result_js = result_js[~result_js['adversary_details'].apply(lambda x: x == [])]


    result_dict = result_js.to_dict(orient='records')
    logger.info(f"Result dict made ")
    #print(result_dict)
    #json_str = json.dumps({"objects": result_dict})
    #json_str = json.dumps(result_dict, indent = 4)
    #output_path = os.path.join(output_directory, output_file)
    #with open(output_path, 'w') as file:
    #json.dump(data, file)
    if not os.path.exists(file):
        #os.makedirs(file)
        with open(file, 'w') as f:
            json.dump(result_dict,f,indent=4)
        #f.write(json_str)
    
    #json_str = json_str.replace('\n', '')

    #print(type(json_str))
    #print(json_str)
    #




# with open('tejas.json', 'w') as f:
#     f.write(json_str)
    


# @ensure_annotations
# def group_rows(group):
#     attack_id = group['attack_id'].iloc[0]
#     attack_name = group['attack_name'].iloc[0]
#     is_subtechnique = group['is_subtechnique'].iloc[0]

#     adversary_details = []

#     for _, row in group.iterrows():
#         if not pd.isna(row['intrusion_id']):
#             adversary_details.append({
#                 'intrusion_id': row['intrusion_id'],
#                 'intrusion_name': row['intrusion_name']
#             })

#         if not pd.isna(row['campaign_id']):
#             adversary_details.append({
#                 'campaign_id': row['campaign_id'],
#                 'campaign_name': row['campaign_name']
#             })

#     return adversary_details

# @ensure_annotations


# @ensure_annotations
# def create_data_frames(storage_dict):
#     data_frames = {}
#     for type_value, objects in storage_dict.items():
#         data_frames[type_value] = pd.DataFrame(objects)
#         logger.info(f"Data frames sucessfully created")
#     return data_frames

# def save_data_frames(data_frames):
#     for type_value, df in data_frames.items():
#         df.to_csv(f"{type_value}.csv", index=False)
#         logger.info(f"Data frames sucessfully saved in csv")


