# Sparkify Music Site Data Warehouse

## Content
- Summary
- Database Diagram
- Data File Descriptions
- Execution Instructions
- Cleanup
- References
    
## Summary

The purpose of this data warehouse is to provide a way for Sparkify analytics team to understand the songs and artists that their users are listening to.  Also, the database was design to answers regarding viability of the site and the type of customers listening to music on their site. For instance, are users willing to pay in order to play music on their Web site. Thus, the database was designed to enable the analytics team to quantify the songs being played for different dimensions such as time, artist and user’s demographics.  With the current database design, they will be able to answer questions like the ones below:

- What is the popularity of each song? 
- What is the popularity of each artist?
- What songs are paying users listening to?
- What is the percentage of users paying to listening music per month?
- What percent of paid users are male/female per month?
- Are more people paying for this service overtime?
- What is our average daily sales rate?

Hence, the database was design not just to answer their current questions, but their anticipated future questions.

## Database Diagram
The database consist of the five tables are depicted in the diagram below. A star schema was used to facilitate the running of the analytical queries. The fact table songplays and dimension tables can be join using the foreign keys: time.timestamp, users.user_id, artists.artist_id and songs.song_id.


![Database Design](file:///music_site_db_design.PNG)

The physical database design was done assuming the fact table songplays and dimension table time will be used daily to determine daily key performance metrics. The other dimension tables along with the fact table while used less frequently. Also, the fact table will be relatively larger than the dimension tables songs, artists and users, assuming the Sparkify music is very successful.

## Data File Descriptions

The song data files contains information about the songs and artists. Each file contains data for one song and a JSON format is used for the record layout. The song data files are store in sub-directories within the directory: s3://udacity-dend/song-data.

The application usage log files contains information about the users logon and songs played by the users. The song played records is filter out by specifying 'NextSong' for the page field. There is one file per day and a JSON format is used for the record layout. The song data files are store in sub-directories within the directory: s3://udacity-dend/log-data. 

Additionally, the record layout of the log files is stored in the file: s3://udacity-dend/log_json_path.json and is used while loading the data into the database.

## Execution Instructions

### IAM User Creation
Logon to your AWS account and execute the following instructions:

> From the IAM User Console, create an IAM user with the following policies: **AmazonS3ReadOnlyAccess** and **AmazonRedshiftFullAccess**

-  IAM Console > Add User
-  User Name: airflow_redshift
-  Access Type: **Programmatic access** -- select this option
  
> On the Set Permissions dialog page, select the option: **Attach existing policies**. Then search for and add the policies mentioned above.
  
> On the Add tags (optional) page -- you do not need to specify any tags.
  
> From Add User success page, save the **Access Key ID** and **Secret Access Key**. You will need them to create you Airflow AWS connection below.

#### IAM Redshift DB Role Creation
> Next use the IAM Console to create Redshift Role: **myRedshiftRole** and attach the following policies: **AmazonRedshiftFullAccess**, **AmazonS3ReadOnlyAccess** and **AmazonRedshiftQueryEditor**

#### Redshift DB Cluster Creation  
> From the Redshift dashboard, use the "Quick Launch Cluster" button to create Redshift DB Cluster with default settings and the role: **myRedshiftRole** created above. Record the following attributes of the cluster:
    
- Host: redshift-cluster-1.cqlqgt8pufyq.us-west-2.redshift.amazonaws.com
- Schema: dev -- Redshift DB name
- Login: awsuser -- Redshift Master User Name
- Password: <**password**> -- replace with your real Redshift user password
- Port: 5439

> You can select the "Clusters" option from the dashboard to see the status of the cluster. Also, you can refresh the page to see the updated status of the cluster.

### Redshift DB Tables Creation  
> Once the Redshift cluster is available, use the AWS Query Editor to create tables using DDLs mentioned below and located in the project workspace:
- /home/workspace/airflow/create_table.sql

### Running the ELT Using AirFlow DAG
#### Start Airflow Web UI
> Navigate to the project workspace and start Airflow Web UI by executing command:

- /opt/airflow/start.sh

#### Open Airflow UI  
> Once the above start script finish successfully, open Airflow UI by clicking tab: Access Workflow

#### Create Connection to Access AWS Resources
> From the Airflow UI, create airflow connection to access AWS resources: S3 and Redshift DB using key and secret from the dialog: Airflow > Admin > Connection > Create

- Conn Id: aws_credentials
- Conn Type: Amazon Web Services
- Login: <**Access Key ID**>
- Password: <**Secret Access Key**>

#### Create Redshift DB Connection   
> Create airflow connection to access Redshift DB from the dialog: Airflow > Admin > Connection > Create.

- Conn Id: redshift
- Conn Type: Postgres (Redshift and Postgres are compatible)
- Host: redshift-cluster-1.cqlqgt8pufyq.us-west-2.redshift.amazonaws.com
- Schema: dev -- Redshift DB
- Login: awsuser -- Redshift Master User Name
- Password: <**password**> -- replace with your real Redshift user password
- Port: 5439
 
#### Run DAG Tasks
> Turn on DAG schedule to run tasks.

> Turn off DAG schedule, once the tasks have run successfully.

## Cleanup
> From the Redshift dashboard delete the DB cluster: Clusters >  redshift-cluster-1 > Cluster > Delete.

## References
Apache Airflow Documentation:

https://airflow.apache.org/index.html

The Zen of Python and Apache Airflow:

https://blog.godatadriven.com/zen-of-python-and-apache-airflow

Python args and kwargs: Demystified:

https://realpython.com/python-kwargs-and-args

Jinja Templating:

https://airflow.readthedocs.io/en/stable/concepts.html

Airflow tutorial 7: Airflow variables:

https://www.applydatascience.com/airflow/airflow-variables/

Airflow Tutorial:

https://airflow.apache.org/docs/stable/tutorial.html

Python dict how to create key or append an element to key?

https://stackoverflow.com/questions/12905999/python-dict-how-to-create-key-or-append-an-element-to-key

Python Datetime:

https://www.programiz.com/python-programming/datetime

Rendering of inline images with relative paths is not working:

https://github.com/nea/MarkdownViewerPlusPlus/issues/23#issuecomment-287190881





