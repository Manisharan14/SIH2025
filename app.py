from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ---------- MySQL Configuration ----------
DB_CONFIG = {
    "host": "127.0.0.1",        # or your MySQL server IP
    "user": "root",             # your MySQL username
    "password": "Hack2025",# your MySQL password
    "database": "SIH2025_db"    # your MySQL database name
}

# ---------- Database Helper Functions ----------
def db_get_user(email):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "SELECT email,name,phone,idNumber,language,password FROM users WHERE email=%s",
        (email,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "email": row[0],
        "name": row[1],
        "phone": row[2],
        "idNumber": row[3],
        "language": row[4],
        "password": row[5]
    }

def db_create_user(email, name, phone, idNumber, language, password):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(email,name,phone,idNumber,language,password) VALUES (%s,%s,%s,%s,%s,%s)",
        (email, name, phone, idNumber, language, password)
    )
    conn.commit()
    conn.close()

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register_page")
def signup_page():
    return render_template("register.html")

# -------- Signup --------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    id_number = data.get("idNumber")
    language = data.get("language")
    password = data.get("password")

    if not all([name, email, phone, id_number, language, password]):
        return jsonify({"success": False, "message": "All fields required!"})

    if db_get_user(email):
        return jsonify({"success": False, "message": "Email already registered!"})

    db_create_user(email, name, phone, id_number, language, password)
    return jsonify({"success": True, "message": "Signup successful ✅"})

# -------- Login --------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = db_get_user(email)
    if user and user["password"] == password:
        return jsonify({"success": True, "message": "Login successful ✅"})
    
    return jsonify({"success": False, "message": "Invalid credentials ❌"})

# -------- Run Server --------
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
