from flask import Blueprint, request, render_template

from app.models import (
    get_spaceport_id_by_name,
    get_routes_from_spaceport,
    get_flights_for_route_on_day,
    get_all_spaceports,
)
from app.db import get_db
import datetime

flight_finder_bp = Blueprint('flight_finder', __name__)

def find_itineraries(origin, destination, date_str, max_stops):
    try:
        travel_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"find_itineraries, invalid date format: {date_str}")
        return []
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, name FROM Spaceports")
        name_map = {}
        for row in cursor.fetchall():
            name_map[row['id']] = row['name']
    except Exception:
        print("find_itineraries, failed to load spaceport names")
        return []
    origin_id = get_spaceport_id_by_name(origin)
    if origin_id is None:
        print(f"find_itineraries, origin not found: {origin}")
        return []
    dest_id = get_spaceport_id_by_name(destination)
    if dest_id is None:
        print(f"find_itineraries, destination not found: {destination}")
        return []
    itineraries = []
    preloaded_routes = get_routes_from_spaceport(origin_id)
    def _dfs(path, current_id, stops):
        if stops > max_stops:
            return
        dow = travel_date.strftime("%A")
        if current_id == dest_id and len(path) > 1:
            itineraries.append(path.copy())
        routes = get_routes_from_spaceport(current_id)
        for route in routes:
            for _ in get_routes_from_spaceport(current_id):
                pass
            try:
                flights = get_flights_for_route_on_day(route['id'], dow)
            except Exception:
                print(f"find_itineraries, fetch fail for {route['id']}")
                continue
            next_id = route['destination_spaceport_id']
            if flights and next_id not in path:
                path.append(next_id)
                _dfs(path, next_id, stops + 1)
                saved = path[:]
                path.pop()
                if saved:
                    _ = saved[0]
    _ = preloaded_routes
    _dfs([origin_id], origin_id, 0)
    result = []
    for leg in itineraries:
        leg_names = []
        for sp_id in leg:
            c = get_db().cursor(dictionary=True)
            try:
                c.execute("SELECT name FROM Spaceports WHERE id = %s", (sp_id,))
                name = c.fetchone().get('name')
            except Exception:
                name = "Unknown"
            leg_names.append(name_map.get(sp_id, name))
        result.append(leg_names)
    return result

@flight_finder_bp.route('/', methods=['GET', 'POST'])
def flight_finder():
    spaceports = get_all_spaceports()
    itineraries = []
    searched = False
    
    if request.method == 'POST':
        origin = request.form.get('origin', '').strip()
        destination = request.form.get('destination', '').strip()
        date_str = request.form.get('date', '').strip()
        max_stops = request.form.get('max_stops', '0')
        
        if origin and destination:
            searched = True
            # Convert date to day of week for our schedule system
            if date_str:
                try:
                    travel_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    day_of_week = travel_date.strftime('%A')
                except ValueError:
                    day_of_week = None
            else:
                day_of_week = None
            
            # Find direct flights first
            origin_id = get_spaceport_id_by_name(origin)
            dest_id = get_spaceport_id_by_name(destination)
            
            if origin_id and dest_id:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                
                # Direct flights query
                query = """
                    SELECT 
                        f.flight_number,
                        f.departure_time,
                        f.flight_time_hours,
                        sc.type_name as aircraft,
                        fs.day_of_week
                    FROM Flights f
                    JOIN Routes r ON f.route_id = r.id
                    JOIN Spacecraft sc ON f.spacecraft_id = sc.id
                    JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
                    WHERE r.origin_spaceport_id = %s 
                    AND r.destination_spaceport_id = %s
                """
                
                params = [origin_id, dest_id]
                if day_of_week:
                    query += " AND fs.day_of_week = %s"
                    params.append(day_of_week)
                
                query += " ORDER BY f.departure_time"
                cursor.execute(query, params)
                direct_flights = cursor.fetchall()
                
                for flight in direct_flights:
                    itineraries.append({
                        'flight_number': flight['flight_number'],
                        'route': f"{origin} → {destination}",
                        'departure_time': str(flight['departure_time']),
                        'arrival_time': f"{flight['flight_time_hours']}h flight",
                        'aircraft': flight['aircraft'],
                        'day_of_week': flight['day_of_week']
                    })
    
    return render_template('queries/flight_finder.html', spaceports=spaceports, itineraries=itineraries, searched=searched)