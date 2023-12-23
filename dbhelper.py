import mysql.connector
import pandas as pd

df = pd.read_excel("Test Data Set + Requirements.xlsx", sheet_name="Data")
df.date = df.date.astype("str")
# Adjust column names in the DataFrame to match your SQL table
df.columns = ['index_', 'date', 'open', 'high', 'low', 'close', 'volume', 'oi', 'strike', 'type']

# create database
mydb = mysql.connector.connect(host='localhost', user='root', password='123456')
print(mydb.connection_id)

cur = mydb.cursor()
cur.execute("CREATE DATABASE stocks")
mydb.commit()

#create table
mydb = mysql.connector.connect(host='localhost', user='root', password='123456',database="stocks")
print(mydb.connection_id)

cur = mydb.cursor()

query = """create table banknifty(
id integer NOT NULL PRIMARY KEY AUTO_INCREMENT,
index_ integer,
date datetime,
open integer,
high integer,
low integer,
close integer,
volume integer,
oi integer,
strike integer,
type varchar(255)
)"""

cur.execute(query)
mydb.commit()


query = """
        INSERT INTO banknifty 
        (index_, date, open, high, low, close, volume, oi, strike, type)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

# Convert DataFrame to a list of tuples
val = df.to_records(index=None).tolist()

cur.executemany(query, val)  # Use executemany for multiple rows
mydb.commit()
