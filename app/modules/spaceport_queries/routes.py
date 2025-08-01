from flask import Blueprint, request, render_template
from app.models import get_all_spaceports, get_spaceport_flights

# TODO: Team Member 2 - Implement spaceport queries
spaceport_queries_bp = Blueprint('spaceport_queries', __name__)

# TODO: Add spaceport query routes

@spaceport_queries_bp.route('/', methods=['GET', 'POST'])
def spaceport_query():
    spaceports = get_all_spaceports()
    results = []
    searched = False

    if request.method == 'POST':
        spaceport_id = request.form.get('spaceport')
        day_of_week = request.form.get('day_of_week')
        
        if spaceport_id:
            searched = True
            results = get_spaceport_flights(spaceport_id, day_of_week if day_of_week else None)

    return render_template('queries/spaceport_query.html', spaceports=spaceports, results=results, searched=searched)