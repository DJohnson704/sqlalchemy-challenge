# Import the dependencies.
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

app = Flask(__name__)

# Database Setup
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Home Route
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= (dt.datetime.now() - dt.timedelta(days=365))).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = {date: prcp for date, prcp in results}
    return jsonify(all_precipitations)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    all_stations = [station[0] for station in results]
    return jsonify(all_stations)

# TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    most_active_station = 'USC00519281'  # example, replace with your most active station
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= (dt.datetime.now() - dt.timedelta(days=365))).all()
    session.close()

    temps = {date: temp for date, temp in results}
    return jsonify(temps)

# Dynamic Route for temperature range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start, end=None):
    session = Session(engine)
    if not end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)




#################################################
# Flask Routes
#################################################
