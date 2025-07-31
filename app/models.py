from .db import get_db
#TODO: Add models here lol

def get_all_spaceports():
    """All space ports so the menue can dropdown."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM Spaceports ORDER BY name ASC")
    spaceports = cursor.fetchall()
    return spaceports

def find_flights_on_route(origin_id, destination_id):
    """
    find the flights and the details about those flights on the rotue on.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Joins to get details for each flight
    query = """
        SELECT
            f.flight_number,
            f.departure_time,
            f.flight_time_hours,
            sc.type_name AS spacecraft_type,
            sc.capacity AS spacecraft_capacity,
            r.distance
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spacecraft sc ON f.spacecraft_id = sc.id
        WHERE r.origin_spaceport_id = %s AND r.destination_spaceport_id = %s
    """
    cursor.execute(query, (origin_id, destination_id))
    flights = cursor.fetchall()
    return flights

def spaceport_arrivals_departures_query(spaceport_name):
    # given a spaceport, list all arrivals and departures at that spaceport

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """SELECT origin_spaceport_id, 'Departure' AS route_type
            FROM Routes
            WHERE origin_spaceport_id = %s
            
            UNION

            SELECT destination_spaceport_id, 'Arrival' AS route_type
            FROM Routes
            WHERE destination_spaceport_id = %s"""
    
    cursor.execute(query, (spaceport_name, spaceport_name))
    
    arrivals_departures = cursor.fetchall()

    return arrivals_departures


def date_and_spaceport_arrivals_departures_query(day_of_week, spaceport_name):
    # given a date and spaceport, list all departures in order, all arrivals in order, and all flight details

    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """SELECT *, 'Departure' AS flight_type
            FROM Flights
            WHERE route_id IN 
                (SELECT id
                 FROM Routes
                 WHERE origin_spaceport_id = %s)
            AND flight_number IN
                (SELECT flight_number
                 FROM FlightSchedules
                 WHERE date = %s)
            
            UNION

            SELECT *, 'Arrival' AS flight_type
            FROM Flights
            WHERE route_id IN 
                (SELECT id
                 FROM Routes
                 WHERE destination_spaceport_id = %s)
            AND flight_number IN
                (SELECT flight_number
                 FROM FlightSchedules
                 WHERE date = %s)

            ORDER BY departure_time ASC"""
    
    cursor.execute(query, (spaceport_name, day_of_week, spaceport_name, day_of_week))
    
    date_arrivals_departures = cursor.fetchall()

    return date_arrivals_departures