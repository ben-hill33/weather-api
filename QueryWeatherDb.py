# Purpose: Query database using SQL
# Name: Ben Hill
# Date: 3/21/22
# Run BuildWeatherDB.py to build weather database before running this program

import sqlite3
import pandas as pd

dbFile = "weather.db"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

conn = sqlite3.connect(dbFile)
# selectAll = " SELECT * FROM observations ORDER BY timestamp; "
# resultAll = pd.read_sql_query(selectAll, conn)
# print(resultAll)

# selectMinMax = " SELECT MIN(temperature), MAX(temperature) FROM observations; "
# resultMinMax = pd.read_sql_query(selectMinMax, conn)
# print(resultMinMax)

selectTempWindText = " SELECT timestamp, temperature, windspeed, textDescription FROM observations where textDescription = 'Clear'; "
resultTempWindText = pd.read_sql_query(selectTempWindText, conn)
print(resultTempWindText)

