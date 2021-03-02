import numpy as np
import datetime as dt

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
        f"<a href='/api/v1.0/tobs/start_date'>tobs_after_date</a><br/>"
        #f"<a href='/api/v1.0/<start_date>/<end_date>'>tobs_between_dates</a><br/>"
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
    endDate = endDate[0]
    endDate = dt.date.fromisoformat(endDate)
    startDate = endDate - dt.timedelta(days=365)
    #print(f'{startDate}')

    # Query temp measurements from that station)
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
    results = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date >= start_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_results = list(np.ravel(results))

    return jsonify(all_results)

#return jsonify({"error": f"TOBS Measurements in provided range not found. Please use date format YYYY-DD-MM"}), 404

if __name__ == '__main__':
    app.run(debug=True)
