from .db import get_db
#TODO: Add models here lol

def get_all_spaceports():
    """All space ports so the menue can dropdown."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM Spaceports ORDER BY name ASC")
    spaceports = cursor.fetchall()
    return spaceports

def get_all_planets():
    """All planets for dropdown menus."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM Planets ORDER BY name ASC")
    planets = cursor.fetchall()
    return planets

def get_all_routes():
    """All routes with origin and destination names."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id, s1.name as origin_name, s2.name as destination_name 
        FROM Routes r
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        ORDER BY s1.name, s2.name
    """)
    routes = cursor.fetchall()
    return routes

def get_all_spacecraft():
    """All spacecraft types for dropdown menus."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, type_name, capacity FROM Spacecraft ORDER BY type_name ASC")
    spacecraft = cursor.fetchall()
    return spacecraft

def get_all_space_stations():
    """All space stations for dropdown menus."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM SpaceStations ORDER BY name ASC")
    stations = cursor.fetchall()
    return stations

def get_spaceport_flights(spaceport_id, day_of_week=None):
    """Get all flights (arrivals and departures) for a specific spaceport."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    base_query = """
        SELECT 
            f.flight_number,
            'Departure' as flight_type,
            CONCAT(s1.name, ' → ', s2.name) as route,
            f.departure_time,
            fs.day_of_week
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
        WHERE r.origin_spaceport_id = %s
        
        UNION ALL
        
        SELECT 
            f.flight_number,
            'Arrival' as flight_type,
            CONCAT(s1.name, ' → ', s2.name) as route,
            f.departure_time,
            fs.day_of_week
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
        WHERE r.destination_spaceport_id = %s
    """
    
    if day_of_week:
        # Add WHERE clause for day filter to both parts of UNION
        query_with_filter = base_query.replace("WHERE r.origin_spaceport_id = %s", "WHERE r.origin_spaceport_id = %s AND fs.day_of_week = %s")
        query_with_filter = query_with_filter.replace("WHERE r.destination_spaceport_id = %s", "WHERE r.destination_spaceport_id = %s AND fs.day_of_week = %s")
        query = query_with_filter + " ORDER BY day_of_week, departure_time"
        cursor.execute(query, (spaceport_id, day_of_week, spaceport_id, day_of_week))
    else:
        query = base_query + " ORDER BY day_of_week, departure_time"
        cursor.execute(query, (spaceport_id, spaceport_id))
    
    return cursor.fetchall()

def get_dashboard_data():
    """Get dashboard data for homepage including upcoming flight schedules."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    dashboard = {}
    
    # Get upcoming flights (next few flights regardless of day)
    cursor.execute("""
        SELECT 
            f.flight_number,
            s1.name as origin,
            s2.name as destination,
            f.departure_time,
            sc.type_name as aircraft,
            sc.capacity,
            fs.day_of_week
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        JOIN Spacecraft sc ON f.spacecraft_id = sc.id
        JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
        ORDER BY 
            CASE fs.day_of_week
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
            END,
            f.departure_time
        LIMIT 15
    """)
    dashboard['upcoming_flights'] = cursor.fetchall()
    
    return dashboard

def get_all_data():
    """Get all data from all tables for the comprehensive view."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    data = {}
    
    # Get all planets
    cursor.execute("SELECT * FROM Planets ORDER BY name")
    data['planets'] = cursor.fetchall()
    
    # Get all space stations with planet names
    cursor.execute("""
        SELECT ss.*, 
               p1.name as orbiting_planet_name,
               p2.name as owner_planet_name
        FROM SpaceStations ss
        LEFT JOIN Planets p1 ON ss.orbiting_planet_id = p1.id
        LEFT JOIN Planets p2 ON ss.owner_planet_id = p2.id
        ORDER BY ss.name
    """)
    data['space_stations'] = cursor.fetchall()
    
    # Get all spaceports with location info
    cursor.execute("""
        SELECT sp.*,
               p.name as planet_name,
               ss.name as station_name
        FROM Spaceports sp
        LEFT JOIN Planets p ON sp.planet_id = p.id
        LEFT JOIN SpaceStations ss ON sp.station_id = ss.id
        ORDER BY sp.name
    """)
    data['spaceports'] = cursor.fetchall()
    
    # Get all spacecraft
    cursor.execute("SELECT * FROM Spacecraft ORDER BY type_name")
    data['spacecraft'] = cursor.fetchall()
    
    # Get all routes with spaceport names
    cursor.execute("""
        SELECT r.*,
               s1.name as origin_name,
               s2.name as destination_name
        FROM Routes r
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        ORDER BY s1.name, s2.name
    """)
    data['routes'] = cursor.fetchall()
    
    # Get all flights with detailed info
    cursor.execute("""
        SELECT f.*,
               s1.name as origin_name,
               s2.name as destination_name,
               sc.type_name as spacecraft_type,
               GROUP_CONCAT(fs.day_of_week ORDER BY fs.day_of_week) as schedule_days
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
        JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
        JOIN Spacecraft sc ON f.spacecraft_id = sc.id
        LEFT JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
        GROUP BY f.flight_number
        ORDER BY f.flight_number
    """)
    data['flights'] = cursor.fetchall()
    
    return data

def find_flights_on_route(origin_id, destination_id):
    """
    find the flights and the details about those flights on the route.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Joins to get details for each flight including schedule information
    query = """
        SELECT
            f.flight_number,
            f.departure_time,
            f.flight_time_hours AS flight_time,
            sc.type_name AS spacecraft_type,
            sc.capacity AS spacecraft_capacity,
            r.distance,
            GROUP_CONCAT(fs.day_of_week ORDER BY 
                CASE fs.day_of_week
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    WHEN 'Sunday' THEN 7
                END
            ) AS departs_on_day
        FROM Flights f
        JOIN Routes r ON f.route_id = r.id
        JOIN Spacecraft sc ON f.spacecraft_id = sc.id
        LEFT JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
        WHERE r.origin_spaceport_id = %s AND r.destination_spaceport_id = %s
        GROUP BY f.flight_number, f.departure_time, f.flight_time_hours, sc.type_name, sc.capacity, r.distance
    """
    cursor.execute(query, (origin_id, destination_id))
    flights = cursor.fetchall()
    return flights

def get_spaceport_id_by_name(name):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id FROM Spaceports WHERE name = %s",
            (name,)
        )
        row = cursor.fetchone()
    except Exception:
        print(f"get_spaceport_id_by_name,{name} Query Failed")
        return None
    return row['id'] if row else None


def get_routes_from_spaceport(spaceport_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT r.id, s2.name as destination_name, r.destination_spaceport_id "
            "FROM Routes r "
            "JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id "
            "WHERE r.origin_spaceport_id = %s",
            (spaceport_id,)
        )
        rows = cursor.fetchall()
    except Exception:
        print(f"get_routes_from_spaceport,{spaceport_id} Query Failed")
        return []
    return rows


def get_flights_for_route_on_day(route_id, day_of_week):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT f.flight_number "
            "FROM Flights f "
            "JOIN FlightSchedules fs ON f.flight_number = fs.flight_number "
            "WHERE f.route_id = %s AND fs.day_of_week = %s",
            (route_id, day_of_week)
        )
        rows = cursor.fetchall()
    except Exception:
        print(f"get_flights_for_route_on_day,{route_id},{day_of_week} Query Failed")
        return []
    return rows

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