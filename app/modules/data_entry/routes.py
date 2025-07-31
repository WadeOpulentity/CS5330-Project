from flask import Blueprint

# TODO: Team Member 1 - Implement data entry routes
data_entry_bp = Blueprint('data_entry', __name__, template_folder='../../../templates/data_entry')

# TODO: Add routes for:
# - add_planet
# - add_space_station  
# - add_spaceport
# - add_route
# - add_spacecraft
# - add_flight

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