from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Function to calculate distance using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers

# Mock data: list of tutors with their coordinates (latitude, longitude)
tutors = [
    ("Tutor from Ground", 19.848449437106808, 75.3210357727399),  # New York
    ("Tutor mech", 19.85076769119021, 75.32255053928108),  # Los Angeles
    ("Tutor sofa factory", 19.851418068537782, 75.32124588543763),    # London
    ("Tutor poly", 19.849943649713826, 75.32397000257328),     # Paris
    ("Tutor new MIt building", 19.848924050266497, 75.32474077496879),    # Rome
    ("Tutor bypass road", 19.851691805353816, 75.32199851827103),   # Tokyo
    ("Tutor yathart house", 19.85351239150522, 75.32383235993335),    # Moscow
    ("Tutor arcitecture", 19.850575283769313, 75.32370891045117),  # Sydney
    ("Tutor nursing ", 19.850787821805948, 75.32377401891429),  # San Francisco
    ("Tutor canteen", 19.85001132187747, 75.32257185992928),    # Berlin
]

# Route to handle POST request to find nearest tutors
@app.route('/find_nearest_tutors', methods=['POST'])
def find_nearest_tutors():
    # Get user's latitude and longitude from the request
    data = request.get_json()
    user_lat = data['latitude']
    user_lon = data['longitude']

    # Calculate distance from user to each tutor and store in a list
    tutors_with_distance = []
    for tutor in tutors:
        tutor_name, tutor_lat, tutor_lon = tutor
        distance = haversine_distance(user_lat, user_lon, tutor_lat, tutor_lon)
        tutors_with_distance.append({"name": tutor_name, "distance": distance})

    # Sort tutors by distance and return the top 10 nearest tutors
    tutors_with_distance.sort(key=lambda x: x['distance'])
    nearest_tutors = tutors_with_distance[:10]

    return jsonify(nearest_tutors)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
