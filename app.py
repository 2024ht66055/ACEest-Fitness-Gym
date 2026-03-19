from flask import Flask, jsonify, request
import sqlite3
import random
from datetime import date

app = Flask(__name__)

DB_NAME = "aceest_fitness.db"

program_templates = {
    "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
    "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"]
}

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        age INTEGER,
        height REAL,
        weight REAL,
        program TEXT,
        calories INTEGER,
        target_weight REAL,
        target_adherence INTEGER,
        membership_status TEXT,
        membership_end TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        workout_type TEXT,
        duration_min INTEGER,
        notes TEXT
    )
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin', 'admin', 'Admin')")

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return jsonify({
        "message": "ACEest Fitness & Gym Flask App Running",
        "status": "success"
    })

@app.route("/clients", methods=["GET"])
def get_clients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients ORDER BY name")
    rows = cur.fetchall()
    conn.close()

    clients = [dict(row) for row in rows]
    return jsonify(clients)

@app.route("/add-client", methods=["POST"])
def add_client():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Client name is required"}), 400

    name = data["name"].strip()
    age = data.get("age")
    height = data.get("height")
    weight = data.get("weight")
    membership_status = data.get("membership_status", "Active")
    membership_end = data.get("membership_end", str(date.today()))

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO clients (name, age, height, weight, membership_status, membership_end)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, age, height, weight, membership_status, membership_end))
        conn.commit()
        return jsonify({"message": f"Client {name} added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Client already exists"}), 409
    finally:
        conn.close()

@app.route("/generate-program/<name>", methods=["POST"])
def generate_program(name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clients WHERE name = ?", (name,))
    client = cur.fetchone()

    if not client:
        conn.close()
        return jsonify({"error": "Client not found"}), 404

    program_type = random.choice(list(program_templates.keys()))
    program_detail = random.choice(program_templates[program_type])

    cur.execute("UPDATE clients SET program=? WHERE name=?", (program_detail, name))
    conn.commit()
    conn.close()

    return jsonify({
        "client": name,
        "program_type": program_type,
        "program": program_detail
    })

@app.route("/membership/<name>", methods=["GET"])
def check_membership(name):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT membership_status, membership_end FROM clients WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Client not found"}), 404

    return jsonify({
        "client": name,
        "membership_status": row["membership_status"],
        "membership_end": row["membership_end"]
    })

@app.route("/add-workout", methods=["POST"])
def add_workout():
    data = request.get_json()

    required_fields = ["client_name", "date", "workout_type", "duration_min"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required workout fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["client_name"],
        data["date"],
        data["workout_type"],
        data["duration_min"],
        data.get("notes", "")
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Workout added successfully"}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)