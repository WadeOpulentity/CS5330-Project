from flask import Flask, render_template, request, flash
from .db import get_db
from .models import get_dashboard_data, get_all_data

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-change-this-in-production'

    @app.route('/')
    def index():
        dashboard = get_dashboard_data()
        return render_template('index.html', dashboard=dashboard)

    @app.route('/all-data')
    def view_all_data():
        all_data = get_all_data()
        return render_template('all_data.html', data=all_data)
    
    @app.route('/view-all-flights')
    def view_all_flights():
        """Display all available flights for customers."""
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                f.flight_number,
                s1.name as origin,
                s2.name as destination,
                f.departure_time,
                f.flight_time_hours,
                sc.type_name as aircraft,
                sc.capacity,
                r.distance,
                sp1.fee_per_seat + sp2.fee_per_seat as total_fee,
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
                ) as schedule_days
            FROM Flights f
            JOIN Routes r ON f.route_id = r.id
            JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
            JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
            JOIN Spaceports sp1 ON r.origin_spaceport_id = sp1.id
            JOIN Spaceports sp2 ON r.destination_spaceport_id = sp2.id
            JOIN Spacecraft sc ON f.spacecraft_id = sc.id
            LEFT JOIN FlightSchedules fs ON f.flight_number = fs.flight_number
            GROUP BY f.flight_number
            ORDER BY s1.name, s2.name, f.departure_time
        """)
        flights = cursor.fetchall()
        
        return render_template('customer/all_flights.html', flights=flights)
    
    @app.route('/book-flight', methods=['GET', 'POST'])
    def book_flight():
        """Simple flight booking interface."""
        if request.method == 'POST':
            flight_number = request.form.get('flight_number')
            passenger_name = request.form.get('passenger_name')
            seats = request.form.get('seats', 1)
            
            if flight_number and passenger_name:
                # Get flight details for confirmation
                db = get_db()
                cursor = db.cursor(dictionary=True)
                cursor.execute("""
                    SELECT 
                        f.flight_number,
                        s1.name as origin,
                        s2.name as destination,
                        f.departure_time,
                        f.flight_time_hours,
                        sc.type_name as aircraft,
                        sc.capacity,
                        sp1.fee_per_seat + sp2.fee_per_seat as total_fee
                    FROM Flights f
                    JOIN Routes r ON f.route_id = r.id
                    JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
                    JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
                    JOIN Spaceports sp1 ON r.origin_spaceport_id = sp1.id
                    JOIN Spaceports sp2 ON r.destination_spaceport_id = sp2.id
                    JOIN Spacecraft sc ON f.spacecraft_id = sc.id
                    WHERE f.flight_number = %s
                """, (flight_number,))
                flight = cursor.fetchone()
                
                if flight:
                    total_cost = float(flight['total_fee']) * int(seats)
                    flash(f'Booking confirmed for {passenger_name}! Flight {flight_number} from {flight["origin"]} to {flight["destination"]} for {seats} seat(s). Total cost: ${total_cost:.2f}', 'success')
                else:
                    flash('Flight not found!', 'error')
            else:
                flash('Please fill in all required fields!', 'error')
        
        # Get all flights for booking selection
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                f.flight_number,
                s1.name as origin,
                s2.name as destination,
                f.departure_time,
                sc.type_name as aircraft,
                sp1.fee_per_seat + sp2.fee_per_seat as total_fee
            FROM Flights f
            JOIN Routes r ON f.route_id = r.id
            JOIN Spaceports s1 ON r.origin_spaceport_id = s1.id
            JOIN Spaceports s2 ON r.destination_spaceport_id = s2.id
            JOIN Spaceports sp1 ON r.origin_spaceport_id = sp1.id
            JOIN Spaceports sp2 ON r.destination_spaceport_id = sp2.id
            JOIN Spacecraft sc ON f.spacecraft_id = sc.id
            ORDER BY s1.name, s2.name, f.departure_time
        """)
        flights = cursor.fetchall()
        
        return render_template('customer/book_flight.html', flights=flights)

    # Import and register blueprints for each module
    from .modules.data_entry.routes import data_entry_bp
    from .modules.spaceport_queries.routes import spaceport_queries_bp
    from .modules.route_queries.routes import route_queries_bp
    from .modules.flight_finder.routes import flight_finder_bp

    app.register_blueprint(data_entry_bp, url_prefix='/data_entry')
    app.register_blueprint(spaceport_queries_bp, url_prefix='/spaceport_queries')
    app.register_blueprint(route_queries_bp, url_prefix='/route_queries')
    app.register_blueprint(flight_finder_bp, url_prefix='/flight_finder')

    return app
