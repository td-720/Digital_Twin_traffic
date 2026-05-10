from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "data/traffic.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT,
        speed INTEGER,
        speed_limit INTEGER,
        status TEXT,
        location TEXT,
        image TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

# --- API ENDPOINTS ---

@app.route('/api/record', methods=['POST'])
def receive_record():
    """Receives processed record from the pipeline and stores it."""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO traffic_logs (plate, speed, speed_limit, status, location, image, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (data['plate'], data['speed'], data['speed_limit'], data['status'], data['location'], data['image'], data['timestamp']))
    
    conn.commit()
    conn.close()

    return jsonify({"status": "stored", "record": data}), 201


@app.route('/images/<filename>')
def serve_image(filename):
    """Tells Flask how to serve the actual image files."""
    return send_from_directory('images', filename)

@app.route('/api/latest')
def latest():
    """Endpoint for the dashboard to fetch the latest records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Fetch the 15 most recent records
    cursor.execute("SELECT * FROM traffic_logs ORDER BY id DESC LIMIT 15")
    
    # Format rows into dictionaries for the JSON response
    columns = [desc[0] for desc in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(rows)

# --- FRONTEND ROUTE ---

@app.route('/')
def dashboard():
    """Serves the live monitoring dashboard."""
    return render_template('index.html')

if __name__ == "__main__":
    init_db()
    # Run on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)