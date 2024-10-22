# pip install flask psycopg2 requests

from flask import Flask, request, jsonify
import psycopg2
import requests

app = Flask(__name__)

# Configure PostgreSQL connection
DB_CONFIG = {
    "dbname": "carbon_footprint_db",
    "user": "your_db_username",
    "password": "your_db_password",
    "host": "localhost"
}

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_CONFIG['dbname'], 
        user=DB_CONFIG['user'], 
        password=DB_CONFIG['password'], 
        host=DB_CONFIG['host']
    )
    return conn

# API to calculate the carbon footprint and store data in PostgreSQL
@app.route('/calculate', methods=['POST'])
def calculate_footprint():
    data = request.get_json()

    miles_driven = data.get('miles_driven')
    diet_type = data.get('diet_type')
    energy_usage = data.get('energy_usage')

    if not miles_driven or not diet_type or not energy_usage:
        return jsonify({"error": "Missing data"}), 400

    # Call an external API to get real-time emission factors (example)
    emission_data = get_emission_factors()

    # Calculate the footprint based on user inputs and emission factors
    footprint = calculate_footprint_logic(miles_driven, diet_type, energy_usage, emission_data)

    # Save the result to the database
    save_footprint_to_db(data, footprint)

    return jsonify({"carbon_footprint": footprint})

# Function to handle calculation logic
def calculate_footprint_logic(miles, diet, energy, emission_data):
    diet_factor = {'meat': 150, 'vegetarian': 100, 'vegan': 70}.get(diet, 100)

    # Assume 0.4 kg CO2 per mile for driving and 0.5 kg CO2 per kWh of energy
    driving_footprint = miles * emission_data.get('miles_factor', 0.4) * 30
    energy_footprint = energy * emission_data.get('energy_factor', 0.5)

    total_footprint = driving_footprint + diet_factor + energy_footprint
    return total_footprint

# Function to save the footprint data in the PostgreSQL database
def save_footprint_to_db(data, footprint):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO carbon_footprints (miles_driven, diet_type, energy_usage, carbon_footprint) 
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (data['miles_driven'], data['diet_type'], data['energy_usage'], footprint))

    conn.commit()
    cursor.close()
    conn.close()

# Fetch emission factors from an external API (Example)
def get_emission_factors():
    try:
        response = requests.get("https://api.example.com/emission_factors")
        if response.status_code == 200:
            return response.json()  # Assuming the API returns a JSON with 'miles_factor' and 'energy_factor'
        else:
            return {"miles_factor": 0.4, "energy_factor": 0.5}  # Default values if API fails
    except Exception as e:
        print(f"Error fetching emission factors: {e}")
        return {"miles_factor": 0.4, "energy_factor": 0.5}

if __name__ == '__main__':
    app.run(debug=True)
