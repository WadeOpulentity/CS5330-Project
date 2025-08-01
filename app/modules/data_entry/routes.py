from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db
from app.models import get_all_spaceports, get_all_planets, get_all_routes, get_all_spacecraft, get_all_space_stations

data_entry_bp = Blueprint('data_entry', __name__)

@data_entry_bp.route('/add_planet', methods=['GET', 'POST'])
def add_planet():
    if request.method == 'POST':
        name = request.form.get('name')
        size = request.form.get('size')
        population = request.form.get('population')
        
        # Validate required fields
        if not name or not size or not population:
            flash('All fields are required for planets!', 'error')
            return redirect(url_for('data_entry.add_planet'))
        
        try:
            size = int(size)
            population = int(population)
            if size <= 0 or population < 0:
                flash('Size must be positive and population cannot be negative!', 'error')
                return redirect(url_for('data_entry.add_planet'))
        except ValueError:
            flash('Size and population must be valid numbers!', 'error')
            return redirect(url_for('data_entry.add_planet'))
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO Planets (name, size, population) VALUES (%s, %s, %s)", 
                         (name, size, population))
            db.commit()
            flash('Planet added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding planet: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_planet'))
    
    return render_template('data_entry/add_planet.html')

@data_entry_bp.route('/add_space_station', methods=['GET', 'POST'])
def add_space_station():
    planets = get_all_planets()
    if request.method == 'POST':
        name = request.form.get('name')
        orbiting_planet_id = request.form.get('orbiting_planet_id')
        owner_planet_id = request.form.get('owner_planet_id')
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO SpaceStations (name, orbiting_planet_id, owner_planet_id) VALUES (%s, %s, %s)", 
                         (name, orbiting_planet_id if orbiting_planet_id else None, owner_planet_id))
            db.commit()
            flash('Space station added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding space station: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_space_station'))
    
    return render_template('data_entry/add_space_station.html', planets=planets)

@data_entry_bp.route('/add_spaceport', methods=['GET', 'POST'])
def add_spaceport():
    planets = get_all_planets()
    stations = get_all_space_stations()
    if request.method == 'POST':
        name = request.form.get('name')
        planet_id = request.form.get('planet_id')
        station_id = request.form.get('station_id')
        capacity = request.form.get('capacity')
        fee_per_seat = request.form.get('fee_per_seat')
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO Spaceports (name, planet_id, station_id, capacity, fee_per_seat) VALUES (%s, %s, %s, %s, %s)", 
                         (name, planet_id if planet_id else None, station_id if station_id else None, 
                          int(capacity) if capacity else None, float(fee_per_seat) if fee_per_seat else None))
            db.commit()
            flash('Spaceport added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding spaceport: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_spaceport'))
    
    return render_template('data_entry/add_spaceport.html', planets=planets, stations=stations)

@data_entry_bp.route('/add_route', methods=['GET', 'POST'])
def add_route():
    spaceports = get_all_spaceports()
    if request.method == 'POST':
        origin_spaceport_id = request.form.get('origin_spaceport_id')
        destination_spaceport_id = request.form.get('destination_spaceport_id')
        distance = request.form.get('distance')
        
        # Validate that origin and destination are different
        if origin_spaceport_id == destination_spaceport_id:
            flash('Origin and destination cannot be the same spaceport!', 'error')
            return redirect(url_for('data_entry.add_route'))
        
        db = get_db()
        cursor = db.cursor()
        
        # Check for existing route in either direction (bidirectional uniqueness)
        cursor.execute("""
            SELECT id FROM Routes 
            WHERE (origin_spaceport_id = %s AND destination_spaceport_id = %s) 
            OR (origin_spaceport_id = %s AND destination_spaceport_id = %s)
        """, (origin_spaceport_id, destination_spaceport_id, destination_spaceport_id, origin_spaceport_id))
        
        existing_route = cursor.fetchone()
        if existing_route:
            flash('A route between these spaceports already exists!', 'error')
            return redirect(url_for('data_entry.add_route'))
        
        try:
            cursor.execute("INSERT INTO Routes (origin_spaceport_id, destination_spaceport_id, distance) VALUES (%s, %s, %s)", 
                         (origin_spaceport_id, destination_spaceport_id, int(distance) if distance else None))
            db.commit()
            flash('Route added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding route: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_route'))
    
    return render_template('data_entry/add_route.html', spaceports=spaceports)

