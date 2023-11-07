# ESProfiler data scientist challenge

## Transform


### Parsing and Transforming
Two main utility functions located in /utils/common.py were created :
* For parsing the json file ```load_create_df()```<br>
The function loads JSON data from the specified file and processes it to create DataFrames for various object types. It extracts 'attack-pattern', 'malware', 'relationship', 'intrusion-set', and 'campaign' objects and stores them in separate DataFrames. These DataFrames are then saved as CSV files and returned as a tuple.

* For generating the desired file format of objects ```attack_to_adversary()``` <br>
The function combines information from 'attack', 'relationship', 'intrusion-set', and 'campaign' DataFrames to create an 'attack_to_adversary' JSON structure, mapping all  the adversaries under unique attack-patterns.
    - An inner join links 'attack' and 'relationship' data based on 'attack_id' and 'target_ref'.
    - A left join merges the result with 'intrusion' data, connecting 'source_ref' and 'id'.
    - Column renaming enhances clarity by providing more meaningful names.
    - Grouping and aggregation create a structured 'adversary' JSON structure.

In summary, these joins and aggregation steps integrate data, resulting in a concise representation of adversary details for each attack pattern.



### Saving "attack_pattern_to_adversary.json"
The transformed json data file gets stored in /artifacts/data_transformation folder. The entire project's folder structure is as follows:

```bash
    ESP
        ├───.github
        ├───.streamlit
        ├───artifacts
        │   ├───data_ingestion
        │   └───data_transformation
        ├───config
        ├───research
        ├───src
        │   └───mlProject
        └───stream
            └───
```

## Display
Link of the streamlit dashboard : https://esp-dsc.streamlit.app/


## Additional Info
* Tools and Technology
    - IDE: VSCode
    - Language : Python
    - Version Control : GitHub & GitLab
    - Visualisation : Streamlit

* Challenges Faced
    - Understanding the data and relationships : <br>
        In the beginning of the project, it took me some time to understand what the data actually represent. I had to go back and forth to understand the meaning of different types of objects and how they link with each other. The MITRE ATT&CK website proved to be a valuable resource, helping me in the process of understanding the relationship between objects.
    - It was also a good exercise on building a well-working Extract and Transform pipeline. I had earlier knowledge about building pipelines, and this project helped me solidify and build upon that experience.
 
* Future Work
    - Using MongoDB to store records.
    - Adding more key metrics to the dashboard. 







