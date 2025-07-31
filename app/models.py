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
