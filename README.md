# DATA ENGINEER PYTHON TEST

*Created by Jelizaveta Malinina*

*5th of August 2020*
- - - -

This project reads data from ```data/csv/raw``` path, saves it to parquet. After that applies multiple transformations
and data quality validations before it saves the final results to parquet files partitioned by year-month-day.

As a result of this program it prints out the hottest day, the temperature on that day and the region where it happened.

E.g.
```
The hottest day between 2016-02-01 and 2016-03-31 is 2016-03-17
The temperature on this date was 15.8 degrees Celsius
It happened in Highland & Eilean Siar region
```

# Assumptions
* Hottest date is a date on which ScreenTemperature had it's maximum value
* What temperature on that date means what was the maximum temperature on the hottest date
* File names are of the following format ```weather.YYYYMM01.csv```
* All files contain the same set of columns:
```
['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection','WindSpeed',
'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
'SiteName', 'Latitude', 'Longitude', 'Region', 'Country']
```
* ObservationTime column contains a valid date
* ScreenTemperature column contains a valid temperature, in this project I assumed that any temperature between -50 and 50 degrees Celsius is valid

# Improvements
* I would use PySpark instead of Python for any project with big amount of data
* I would allow user an option to enter start date from which the program should run
* I would allow user an option to enter start date and end date between the program should run
* I would save partitioned data with overwrite mode
* I would store all parameters (like path for the raw data) in a configuration file