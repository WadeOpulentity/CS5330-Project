# Project Responsibilities

Here are the responsibilities GPT came up with. We can talk about who is doing what in meeting.

---

## Team Member 1
* **Task**: Implement database models and all data entry functionality, ensuring all data constraints are satisfied.
* **Primary Files**:
    * `app/db.py`
    * `app/models.py`
    * `app/modules/data_entry/routes.py`

---

## Team Member 2
* **Task**: Implement the "Spaceport Query" to show connected spaceports and flights within a given date range.
* **Primary Files**:
    * `app/modules/spaceport_queries/routes.py`
    * (will also add query functions to `app/models.py`)

---

## Team Member 3
* **Task**: Implement the "Route Query" to show all flights and their details for a specific route.
* **Primary Files**:
    * `app/modules/route_queries/routes.py`
    * (will also add query functions to `app/models.py`)

---

## Team Member 4
* **Task**: Implement the "Flight Finder" for searching multi-stop itineraries based on user-defined criteria.
* **Primary Files**:
    * `app/modules/flight_finder/routes.py`
    * (will also add query functions to `app/models.py` or `app/utils.py`)