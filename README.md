# SQLAlchemy-Challenge
SQLAlchemy, Sqlite, and Flask API HI Climate Queries

Primary files: climate.ipynb (Jupyter Notebook) and app.py (Flask API)

## Climate analysis of the SQLite data using SQL Alchemy
* Precipation Measurements collected from the HI stations for the year period leading up to the latest measurement found in the data.

![Precipitation Tracking](https://github.com/pulliam-chris/SQLAlchemy-Challenge/blob/main/images/HI_Precipitation.PNG "Precipitation Tracking")

* Temperature frequencies collected from the most "active" station over the same year period as used in the precipitation tracking.

![Temperature Frequencies](https://github.com/pulliam-chris/SQLAlchemy-Challenge/blob/main/images/HI_Temp_Histogram.PNG "Temperature Frequencies")

## Creating a Flash API that produces JSON returns from provided routes

* Available Routes
![API Routes](https://github.com/pulliam-chris/SQLAlchemy-Challenge/blob/main/images/routes.PNG "API Routes")

  *  precipitation (returns all precipitation meaurements indexed by date collected)
  *  stations (returns all weather stations with associated measurements in the data)
  *  tobs (returns temperature information collected over the year leading up to the last measurement)
  *  tobs/start_date (returns [min, average, max] temperature information from the selected start_date onward)
  *  tobs/start_date/end_date (returns [min, average, max] temperature information within the selected date period)

### Example
* Query passing targeted dates.  
![API Query](https://github.com/pulliam-chris/SQLAlchemy-Challenge/blob/main/images/temps_query.PNG "API Query")

* JSON Return [min temperature, average temperature, max temperature] over targeted period.  
![JSON Return](https://github.com/pulliam-chris/SQLAlchemy-Challenge/blob/main/images/temps_return.PNG "JSON Return")
