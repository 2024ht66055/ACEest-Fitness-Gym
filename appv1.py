from flask import Flask, request
import sqlite3
from datetime import datetime, date
import matplotlib.pyplot as plt

DB_NAME = "aceest_fitness.db"


class ACEestApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ACEest Fitness & Performance")
        self.root.geometry("1300x850")
        self.root.configure(bg="#1a1a1a")

        self.conn = None
        self.cur = None

        self.current_client = None

        self.init_db()
        self.setup_data()
        self.setup_ui()
        self.refresh_client_list()

    # ---------- DATABASE ----------

    def init_db(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cur = self.conn.cursor()

        # Ensure clients table has the correct columns.
        # For a simple desktop app, easiest is to drop and recreate if schema is old.
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='clients'"
        )
        exists = self.cur.fetchone() is not None

        if exists:
            # Check schema
            self.cur.execute("PRAGMA table_info(clients)")
            cols = [row[1] for row in self.cur.fetchall()]
            required = {
                "id",
                "name",
                "age",
                "height",
                "weight",
                "program",
                "calories",
                "target_weight",
                "target_adherence",
            }
            if not required.issubset(set(cols)):
                # Drop and recreate with full schema
                self.cur.execute("DROP TABLE clients")

        # Create clients with full schema
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                age INTEGER,
                height REAL,
                weight REAL,
                program TEXT,
                calories INTEGER,
                target_weight REAL,
                target_adherence INTEGER
            )
            """
        )

        # Weekly adherence
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                week TEXT,
                adherence INTEGER
            )
            """
        )

        # Workouts (session-level)
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT,
                date TEXT,
                workout_type TEXT,
                duration_min INTEGER,
                notes TEXT
            )
            """
        )

        # Exercises (per workout)
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workout_id INTEGER,
                name TEXT,
                sets INTEGER,
                reps INTEGER,
                weight REAL
            )
            """
        )

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
    <h1>ACEest Fitness Flask App</h1>
    <p><a href="/init-db">Initialize Database</a></p>
    <p><a href="/login">Go to Login</a></p>
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
            category = "Obese"
            risk = "Higher risk; prioritize fat loss, consistency, and supervision."

        messagebox.showinfo(
            "BMI Info",
            f"BMI for {self.current_client}: {bmi} ({category})\n\nRisk note: {risk}",
        )

    # ---------- WORKOUT LOGGING ----------

    def ensure_client(self) -> bool:
        name = self.current_client or self.name.get().strip() or self.client_list.get()
        if not name:
            messagebox.showwarning("No Client", "Select or enter client first")
            return False
        self.current_client = name
        return True

    def open_log_workout_window(self):
        if not self.ensure_client():
            return

        win = tk.Toplevel(self.root)
        win.title(f"Log Workout – {self.current_client}")
        win.configure(bg="#1a1a1a")
        win.geometry("450x500")

        tk.Label(win, text="Date (YYYY-MM-DD)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=date_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Workout Type", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        type_var = tk.StringVar()
        ttk.Combobox(
            win,
            textvariable=type_var,
            values=["Strength", "Hypertrophy", "Conditioning", "Mixed", "Mobility"],
            state="readonly",
        ).pack()

        tk.Label(win, text="Duration (min)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        dur_var = tk.IntVar(value=60)
        tk.Entry(win, textvariable=dur_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Notes", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        notes_text = tk.Text(win, height=4, bg="#333", fg="white")
        notes_text.pack(fill="x", padx=10)

        tk.Label(win, text="Exercise Name", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        ex_name_var = tk.StringVar()
        tk.Entry(win, textvariable=ex_name_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Sets", bg="#1a1a1a", fg="white").pack(pady=(5, 0))
        sets_var = tk.IntVar(value=3)
        tk.Entry(win, textvariable=sets_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Reps", bg="#1a1a1a", fg="white").pack(pady=(5, 0))
        reps_var = tk.IntVar(value=10)
        tk.Entry(win, textvariable=reps_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Weight (kg)", bg="#1a1a1a", fg="white").pack(pady=(5, 0))
        ex_weight_var = tk.DoubleVar(value=0.0)
        tk.Entry(win, textvariable=ex_weight_var, bg="#333", fg="white").pack()

        def save_workout():
            try:
                w_date = date_var.get().strip()
                w_type = type_var.get().strip()
                duration = int(dur_var.get())
                notes = notes_text.get("1.0", "end").strip()

                if not w_date or not w_type:
                    messagebox.showerror("Error", "Date and workout type are required")
                    return

                self.cur.execute(
                    """
                    INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.current_client, w_date, w_type, duration, notes),
                )
                workout_id = self.cur.lastrowid

                ex_name = ex_name_var.get().strip()
                ex_sets = sets_var.get()
                ex_reps = reps_var.get()
                ex_weight = ex_weight_var.get()

                if ex_name:
                    self.cur.execute(
                        """
                        INSERT INTO exercises (workout_id, name, sets, reps, weight)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (workout_id, ex_name, ex_sets, ex_reps, ex_weight),
                    )

                self.conn.commit()
                self.set_status(f"Workout logged for {self.current_client}")
                messagebox.showinfo("Saved", "Workout logged successfully")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Save Workout", command=save_workout).pack(pady=15)

    def open_log_metrics_window(self):
        if not self.ensure_client():
            return

        win = tk.Toplevel(self.root)
        win.title(f"Log Body Metrics – {self.current_client}")
        win.configure(bg="#1a1a1a")
        win.geometry("350x300")

        tk.Label(win, text="Date (YYYY-MM-DD)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        date_var = tk.StringVar(value=date.today().isoformat())
        tk.Entry(win, textvariable=date_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Weight (kg)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        weight_var = tk.DoubleVar(value=self.weight.get() if self.weight.get() > 0 else 0.0)
        tk.Entry(win, textvariable=weight_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Waist (cm)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        waist_var = tk.DoubleVar(value=0.0)
        tk.Entry(win, textvariable=waist_var, bg="#333", fg="white").pack()

        tk.Label(win, text="Bodyfat (%)", bg="#1a1a1a", fg="white").pack(pady=(10, 0))
        bf_var = tk.DoubleVar(value=0.0)
        tk.Entry(win, textvariable=bf_var, bg="#333", fg="white").pack()

        def save_metrics():
            try:
                m_date = date_var.get().strip()
                m_weight = weight_var.get()
                m_waist = waist_var.get()
                m_bf = bf_var.get()

                if not m_date:
                    messagebox.showerror("Error", "Date is required")
                    return

                self.cur.execute(
                    """
                    INSERT INTO metrics (client_name, date, weight, waist, bodyfat)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.current_client, m_date, m_weight, m_waist, m_bf),
                )
                self.conn.commit()
                if m_weight > 0:
                    self.weight.set(m_weight)
                self.refresh_summary()
                self.set_status(f"Metrics logged for {self.current_client}")
                messagebox.showinfo("Saved", "Metrics logged successfully")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(win, text="Save Metrics", command=save_metrics).pack(pady=15)

    # ---------- WORKOUT HISTORY (TREEVIEW) ----------

    def open_workout_history_window(self):
        if not self.ensure_client():
            return

        win = tk.Toplevel(self.root)
        win.title(f"Workout History – {self.current_client}")
        win.geometry("700x400")

        columns = ("date", "type", "duration", "notes")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        tree.heading("date", text="Date")
        tree.heading("type", text="Type")
        tree.heading("duration", text="Duration (min)")
        tree.heading("notes", text="Notes")

        tree.column("date", width=100, anchor="center")
        tree.column("type", width=100, anchor="center")
        tree.column("duration", width=120, anchor="center")
        tree.column("notes", width=350, anchor="w")

        tree.pack(fill="both", expand=True)

        self.cur.execute(
            """
            SELECT date, workout_type, duration_min, notes
            FROM workouts
            WHERE client_name=?
            ORDER BY date DESC, id DESC
            """,
            (self.current_client,),
        )
        rows = self.cur.fetchall()

        for row in rows:
            tree.insert("", "end", values=row)

        self.set_status(f"Loaded workout history for {self.current_client}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ACEestApp(root)
    root.mainloop()
