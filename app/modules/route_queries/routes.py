from flask import Blueprint, render_template, request
from app.models import get_all_spaceports, find_flights_on_route

route_queries_bp = Blueprint(
    'route_queries',
    __name__
)

@route_queries_bp.route('/', methods=['GET', 'POST'])
def route_query():
    # Fetch all spaceports to populate the dropdown menus on the form.
    spaceports = get_all_spaceports()
    flights = []
    
    # This block runs when the user submits the form.
    if request.method == 'POST':
        origin_id = request.form.get('origin')
        destination_id = request.form.get('destination')

        # Check that the user selected both an origin and destination.
        if origin_id and destination_id:
            # Call the model function to get the flights for the selected route.
            flights = find_flights_on_route(origin_id, destination_id)

    # Render the page, passing the list of spaceports and any flight results.
    return render_template('queries/route_query.html', spaceports=spaceports, flights=flights)