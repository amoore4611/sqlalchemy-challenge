import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def percipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

  # Find the most recent date in the data set.
    recent_Date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    import datetime as dt

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)
    #print(year_ago)

    # Perform a query to retrieve the data and precipitation scores
    rain = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()

    session.close()
# Create a dictionary from the row data and append to a list of precip
    percip = []
    for date, prcp in rain:
        percip_dict = {}
        percip_dict["date"] = date
        percip_dict["prcp"] = prcp
        percip.append(percip_dict)

    return jsonify(percip)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

  # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    # Find the most recent date in the data set.
    recent_date=session.query(func.max(Measurement.date)).filter(Measurement.station == 'USC00519281').scalar()
    print(recent_date)

    import datetime as dt

    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017,8,18) - dt.timedelta(days = 365)
    #print(year_ago)

    # Perform a query to retrieve the precipitation 
    temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station =='USC00519281').\
    filter(Measurement.date > year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_temp = list(np.ravel(temp))

    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    from datetime import datetime
    date_object = datetime.strptime(start, "%Y-%m-%d")
    
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the maximum temperature for a given start or start-end range.   

    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
    # TMIN = session.query(Measurement.date, func.min(Measurement.tobs)).filter(Measurement.date >= date_object).all()
    TMIN = session.query(Measurement.tobs,).\
            filter(Measurement.date >= date_object).\
            order_by(Measurement.tobs).first()
    TMAX = session.query(Measurement.tobs).\
            filter(Measurement.date >= date_object).\
            order_by(Measurement.tobs.desc()).first()
    TAVG = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= date_object).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_TMIN = list(np.ravel(TMIN))
    all_TAVG = list(np.ravel(TAVG))
    all_TMAX = list(np.ravel(TMAX))

    return jsonify(all_TMIN + all_TAVG + all_TMAX)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine) 
    from datetime import datetime
    start_date_object = datetime.strptime(start, "%Y-%m-%d")
    end_date_object = datetime.strptime(end, "%Y-%m-%d")
    
    #Return a JSON list of the minimum temperature, the average temperature, 
    #and the maximum temperature for a given start or start-end range.   

    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for 
    # dates from the start date through the end date (inclusive).
    
    TMIN = session.query(Measurement.tobs,).\
            filter(Measurement.date >= start_date_object).\
            filter(Measurement.date <= end_date_object).\
            order_by(Measurement.tobs).first()
    TMAX = session.query(Measurement.tobs).\
            filter(Measurement.date >= start_date_object).\
            filter(Measurement.date <= end_date_object).\
            order_by(Measurement.tobs.desc()).first()
    TAVG = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date_object).\
            filter(Measurement.date <= end_date_object).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_TMIN = list(np.ravel(TMIN))
    all_TAVG = list(np.ravel(TAVG))
    all_TMAX = list(np.ravel(TMAX))

    return jsonify(all_TMIN + all_TAVG + all_TMAX)



if __name__ == '__main__':
    app.run(debug=True)
