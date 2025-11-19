from flask import Flask, render_template, request, redirect, flash
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# -----------------------------
# Flask App
# -----------------------------
app = Flask(__name__)


# -----------------------------
# Load environment
# -----------------------------
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY") or "development_secret_key_123"
FRESHDESK_DOMAIN = os.getenv("FRESHDESK_DOMAIN")
API_KEY = os.getenv("API_KEY")

# -----------------------------
# Database Setup
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# -----------------------------
# User Model
# -----------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Initialize DB
with app.app_context():
    db.create_all()

# -----------------------------
# Login Manager Setup
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -----------------------------
# User Loader
# -----------------------------
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")

# -----------------------------
# REGISTER PAGE
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form.get("role", "user")
        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect("/register")
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please login.")
        return redirect("/login")
    return render_template("register.html")

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    response = requests.get(
        f"{FRESHDESK_DOMAIN}/api/v2/tickets",
        auth=HTTPBasicAuth(API_KEY, "X")
    )
    tickets = response.json()
    total = len(tickets)
    open_tickets = sum(1 for t in tickets if t["status"] == 2)
    high_priority = sum(1 for t in tickets if t["priority"] in [3, 4])
    latest = tickets[-1]["id"] if total > 0 else 0
    return render_template(
        "dashboard.html",
        title="Dashboard",
        total=total,
        open=open_tickets,
        high=high_priority,
        latest=latest,
        user=current_user
    )

# -----------------------------
# HOME → redirect to dashboard
# -----------------------------
@app.route("/")
def home():
    return redirect("/dashboard")

# -----------------------------
# CREATE PAGE
# -----------------------------
@app.route("/create")
@login_required
def create():
    return render_template("form.html")

# -----------------------------
# CREATE TICKET API
# -----------------------------
@app.route("/create-ticket", methods=["POST"])
@login_required
def create_ticket():
    data = {
        "email": request.form["email"],
        "subject": request.form["subject"],
        "description": request.form["description"],
        "priority": int(request.form["priority"]),
        "status": 2
    }
    response = requests.post(
        f"{FRESHDESK_DOMAIN}/api/v2/tickets",
        auth=HTTPBasicAuth(API_KEY, "X"),
        json=data
    )
    if response.status_code == 201:
        return render_template("achive.html")
    else:
        return render_template("error.html", message=response.text)

# -----------------------------
# VIEW ALL TICKETS
# -----------------------------
@app.route("/view-tickets")
@login_required
def view_tickets():
    response = requests.get(
        f"{FRESHDESK_DOMAIN}/api/v2/tickets",
        auth=HTTPBasicAuth(API_KEY, "X")
    )
    tickets = response.json()
    return render_template("tickets.html", tickets=tickets)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
