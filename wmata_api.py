import json
import requests
from flask import Flask, jsonify

# API endpoint URL and access key
WMATA_API_KEY = "4a612601baa84267a789154891191d30"
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
  # use 'requests' to do a GET request to the WMATA Incidents API
  # retrieve the JSON from response
    response = requests.get(INCIDENTS_URL, headers=headers)

  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
  # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
  #   -StationCode, StationName, UnitType, UnitName
  # add each incident dictionary object to the 'incidents' list
    if response.status_code == 200:
        incidents_data = response.json().get("ElevatorIncidents", list())
        
        # Add each incident if unit type matches
        incidents = []
        for incident in incidents_data:
          if (incident["UnitType"] == "ESCALATOR" and unit_type == "escalators") \
            or (incident["UnitType"] == "ELEVATOR" and unit_type == "elevators"):
            incidents.append({
                "StationCode": incident.get("StationCode"),
                "StationName": incident.get("StationName"),
                "UnitType": incident.get("UnitType"),
                "UnitName": incident.get("UnitName")
            })

        # Return the list of incident dictionaries as JSON
        return jsonify(incidents)
    
    # If response is unsuccessful, raise Exception
    raise Exception(f"Error: {INCIDENTS_URL} not found!")

if __name__ == '__main__':
    app.run(debug=True)