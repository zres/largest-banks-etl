from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3

# Functions
def log_progress(log_file, message):
    '''Function to log progress in the file through 
        a timestamp and a message'''
    dt_now = datetime.now()
    date_format = '%Y-%m-%d %H:%M:%S'
    dt_now = dt_now.strftime(date_format)

    with open(log_file, 'a') as f:
        f.write(dt_now + ' : ' + message + '\n')

def extract(url, table_attribs):
    '''Function to extract the name and the revenue from the url'''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    df = pd.DataFrame(columns=table_attribs)
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            dict = {table_attribs[0]:cells[1].text.strip(),
                   table_attribs[1]:float(cells[2].text)}
            df1 = pd.DataFrame(data = dict, index = [0])
            df = pd.concat([df, df1], ignore_index=True)
    return df

def transform(df, exchange_rate_input):
    '''Convert USD values to EUR, GBP and INR'''
    exchange_rates = pd.read_csv(exchange_rate_input)
    for ex_rate in exchange_rates.iterrows():
        column_name = 'MC_'+ex_rate[1]['Currency']+'_Billion'
        df[column_name] = round(ex_rate[1]['Rate']*df['MC_USD_Billion'],2)
    return df

def load_to_csv(df, output_csv):
    df.to_csv(output_csv)

def load_to_db(df, connection, db_tablename):
    df.to_sql(db_tablename, connection, if_exists = 'replace')

def run_queries(query_string, conn):
    df_query = pd.read_sql(query_string, conn)
    print(df_query)

# Initialization
log_file = 'code_log.txt'
log_progress(log_file, "Start initialization")
url = "https://web.archive.org/web/20230908091635 /https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs_extract = ['Name', 'MC_USD_Billion']
table_attribs_final = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion',
                       'MC_EUR_Billion', 'MC_INR_Billion']
input_csv = 'exchange_rate.csv'
output_csv = 'Largest_banks_data.csv'
output_db = 'Banks.db'
db_tablename = 'Largest_banks'
log_progress(log_file, 'End initialization')

# Extract
log_progress(log_file, "Start extract")
df = extract(url, table_attribs_extract)
log_progress(log_file, "End extract")

# Transform
log_progress(log_file, "Start transformation")
df = transform(df,input_csv)
log_progress(log_file, "End transformation")

# Load
log_progress(log_file, "Start loading")
load_to_csv(df, output_csv)

with sqlite3.connect(output_db) as conn:
    load_to_db(df,conn, db_tablename)
log_progress(log_file, "End loading")

# Querying
log_progress(log_file, "Start querying")
with sqlite3.connect(output_db) as conn:
    run_queries("SELECT NAME, MC_USD_Billion FROM {table}"
                .format(table = db_tablename), conn)    
    run_queries("SELECT NAME, MC_GBP_Billion FROM {table}"
                .format(table = db_tablename), conn)    
    run_queries("SELECT NAME, MC_EUR_Billion FROM {table}"
                .format(table = db_tablename), conn)  
    run_queries("SELECT NAME, MC_INR_Billion FROM {table}"
                .format(table = db_tablename), conn)      
log_progress(log_file, "End querying")
