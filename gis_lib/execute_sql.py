from gis_lib.helpers import deleteFolder, get_last_monday
import pandas as pd
import cx_Oracle
from dotenv import load_dotenv 
import os


# use env credentials to establish a connection with the Oracle db, and return the connection object
def oracle_connect():
    
    # get credentials from the .env file
    load_dotenv()
    oracle_user = os.getenv('oracle_user')
    oracle_password = os.getenv('oracle_password')
    oracle_server_name = os.getenv('oracle_server_name')
    oracle_instant_client_path = os.getenv('oracle_instant_client_path')

    # establish a connection with the Oracle database
    try:     cx_Oracle.init_oracle_client(lib_dir = oracle_instant_client_path)
    except:  pass   
    
    # return connection object 
    return cx_Oracle.connect(oracle_user, oracle_password, oracle_server_name)


# Runs the sql query provided in the input filepath sql_query, and
# returns a data frame with the output data 
def run_SQL(sql_query):
    #sql_name = sql_query.replace('.sql','') # just the name of the sql file
    
    # establish a connection with FXPROD
    con = oracle_connect()

    # run the query, store in a data frame
    sql_statement = open(sql_query, 'r').read()
    df = pd.read_sql(sql_statement, con)

    con.close()

    return df


# run each of the SQL queries, storing the output in the csv location specified by the config 
def create_csv_data():

    # identify the location for this week's system data to go
    csv_dir = os.path.join(os.getenv('SQL_EXPORTS'), get_last_monday())

    # clear out any existing folder and create a new folder in SQL Exports for the current week's data
    deleteFolder(csv_dir)
    os.mkdir(csv_dir)

    # iterate through each sql file in the sql folder,
    sql_folder = os.path.join(os.getcwd(),'sql')
    for file in os.listdir(sql_folder):

        # identfy the sql file being ur\\run, and run it
        sql_name = file.replace('.sql','') # just the name of the sql file
        print('running sql:', sql_name,'\n')
        df = run_SQL(os.path.join(sql_folder, file))
        print('finished running ', sql_name)

        # format columns lowercase and export csv to the export location
        df.columns = [x.lower() for x in df.columns]
        export_loc = os.path.join(csv_dir, f'{sql_name}{get_last_monday()}.csv')
        print('exporting to ', export_loc,'\n')
        df.to_csv(export_loc, index = False) # TODO: column names from all caps to the appropriate names

