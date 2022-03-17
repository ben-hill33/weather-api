# Purpose: Build weather database from NOAA data

- Name: Ben Hill
- Date: 3/16/2022

See [noaa_sdk](https://pypi.org/project/noaa-sdk/) for details on package used

## Code used

```python
from noaa_sdk import noaa
import sqlite3
import datetime
```

### Parameters for retrieving NOAA weather data

```python
zipCode = "90808"  # change to your postal code
country = "US" 
# date-time format is yyyy-mm-ddThh:mm:ssZ, times are Zulu time (GMT)
# gets the most recent 14 days of data
today = datetime.datetime.now()
past = today - datetime.timedelta(days=14)
startDate = past.strftime("%Y-%m-%dT00:00:00Z") 
endDate = today.strftime("%Y-%m-%dT23:59:59Z")
```

### Create connection - If database does not exist

```python
print("Preparing database...")
dbFile = "weather.db"
conn = sqlite3.connect(dbFile)
```

### Create cursor to execute SQL commands

```python
cur = conn.cursor()
```

### Drop previous version of table if any so we start fresh each time

```python
dropTableCmd = "DROP TABLE IF EXISTS observations;"
cur.execute(dropTableCmd)
```

### Create new table to store observations

```python
createTableCmd = """ CREATE TABLE IF NOT EXISTS observations ( 
                        timestamp TEXT NOT NULL PRIMARY KEY, 
                        windSpeed REAL,
                        temperature REAL,
                        relativeHumidity REAL,
                        windDirection INTEGER,
                        barometricPressure INTEGER,
                        visibility INTEGER,
                        textDescription TEXT
                     ) ; """

cur.execute(createTableCmd)
print("Database prepared")
```

### Get hourly weather observations from NOAA Weather Service API

```python
print("Getting weather data...")
n = noaa.NOAA()
observations =  n.get_observations(zipCode,country,startDate,endDate)
```

### Populate table with weather observations

```python
print("Inserting rows...")
insertCmd = """ INSERT INTO observations 
                    (timestamp, windSpeed, temperature, relativeHumidity, 
                     windDirection, barometricPressure, visibility, textDescription)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?) """
count = 0
for obs in observations:
    insertValues = (obs["timestamp"],
                    obs["windSpeed"]["value"],
                    obs["temperature"]["value"],
                    obs["relativeHumidity"]["value"],
                    obs["windDirection"]["value"],
                    obs["barometricPressure"]["value"],
                    obs["visibility"]["value"],
                    obs["textDescription"])
    cur.execute(insertCmd, insertValues)
    count += 1
if count > 0:
    cur.execute("COMMIT;")
print(count, "rows inserted")
print("Database load complete!")
```