@data_entry_bp.route('/add_spacecraft', methods=['GET', 'POST'])
def add_spacecraft():
    if request.method == 'POST':
        type_name = request.form.get('type_name')
        capacity = request.form.get('capacity')
        range_km = request.form.get('range_km')
        
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO Spacecraft (type_name, capacity, range_km) VALUES (%s, %s, %s)", 
                         (type_name, int(capacity) if capacity else None, int(range_km) if range_km else None))
            db.commit()
            flash('Spacecraft added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding spacecraft: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_spacecraft'))
    
    return render_template('data_entry/add_spacecraft.html')

@data_entry_bp.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    routes = get_all_routes()
    spacecraft_types = get_all_spacecraft()
    
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        route_id = request.form.get('route_id')
        spacecraft_id = request.form.get('spacecraft_id')
        departure_time = request.form.get('departure_time')
        flight_time_hours = request.form.get('flight_time_hours')
        days_of_week = request.form.getlist('days_of_week')
        
        if not days_of_week:
            flash('Please select at least one day of the week', 'error')
            return redirect(url_for('data_entry.add_flight'))
        
        db = get_db()
        cursor = db.cursor()
        try:
            # Insert flight
            cursor.execute("INSERT INTO Flights (flight_number, route_id, spacecraft_id, departure_time, flight_time_hours) VALUES (%s, %s, %s, %s, %s)", 
                         (flight_number, route_id, spacecraft_id, departure_time, float(flight_time_hours) if flight_time_hours else None))
            
            # Insert flight schedules for each selected day
            for day in days_of_week:
                cursor.execute("INSERT INTO FlightSchedules (flight_number, day_of_week) VALUES (%s, %s)", 
                             (flight_number, day))
            
            db.commit()
            flash('Flight and schedule added successfully!', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error adding flight: {str(e)}', 'error')
        
        return redirect(url_for('data_entry.add_flight'))
    
    return render_template('data_entry/add_flight.html', routes=routes, spacecraft_types=spacecraft_types)

def add_planets(db, attribute_tuple):
  query = "INSERT INTO planets (name, size, population) VALUES (%s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }

def add_spacestations(db, attribute_tuple):
  query = "INSERT INTO spacestations (name, orbiting_planet_id, owner_planet_id) VALUES (%s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }

def add_spaceports(db, attribute_tuple):
  query = "INSERT INTO spaceports (name, planet_id, station_id, capacity, fee_per_seat) VALUES (%s, %s, %s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }

def add_routes(db, attribute_tuple):
  query = "INSERT INTO routes (origin_spaceport_id, destination_spaceport_id, distance) VALUES (%s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }

def add_spacecraft(db, attribute_tuple):
  query = "INSERT INTO spacecraft (type_name, capacity, range_km) VALUES (%s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }

def add_flights(db, attribute_tuple):
  query = "INSERT INTO flights (flight_number, route_id, spacecraft_id, departure_time, flight_time_hours) VALUES (%s, %s, %s, %s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }
  
def add_flighschedules(db, attribute_tuple):
  query = "INSERT INTO flightschedules (flight_number, day_of_week) VALUES (%s, %s)"
  try:
    with db.cursor as cursor:
      cursor.execute(query, attribute_tuple)
      db.commit()
      return {"success": True}
  
  except Exception as e:
    db.rollback()
    return {
      "success": False,
      "error": str(e)
    }