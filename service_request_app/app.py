from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_requests.db'
app.config['SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)

# Database Model
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    service = db.Column(db.String(100))
    message = db.Column(db.Text)
    status = db.Column(db.String(50), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit-request', methods=['POST'])
def submit_request():
    data = request.get_json()

    req = ServiceRequest(
        name=data['name'],
        email=data['email'],
        mobile=data['phone'],
        service=data['service_type'],
        message=data['description']
    )

    db.session.add(req)
    db.session.commit()

    return jsonify({"success": True})

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for("admin_dashboard"))

    return render_template("admin_login.html")

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
    return render_template("admin_dashboard.html", requests=requests)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/api/requests/<int:id>', methods=['DELETE'])
@login_required
def delete_request(id):
    req = ServiceRequest.query.get(id)
    db.session.delete(req)
    db.session.commit()
    return jsonify({"success":True})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
