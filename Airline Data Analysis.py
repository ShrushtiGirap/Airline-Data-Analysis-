import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Database Connection

connection = sqlite3.connect('travel.sqlite')
cursor = connection.cursor()

cursor.execute("""select name from sqlite_master where type ='table';""")
print('List of tables present in the database')
table_list = [table[0] for table in cursor.fetchall()]
table_list
>List of tables present in the database

['aircrafts_data',
 'airports_data',
 'boarding_passes',
 'bookings',
 'flights',
 'seats',
 'ticket_flights',
 'tickets']
