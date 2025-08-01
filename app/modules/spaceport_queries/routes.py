from flask import Blueprint, request, render_template
from app.models import spaceport_arrivals_departures_query, date_and_spaceport_arrivals_departures_query

# TODO: Team Member 2 - Implement spaceport queries
spaceport_queries_bp = Blueprint('spaceport_queries', __name__, template_folder='../../../templates/queries')

# TODO: Add spaceport query routes

@spaceport_queries_bp('/', methods=['GET', 'POST'])
def spaceport_query():
    results = []

    if request.method == 'POST':
        spaceport_id = request.form.get('spaceport')
        day_of_week = request.form.get('date')

        # check that user inputed either both spaceport_id and day_of_week, or just spaceport_id
        if spaceport_id and day_of_week:
            results = date_and_spaceport_arrivals_departures_query(day_of_week, spaceport_id)
        elif spaceport_id:
            results = spaceport_arrivals_departures_query(spaceport_id)

    
    return render_template('queries/spaceport_query.html', results=results)