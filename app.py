import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurements = Base.classes.measurement
Stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/tobs/start_date'>tobs/start_date</a><br/>"
        f"<a href='/api/v1.0/tobs/start_date/end_date'>tobs/start_date/end_date</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation measurements
    results = session.query(Measurements.date, Measurements.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all weather stations
    results = session.query(func.distinct(Measurements.station)).order_by(Measurements.station).all()
  
    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most active station
    measurementCount = session.query(Measurements.station).filter(Measurements.station == Stations.station).group_by(Stations.name).order_by(func.count(Measurements.station).desc()).first()
    mostActive = np.ravel(measurementCount)
    mostActive = mostActive[0]

    # Find the date range for that station
    lastMeasurement = session.query(Measurements.date).filter(Measurements.station == mostActive).order_by(Measurements.date.desc()).first()
    endDate = np.ravel(lastMeasurement)
    # Unrap list and convert to datetime
    endDate = endDate[0]
    endDate = dt.date.fromisoformat(endDate)
    startDate = endDate - dt.timedelta(days=365)

    # Query temp measurements from that station
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.station == mostActive).filter(Measurements.date >= startDate).all()
  
    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

@app.route("/api/v1.0/tobs/<start_date>")
def tobs_after_date(start_date):

    # Convert passed date to datetime
    start_date = dt.date.fromisoformat(start_date) 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp measurements after provided date
    tempCalcs = session.query(Measurements.tobs).filter(Measurements.date >= start_date).all()
    
    session.close()

    tempCalcs = list(np.ravel(tempCalcs))
    if len(tempCalcs) == 0:
        return jsonify({"error": f"TOBS Measurements in provided range not found. Please use date format YYYY-DD-MM"}), 404

    # Calculations based on query
    lowTemp = int(min(tempCalcs))
    highTemp = int(max(tempCalcs))
    allTemps = pd.Series(tempCalcs,dtype='int32')
    avgTemp = round(allTemps.mean(),2) 

    # Convert caculations into a list
    all_results = [lowTemp, avgTemp, highTemp]

    return jsonify(all_results)

@app.route("/api/v1.0/tobs/<start_date>/<end_date>")
def tobs_between_dates(start_date,end_date):

    # Convert passed date to datetime
    start_date = dt.date.fromisoformat(start_date)
    end_date = dt.date.fromisoformat(end_date) 

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp measurements after provided date
    tempCalcs = session.query(Measurements.tobs).filter(Measurements.date >= start_date).filter(Measurements.date <= end_date).all()
    
    session.close()

    tempCalcs = list(np.ravel(tempCalcs))
    if len(tempCalcs) == 0:
        return jsonify({"error": f"TOBS Measurements in provided range not found. Please use date format YYYY-DD-MM"}), 404

    lowTemp = int(min(tempCalcs))
    highTemp = int(max(tempCalcs))
    allTemps = pd.Series(tempCalcs,dtype='int32')
    avgTemp = round(allTemps.mean(),2) 

    # Convert caculations into a list
    all_results = [lowTemp, avgTemp, highTemp]

    return jsonify(all_results)


if __name__ == '__main__':
    app.run(debug=True)
