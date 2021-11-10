#sparkify_elt_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)

from helpers import SqlQueries


default_args = {
    'owner': 'Sparkify',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 30, 22, 59, 59, 000000),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

"""
# test defsult arguments
default_args = {
    'owner': 'Sparkify',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 30, 22, 59, 59, 000000),
    'end_date': datetime(2018, 12, 1, 0, 0,1, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    #'max_active_runs':1
}
"""

dag = DAG('Udacity',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval="@hourly",
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table='staging_events',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    region="us-west-2",
    s3_bucket="udacity-dend/log_data",
    s3_key="{execution_date.year}/{execution_date.month}",
    json_format="udacity-dend/log_json_path.json"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table='staging_songs',
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    region="us-west-2",
    s3_bucket="udacity-dend/song_data",
    s3_key="",
    json_format="auto",
)

load_songplays_fct_tbl = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    del_tbl_data_ind=False,
    table="songplays",
    redshift_conn_id="redshift",
    insert_sql_stmnt = SqlQueries.songplay_table_insert 
)

load_user_dim_tbl = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    del_tbl_data_ind=True,
    table="users",
    redshift_conn_id="redshift",
    insert_sql_stmnt = SqlQueries.user_table_insert
)

load_song_dim_tbl = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    del_tbl_data_ind = True,
    table = "songs",
    redshift_conn_id = "redshift",
    insert_sql_stmnt = SqlQueries.song_table_insert
)


load_artist_dim_tbl = LoadDimensionOperator(
    task_id = 'Load_artist_dim_table',
    dag = dag,
    del_tbl_data_ind = True,
    table = "artists",
    redshift_conn_id = "redshift",
    insert_sql_stmnt = SqlQueries.artist_table_insert
)

load_time_dim_tbl = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    del_tbl_data_ind = True,
    table = "time",
    redshift_conn_id = "redshift",
    insert_sql_stmnt = SqlQueries.time_table_insert
)

sel_fct_join_dim_queries = {'songplay_join_song': SqlQueries.songplay_join_song_cnt
                            , 'songplay_join_artist': SqlQueries.songplay_join_artist_cnt
                            , 'songplay_join_user': SqlQueries.songplay_join_user_cnt
                            , 'songplay_join_time': SqlQueries.songplay_join_time_cnt}
                            
run_quality_check = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id = "redshift",
    data_quality_queries = sel_fct_join_dim_queries
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# implement task dependency
start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_fct_tbl
load_songplays_fct_tbl >> load_user_dim_tbl
load_songplays_fct_tbl >> load_song_dim_tbl
load_songplays_fct_tbl >> load_artist_dim_tbl
load_songplays_fct_tbl >> load_time_dim_tbl
[load_user_dim_tbl, load_song_dim_tbl, load_artist_dim_tbl, load_time_dim_tbl] >> run_quality_check
run_quality_check >> end_operator