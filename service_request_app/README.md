# Service Request Management System

A simple web application where users can submit service requests and admins can manage them. Built with Flask and SQLite.

## Features

- **User Interface**: Easy-to-use form for submitting service requests
- **Admin Dashboard**: View, update status, and delete service requests
- **Status Tracking**: Track requests through Pending, In Progress, Completed, and Cancelled states
- **Responsive Design**: Works on desktop and mobile devices
- **Secure Login**: Admin authentication to protect requests management

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Navigate to the project directory
```bash
cd service_request_app
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On macOS/Linux
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## Usage

### For Users:
1. Go to the home page (http://localhost:5000)
2. Fill out the service request form with:
   - Full Name
   - Email Address
   - Phone Number
   - Service Type (Installation, Maintenance, Repair, Troubleshooting, Consultation, or Other)
   - Description of the request
3. Click "Submit Request"
4. You'll see a success message confirming your request was submitted

### For Admins:
1. Click "Admin Login" in the navigation menu
2. Use the demo credentials:
   - Username: `admin`
   - Password: `admin123`
3. In the dashboard, you can:
   - View all submitted service requests
   - Update the status of each request using the dropdown
   - Delete requests using the Delete button
   - Navigate through multiple pages of requests

## Project Structure

```
service_request_app/
├── app.py                 # Flask application and database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── service_requests.db   # SQLite database (created on first run)
├── templates/
│   ├── base.html         # Base template with styling
│   ├── index.html        # User service request form
│   ├── admin_login.html  # Admin login page
│   └── admin_dashboard.html  # Admin dashboard
└── static/               # Static files directory (empty by default)
```

## Database

The application uses SQLite for data storage. The database file (`service_requests.db`) is created automatically on the first run in the application directory.

### Service Request Table Schema:
- `id`: Unique identifier (Primary Key)
- `name`: Customer name
- `email`: Customer email
- `phone`: Customer phone number
- `service_type`: Type of service requested
- `description`: Detailed description of the request
- `status`: Current status (Pending, In Progress, Completed, Cancelled)
- `created_at`: Timestamp when the request was submitted

## Security Notes

**IMPORTANT**: This is a demo application with hardcoded admin credentials for testing purposes only. For production use:

1. Change the secret key in `app.py`
2. Implement proper user authentication (using Flask-Login, etc.)
3. Use environment variables for sensitive information
4. Include CSRF protection
5. Add input validation and sanitization
6. Use HTTPS for production
7. Implement proper access control and audit logging

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **ORM**: SQLAlchemy

## License

This is a demo project for learning purposes.
