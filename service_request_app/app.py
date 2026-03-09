from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_requests.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

db = SQLAlchemy(app)

# Database Model
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'service': self.service,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Admin credentials (in production, use proper authentication)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_request():
    try:
        data = request.get_json()
        
        new_request = ServiceRequest(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            service_type=data.get('service_type'),
            description=data.get('description')
        )
        
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Service request submitted successfully!'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/submit-request', methods=['POST'])
def submit_service_request():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Extract and validate required fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        mobile = data.get('phone', '').strip()  # phone field from form becomes mobile in DB
        service = data.get('service_type', '').strip()  # service_type field from form becomes service in DB
        message = data.get('description', '').strip()  # description field from form becomes message in DB
        
        # Validation
        errors = []
        
        # Name validation
        if not name:
            errors.append('Name is required')
        elif len(name) < 2:
            errors.append('Name must be at least 2 characters long')
        elif len(name) > 100:
            errors.append('Name must be less than 100 characters')
        
        # Email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            errors.append('Email is required')
        elif not re.match(email_pattern, email):
            errors.append('Please provide a valid email address')
        
        # Mobile validation (10 digits)
        if not mobile:
            errors.append('Mobile number is required')
        elif not mobile.isdigit():
            errors.append('Mobile number must contain only digits')
        elif len(mobile) != 10:
            errors.append('Mobile number must be exactly 10 digits')
        
        # Service validation
        valid_services = ['PAN Card Apply', 'Aadhaar Update', 'Passport Apply', 'Online Form Filling', 'Document Printing']
        if not service:
            errors.append('Service is required')
        elif service not in valid_services:
            errors.append('Please select a valid service')
        
        # Message validation
        if not message:
            errors.append('Message is required')
        elif len(message) < 10:
            errors.append('Message must be at least 10 characters long')
        elif len(message) > 1000:
            errors.append('Message must be less than 1000 characters')
        
        # If there are validation errors, return them
        if errors:
            return jsonify({'success': False, 'message': 'Validation failed', 'errors': errors}), 400
        
        # Create new service request
        new_request = ServiceRequest(
            name=name,
            email=email,
            mobile=mobile,
            service=service,
            message=message
        )
        
        # Save to database
        db.session.add(new_request)
        db.session.commit()
        
        # Return success response with request ID
        return jsonify({
            'success': True, 
            'message': 'Service request submitted successfully!',
            'request_id': new_request.id,
            'data': {
                'name': name,
                'email': email,
                'mobile': mobile,
                'service': service,
                'message': message[:100] + '...' if len(message) > 100 else message
            }
        }), 201
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in submit_service_request: {str(e)}")
        return jsonify({'success': False, 'message': 'An internal error occurred. Please try again.'}), 500

@app.route('/admin.html')
@login_required
def admin_page():
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    page = request.args.get('page', 1, type=int)
    requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin_dashboard.html', requests=requests)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/requests', methods=['GET'])
@login_required
def get_requests():
    try:
        # Get all service requests ordered by creation date (newest first)
        service_requests = ServiceRequest.query.order_by(ServiceRequest.created_at.desc()).all()
        
        # Convert to list of dictionaries
        requests_list = []
        for req in service_requests:
            requests_list.append({
                'id': req.id,
                'name': req.name,
                'mobile': req.mobile,
                'email': req.email,
                'service': req.service,
                'date': req.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify({
            'success': True,
            'requests': requests_list,
            'total': len(requests_list)
        }), 200
        
    except Exception as e:
        print(f"Error in get_requests: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while fetching requests'}), 500

@app.route('/api/requests/<int:request_id>/status', methods=['PUT'])
@login_required
def update_request_status(request_id):
    try:
        service_req = ServiceRequest.query.get(request_id)
        if not service_req:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        
        data = request.get_json()
        service_req.status = data.get('status', service_req.status)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Status updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/requests/<int:request_id>', methods=['DELETE'])
@login_required
def delete_request(request_id):
    try:
        service_req = ServiceRequest.query.get(request_id)
        if not service_req:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        
        db.session.delete(service_req)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Request deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
