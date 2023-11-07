# ESProfiler data scientist challenge

Thank you in advance for taking the time to attempt our data science challenge. 

## Overview

The Mitre Attack Stix data is a complex json file containing data about adversaries and their techniques. Unfortunately it is arranged in a relatively flat array that makes it hard for us to clearly see all the techniques and how popular these are.
We would like you to take this data and transform it into a more helpful format for our purposes.
For bonus points we would like you to create two charts based on the transformed data.

## Transform

* Get the [Mitre attack](https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack-14.0.json) stix data from github - this is a large json file.
* The file contains a large array of objects, including objects representing adversaries (ie hackers etc) and their techniques.
* The array of adversaries and techniques is supplemented with a second array that explains the relationship between adversaries and their techniques.
* As you will see, there is also other information in the first array, e.g. objects describing security solutions. We are not interested in this. so you will need to find a way to ignore this. 
* We want you to parse the data and reorganise it so that we have a json document with a single array containing technique objects, and then a sub array in each of these technique objects containing the adversaries who use this technique.
### Parsing and Transforming
Two main utility functions located in /utils/common.py were created :
* For parsing the json file ```load_create_df(path)```
The function loads JSON data from the specified file and processes it to create DataFrames for various object types. It extracts 'attack-pattern', 'malware', 'relationship', 'intrusion-set', and 'campaign' objects and stores them in separate DataFrames. These DataFrames are then saved as CSV files and returned as a tuple.


### The Data File After Transformation
* The tranformed json data file gets stored in /artifacts/data_transformation folder with the name "attack_pattern_to_adversery.json" .
* The entire project's folder structure is as follows:
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

* Once you have created your new json file, we would like you to create at least one chart showing the popularity of each technique, ie how many adversaries are using it. This should allow a non technical user to understand what the main threats are. 

## Challenge Submission

* You may use any tools you like, but you must do the work yourself.
* We expect this task to take about 3 hours, but feel free to spend whatever time you feel appropriate on it.
* We would like you to fork this repository and upload your solution to your forked repo. 
* Please add a readme of your own to the repo explaining how you completed the task (including tools and technology used), which parts were hardest/easiest, and how you would improve it/go further if you had more time.
* After you have finished your work, please make the repository public and email the url of the repo to louis.holt@esprofiler.com and marc.newton@esprofiler.com 
* The deadline for submissions is Wednesday 8th November at 5pm.





