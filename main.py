# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:05:15 2019

@author: Eric Born
"""
from psycopg2 import connect, DatabaseError
from config import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd

#Reads the connection parameters from the database.ini file to be used in subsequent connections
params = config()

'''
Connects to the postgres server using a static connection string.
This needs to happen as the config parameters is using the beer database which hasnt been created yet.
Next the database database called beer is created.
Last it closes the cursor and the connection
'''
try:
    #Connects and creates the desired database
    conn = connect('dbname=postgres user=postgres password=1234')
    #I kept getting an error when attempting to create the database and found this statement as a remedy
    #Since creating a database cannot run into a transaction, since without a database you cannot have a transaction
    #setting the isolation level to automatically commit the command forces the server to create the database immediately
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    #conn.setAutoCommit(true)
    cur = conn.cursor()
    #cur.execute('SET AUTOCOMMIT = ON')
    cur.execute(
        '''
        CREATE DATABASE beer
        WITH 
        OWNER = "postgres"
        ENCODING = 'UTF8'
        CONNECTION LIMIT = -1;
        '''
    )
    cur.close()
    #conn.commit()
    conn.close()
except (Exception, DatabaseError) as dbError:
    print(dbError)

'''
Connects to postgres server on beer database using database.ini.
I studied the csv file by opening it in excel and using a dataframe to determine the column names and 
data types that should be used for each.
This section creates the table called reviews based on the column names and types found.
Finally it closes the cursor and the connection.
'''
try:
    # connect to the PostgreSQL server
    # **(Kwargs) used since there are multiple keyword arguments coming into the statement
    conn = connect(**params)
    #conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(
    '''
    CREATE TABLE reviews
    (
       Brewer_id INT
      ,brewer_name VARCHAR(100)
      ,review_time VARCHAR(100)
      ,review_overall FLOAT
      ,review_aroma FLOAT
      ,review_appearance FLOAT
      ,review_profilename VARCHAR(100)
      ,beer_style VARCHAR(100)
      ,review_palate FLOAT
      ,review_taste FLOAT
      ,beer_name VARCHAR(100)
      ,beer_abv FLOAT
      ,beer_beerid INT
    )
    ''')
    cur.close()
    conn.commit()
    conn.close()
except (Exception, DatabaseError) as tableError:
    print(tableError)
'''
I found that the csv contained cells that were not a number,
This was causing the write from the CSV to the database to fail.
I imported the CSV into a dataframe and used fillna(0) to fill in all cells that are not a number with a 0.
I then wrote the dataframe to a new file called beer_reviews_clean.csv 
skipping the index column that the dataframe created.
'''
try:
    #Use this to download the file striaght into a dataframe, make take awhile depending your on internet
    df = pd.read_csv('https://query.data.world/s/5t23kwu7xo2cpqqvmzeqon6un2mbqj')
    #uncomment if you have the file local
    #df = pd.read_csv('beer_reviews.csv')
    
    df.fillna(0)
    df.to_csv('beer_reviews_clean.csv', index=False)
except (IOError) as dfError:
    print(dfError)
    
'''
Lastly I reconnect to the posgres server on the beer database and use copy_expert to write the file into the 
database table created in the previous step
'''
try:
    # connect to the PostgreSQL server
    # ** Kwargs used since there are 4 parameters coming into the connect statement
    conn = connect(**params)
    cur = conn.cursor()
    copy_sql =  '''
                COPY reviews FROM stdin WITH CSV HEADER
                DELIMITER as ','
                '''
    with open('beer_reviews_clean.csv', 'r', encoding='utf-8') as f:
        cur.copy_expert(sql=copy_sql, file=f)
        cur.close()
        conn.commit()
    conn.close()
except (IOError) as writeError:
    print(writeError)
