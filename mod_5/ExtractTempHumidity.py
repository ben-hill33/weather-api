# Purpose: Extract temperature, humidity data from weather database into CSV file
# Name: Ben Hill
# Date: 4/2/2022
# Run BuildWeatherDB.py to build weather database before running this program


import sqlite3

def convert_celsius_to_fahrenheit(c_temp):
    return (c_temp*9.0/5.0) + 32.0


# file names for database and output file
db_file = "weather.db"
output_file_name = "formatdata.csv"

# connect to and query weather db
db_connect = sqlite3.connect(db_file)

# create cursor to execute SQL commands
sql_cursor = db_connect.cursor()
select_cmd = """ SELECT temperature, relativeHumidity FROM observations
                ORDER BY timestamp; """
sql_cursor.execute(select_cmd)
all_rows = sql_cursor.fetchall()

# limit the number of rows output to half
row_count = len(all_rows)//2
rows = all_rows

# write data to output file
with open(output_file_name, "w+") as outf:
    outf.write("Celsius, Fahrenheit, Humidity")
    outf.write("\n")
    for row in rows:
        c_temp = row[0]
        if c_temp is None:
            outf.write(",,")
        else:
            f_temp = convert_celsius_to_fahrenheit(c_temp)
            outf.write(str(c_temp) + ",")
            outf.write(str(f_temp) + ",")

        humidity = row[1]
        if humidity is None:
            outf.write("\n")
        else:
            outf.write(str(humidity) + "\n")