# Project Responsibilities

Here are the responsibilities we came up with using GPT to try and make the work fair.

---

## McLean
* **Task**: Implement database models and all data entry functionality, ensuring all data constraints are satisfied.
* **Primary Files**:
    * `app/db.py`
    * `app/models.py`
    * `app/modules/data_entry/routes.py`

---

## Alyson
* **Task**: Implement the "Spaceport Query" to show connected spaceports and flights within a given date range.
* **Primary Files**:
    * `app/modules/spaceport_queries/routes.py`
    * (will also add query functions to `app/models.py`), wait til end.

---

## Wade
* **Task**: Implement the "Route Query" to show all flights and their details for a specific route.
* **Primary Files**:
    * `app/modules/route_queries/routes.py`
    * (will also add query functions to `app/models.py`), wait til end.

---

## Manny
* **Task**: Implement the "Flight Finder" for searching multi-stop itineraries based on user-defined criteria.
* **Primary Files**:
    * `app/modules/flight_finder/routes.py`
    * (will also add query functions to `app/models.py` or `app/utils.py`)

---

## Interface Notes
* **System Requirements**: To make our demo ensure that we met all of the requirments we decided to have 2 sections of querying and a section for data entry. This ensures that we get full credit for the project.
* **Additional Section (Realism)**: For a more realistic use case of our system, we creates a section that allows users to book flights. This section will allow users to select a flight and book it. 
    
