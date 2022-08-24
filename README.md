# sqlalchemy-challenge
This challenge was broken down into three parts. Before beginning data analysis, the following was accomplished.

1. Used SQLAlchemy to create_engine to connect to your SQLite database.
2. Used SQLAlchemy’s automap_base() to reflect the tables from the SQLite file (Hawaii.sqlite) into classes and save a reference to those classes called Station and Measurement.
3. Link Python to the database by creating a SQLAlchemy session.

Part 1: Percipitation Analysis
In the first part, the amount of rainfall in Hawaii over the past year was analyzed. To do this, the most recent date was determined using the orderby function. Then, the data for the past year was queried by using dt.timedelta to subtract 365 days from the most recent date. Once the data was queried, it was put into a dataframe. Using this dataframe, a bar plot was made of the rainfall vs date. Finally, the summary statistics was calculated for the dataframe using df.describe().

Part 2: Station Analysis 

In this section, an analysis of the stations in the area was performed. In order to do this, the number of stations in Hawaii was determined using func.count. Next, the most active station was determined by querying all stations and performing a func.count on each station to see how many times it was listed. Once the most active station was determined, the min, max, and avg temperature for that station was determined by filtering all temperature data for the most active station. Once completed, the data was queried for temperature in the same way as we did for rainfall over the most recent year. With this data, a histogram was made of the temperature vs date. Once this was completed, the session was closed.

Part 3: Design Climate App
Using the analyzed data from Parts 1-2, a flask API was designed. The following was required for the flask API:
Use Flask to create your routes, as follows:


1. Homepage--List all available routes. 

2. /api/v1.0/precipitation--Convert the query results to a dictionary using date as the key and prcp as the value. Return the JSON representation of your dictionary.

3. /api/v1.0/stations--Return a JSON list of stations from the dataset.

4. /api/v1.0/tobs--Query the dates and temperature observations of the most active station for the previous year of data. Return a JSON list of temperature observations (TOBS) for the previous year.

5./api/v1.0/<start> -- Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range. When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.


6. /api/v1.0/<start>/<end>-- Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range. When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

