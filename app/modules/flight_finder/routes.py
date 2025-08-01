from flask import Blueprint, request, render_template

from app.models import (
    get_spaceport_id_by_name,
    get_routes_from_spaceport,
    get_flights_for_route_on_day,
)
from app.db import get_db
import datetime

bp = Blueprint('flight_finder', __name__, url_prefix='/flight_finder')

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

@bp.route('/', methods=['GET', 'POST'])
def flight_finder():
    itineraries = []
    if request.method == 'POST':
        origin = request.form.get('origin', '').strip()
        destination = request.form.get('destination', '').strip()
        date_str = request.form.get('date', '').strip()
        try:
            max_stops = int(request.form.get('max_stops', 0))
        except ValueError:
            max_stops = 0
            print(f"flight_finder, invalid max_stops: {request.form.get('max_stops')}")
        raw_paths = find_itineraries(origin, destination, date_str, max_stops)
        for idx in range(len(raw_paths)):
            path = raw_paths[idx]
            route_str = ''
            for i, sp in enumerate(path):
                if i > 0:
                    route_str += ' → '
                route_str += sp
            flight_num = f"FN{idx+1:03d}"
            itineraries.append({
                'flight_number': flight_num,
                'route': route_str,
                'departure_time': 'TBD',
                'arrival_time': 'TBD',
            })
    return render_template('queries/flight_finder.html', itineraries=itineraries)