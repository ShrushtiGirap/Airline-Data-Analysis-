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

# Data Exploration

aircrafts_data = pd.read_sql_query("Select * from aircrafts_data", connection)
aircrafts_data

airports_data = pd.read_sql_query("Select * from airports_data", connection)
airports_data.head()

boarding_passes = pd.read_sql_query("Select * from boarding_passes", connection)
boarding_passes.head()

bookings = pd.read_sql_query("Select * from bookings", connection)
bookings.head()

flights = pd.read_sql_query("Select * from flights", connection)
flights.head()

seats = pd.read_sql_query("Select * from seats", connection)
seats.head()

ticket_flights = pd.read_sql_query("Select * from ticket_flights", connection)
ticket_flights.head()

tickets = pd.read_sql_query("Select * from tickets", connection)
tickets.head()

for table in table_list:
    print('\ntable',table)
    column_info=connection.execute("Pragma table_info({})".format(table))
    for column in column_info.fetchall():
        print(column)

for table in table_list:
    print('\ntable',table)
    df_table = pd.read_sql_query(f"select * from {table}",connection)
    print(df_table.isnull().sum())

# Basic Analysis

# How many planes have more than 100 seats?

pd.read_sql_query("""select aircraft_code, count(*) as num_seats from seats group by aircraft_code having num_seats>100""", connection)

# How the number of tickets booked and total amount earned changed with time.

tickets = pd.read_sql_query("""Select * from tickets inner join bookings on tickets.book_ref=bookings.book_ref""", connection)
tickets['book_date']= pd.to_datetime(tickets['book_date'])
tickets['date']=tickets['book_date'].dt.date
tickets

x=tickets.groupby('date')[['date']].count()
plt.figure(figsize=(18,6))
plt.plot(x.index,x['date'],marker='^')
plt.xlabel('Date', fontsize=20)
plt.ylabel('Number of tickets', fontsize=20)
plt.grid('b')
plt.show()

bookings = pd.read_sql_query("Select * from bookings",connection)
bookings['book_date'] = pd.to_datetime(bookings['book_date'])
bookings['date']= bookings['book_date'].dt.date
x=bookings.groupby('date')[['total_amount']].sum()
plt.figure(figsize=(18,6))
plt.plot(x.index,x['total_amount'],marker='^')
plt.xlabel('Date', fontsize=20)
plt.ylabel('Total ammount earned', fontsize=20)
plt.grid('b')
plt.show()

bookings.groupby('date')[['total_amount']].sum()

# Calculate the average charges for each aircraft with different fare conditions.

df=pd.read_sql_query("""select fare_conditions, aircraft_code,avg(amount) from ticket_flights join flights on ticket_flights.flight_id=flights.flight_id group by aircraft_code,fare_conditions""",connection)
df

sns.barplot(data=df,x='aircraft_code', y='avg(amount)',hue='fare_conditions')

#Analyzing occupancy rate

#For each aircraft, calculate the total revenue per year and the average revenue per ticket

pd.read_sql_query("""select aircraft_code,ticket_count, total_revenue,total_revenue/ticket_count as avg_revenue_per_ticket from (select aircraft_code, count(*) as ticket_count, sum(amount) as total_revenue from ticket_flights join flights on ticket_flights.flight_id = flights.flight_id group by aircraft_code)""", connection)

#calculate the average occupancy per aircraft

pd.read_sql_query("""select a.aircraft_code, avg(a.seats_count) as booked_seats, b.num_seats, avg(a.seats_count)/b.num_seats as occupancy_rate from(select aircraft_code, flights.flight_id, count(*) as seats_count from boarding_passes inner join flights on boarding_passes.flight_id=flights.flight_id group by aircraft_code, flights.flight_id) as a inner join (select aircraft_code, count(*) as num_seats from seats group by aircraft_code) as b on a.aircraft_code = b.aircraft_code group by a.aircraft_code""", connection)

#calculate by how much the total annual turnover could increase by giving all aicraft a 10% higher occupancy rate.

occupancy_rate['Inc occupancy rate'] = occupancy_rate['occupancy_rate']+occupancy_rate['occupancy_rate']*0.1
occupancy_rate


