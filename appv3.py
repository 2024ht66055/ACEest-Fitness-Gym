# ============================================
# ACEest Fitness & Gym Management System
# Version: v3
# Description: Improved UI and user experience
# ============================================
from flask import Flask, request
import sqlite3
import random

app = Flask(__name__)

DB_NAME = "aceest_fitness.db"

program_templates = {
    "Fat Loss": ["Full Body HIIT", "Circuit Training", "Cardio + Weights"],
    "Muscle Gain": ["Push/Pull/Legs", "Upper/Lower Split", "Full Body Strength"],
    "Beginner": ["Full Body 3x/week", "Light Strength + Mobility"]
}

def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        week TEXT,
        adherence INTEGER
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER,
        name TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT,
        date TEXT,
        weight REAL,
        waist REAL,
        bodyfat REAL
    )
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users VALUES ('admin', 'admin', 'Admin')")

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    row = cur.fetchone()
    conn.close()
    return row

def get_all_clients():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, membership_status FROM clients ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_client(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO clients (name, membership_status) VALUES (?, ?)",
        (name, "Active")
    )
    conn.commit()
    conn.close()

def get_client_by_id(client_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE id=?", (client_id,))
    row = cur.fetchone()
    conn.close()
    return row

def generate_program_for_client(client_id):
    program_type = random.choice(list(program_templates.keys()))
    program_detail = random.choice(program_templates[program_type])

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE clients SET program=? WHERE id=?", (program_detail, client_id))
    conn.commit()
    conn.close()

    return program_detail

def add_workout_for_client(client_name, workout_date, workout_type, duration_min, notes):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (client_name, workout_date, workout_type, duration_min, notes))
    conn.commit()
    conn.close()

def get_workouts_for_client(client_name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT date, workout_type, duration_min, notes
        FROM workouts
        WHERE client_name=?
        ORDER BY date DESC, id DESC
    """, (client_name,))
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def home():
    return """
<h1 style='color:blue;'>🏋️ ACEest Fitness Dashboard</h1>
<p>Welcome to the Gym Management System</p>
<hr>
<p><a href="/init-db">Initialize Database</a></p>
<p><a href="/login">Login</a></p>
<p><a href="/clients">Manage Clients</a></p>
"""

@app.route("/init-db")
def initialize_database():
    init_db()
    return "Database initialized successfully"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
        <h2>Login</h2>
        <form method="post">
            <label>Username:</label><br>
            <input type="text" name="username"><br><br>

            <label>Password:</label><br>
            <input type="password" name="password"><br><br>

            <button type="submit">Login</button>
        </form>
        """

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    row = check_login(username, password)

    if row:
        role = row[0]
        return f"""
        <h2>Login successful</h2>
        <p>Welcome {username}. Role: {role}</p>
        <p><a href="/clients">Go to Clients</a></p>
        """
    else:
        return "Invalid credentials"

@app.route("/clients", methods=["GET", "POST"])
def clients():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            add_client(name)
            message = f"Client '{name}' saved successfully"
        else:
            message = "Client name cannot be empty"

    rows = get_all_clients()

    html = """
    <h2>Clients</h2>
    <form method="post">
        <label>Client Name:</label><br>
        <input type="text" name="name"><br><br>
        <button type="submit">Add Client</button>
    </form>
    """

    if message:
        html += f"<p><b>{message}</b></p>"

    html += """
    <h3>Saved Clients</h3>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Membership Status</th>
        </tr>
    """

    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td><a href="/client/{row[0]}">{row[1]}</a></td>
            <td>{row[2] if row[2] else ''}</td>
        </tr>
        """

    html += """
    </table>
    <br>
    <p><a href="/">Back to Home</a></p>
    """

    return html

@app.route("/client/<int:client_id>")
def client_detail(client_id):
    client = get_client_by_id(client_id)

    if not client:
        return "Client not found"

    return f"""
    <h2>Client Details</h2>
    <p><b>ID:</b> {client[0]}</p>
    <p><b>Name:</b> {client[1]}</p>
    <p><b>Age:</b> {client[2] if client[2] is not None else ''}</p>
    <p><b>Height:</b> {client[3] if client[3] is not None else ''}</p>
    <p><b>Weight:</b> {client[4] if client[4] is not None else ''}</p>
    <p><b>Program:</b> {client[5] if client[5] else ''}</p>
    <p><b>Calories:</b> {client[6] if client[6] is not None else ''}</p>
    <p><b>Target Weight:</b> {client[7] if client[7] is not None else ''}</p>
    <p><b>Target Adherence:</b> {client[8] if client[8] is not None else ''}</p>
    <p><b>Membership Status:</b> {client[9] if client[9] else ''}</p>
    <p><b>Membership End:</b> {client[10] if client[10] else ''}</p>

    <p><a href="/client/{client_id}/generate-program">Generate Program</a></p>
    <p><a href="/client/{client_id}/workouts">Manage Workouts</a></p>
    <p><a href="/clients">Back to Clients</a></p>
    """

@app.route("/client/<int:client_id>/generate-program")
def generate_program(client_id):
    client = get_client_by_id(client_id)

    if not client:
        return "Client not found"

    program = generate_program_for_client(client_id)

    return f"""
    <h2>Program Generated</h2>
    <p>Program for <b>{client[1]}</b>: {program}</p>
    <p><a href="/client/{client_id}">Back to Client Details</a></p>
    """

@app.route("/client/<int:client_id>/workouts", methods=["GET", "POST"])
def client_workouts(client_id):
    client = get_client_by_id(client_id)

    if not client:
        return "Client not found"

    message = ""

    if request.method == "POST":
        workout_date = request.form.get("date", "").strip()
        workout_type = request.form.get("workout_type", "").strip()
        duration_min = request.form.get("duration_min", "").strip()
        notes = request.form.get("notes", "").strip()

        if workout_date and workout_type and duration_min:
            try:
                duration_value = int(duration_min)
                add_workout_for_client(client[1], workout_date, workout_type, duration_value, notes)
                message = "Workout added successfully"
            except ValueError:
                message = "Duration must be a number"
        else:
            message = "Date, workout type, and duration are required"

    workouts = get_workouts_for_client(client[1])

    html = f"""
    <h2>Workouts for {client[1]}</h2>

    <form method="post">
        <label>Date:</label><br>
        <input type="text" name="date" placeholder="YYYY-MM-DD"><br><br>

        <label>Workout Type:</label><br>
        <input type="text" name="workout_type" placeholder="Strength / Cardio / Mobility"><br><br>

        <label>Duration (minutes):</label><br>
        <input type="text" name="duration_min"><br><br>

        <label>Notes:</label><br>
        <textarea name="notes" rows="4" cols="40"></textarea><br><br>

        <button type="submit">Add Workout</button>
    </form>
    """

    if message:
        html += f"<p><b>{message}</b></p>"

    html += """
    <h3>Workout History</h3>
    <table border="1" cellpadding="8" cellspacing="0">
        <tr>
            <th>Date</th>
            <th>Workout Type</th>
            <th>Duration</th>
            <th>Notes</th>
        </tr>
    """

    for workout in workouts:
        html += f"""
        <tr>
            <td>{workout[0]}</td>
            <td>{workout[1]}</td>
            <td>{workout[2]}</td>
            <td>{workout[3] if workout[3] else ''}</td>
        </tr>
        """

    html += f"""
    </table>
    <br>
    <p><a href="/client/{client_id}">Back to Client Details</a></p>
    <p><a href="/clients">Back to Clients</a></p>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)