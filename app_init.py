from datetime import datetime
import os
import logging
from flask import Flask, request, url_for, session, abort, render_template, redirect
from models import AllowedEmailEndings, BlockList, db, AllowList
from abilities import flask_app_authenticator, apply_sqlite_migrations

# Log session user information for debugging
logger = logging.getLogger(__name__)

# The app initialization must be done in this module to avoid circular dependency problems.

# DO NOT INSTANTIATE THE FLASK APP IN ANOTHER MODULE.
app = Flask(__name__, static_folder='static')

# Set a secret key for session management
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dashboard.db'
app.config['DEFAULT_THEME'] = 'light'
db.init_app(app)
# DO NOT INITIALIZE db IN ANOTHER MODULE.

# Centralized logo configuration
# Check if custom logo exists, otherwise use placeholder
import os

def get_logo_url():
    custom_logo_path = os.path.join(app.root_path, 'static', 'company_logo.png')
    if os.path.exists(custom_logo_path):
        # Check if file is not empty
        if os.stat(custom_logo_path).st_size > 0:
            return '/static/company_logo.png'
    return 'https://placehold.co/300x300?text=logo'

app.config['LOGO_URL'] = get_logo_url()

# Initialize Jinja2 filters
@app.context_processor
def inject_theme():
    return dict(theme=app.config.get('DEFAULT_THEME', 'dark'))

@app.template_filter('initials')
def initials_filter(name):
    if not name:
        return 'U'
    
    # Clean up the name
    name = name.strip()
    
    # Split the name into parts
    name_parts = name.split()
    
    if len(name_parts) >= 2:
        # Get first letter of first and last name
        return (name_parts[0][0] + name_parts[-1][0]).upper()
    elif len(name_parts) == 1 and len(name_parts[0]) >= 2:
        # Get first two letters of single name
        return name_parts[0][:2].upper()
    else:
        return 'U'

@app.before_request
def consolidated_auth_check():
    if request.endpoint == 'static' or request.endpoint == 'logout':
        return None 
    # Flask-App-Authenticator check
    logo_path = app.config['LOGO_URL'] if app.config['LOGO_URL'].startswith('http') else url_for('static', filename=app.config['LOGO_URL'].replace('/static/', ''), _external=True)
    auth_result = flask_app_authenticator(
        allowed_domains=None,
        allowed_users=None,
        logo_path=logo_path,
        app_title="Login to Doc's Lab",
        custom_styles={
            "global": "font-family: 'Inter', sans-serif; background-color: #f5f7fa; color: #495057;",
            "card": "border-radius: 0.75rem; box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); background-color: white; border: none;",
            "logo": "max-width: 100px; height: auto;",
            "title": "font-size: 1.25rem; font-weight: 600; color: #222831;",
            "input": "border-radius: 0.25rem; border: 1px solid #e0e0e0; padding: 0.375rem 0.75rem; background-color: white; color: #495057;",
            "button": "background-color: #4361ee; color: white; border-radius: 0.25rem; padding: 0.5rem 1rem; transition: background-color 0.2s ease;",
            "google_button": "border: 1px solid #4361ee; border-radius: 0.25rem; padding: 0.5rem 1rem; transition: background-color 0.2s ease; color: #4361ee; background-color: white;"
        },
        session_expiry=None
    )()
    
    if auth_result is not None:
        return auth_result
    
    # Check allowed list
    if 'user' in session and 'email' in session['user']:
        user_email = session['user']['email']
        allowed_list = AllowList.query.all()
        block_list = BlockList.query.all()
        allowed_endings = AllowedEmailEndings.query.all()
        email_ending = user_email.split('@')[-1]
        
        if BlockList and user_email in [item.email for item in block_list]:
            abort(401)
            
        if (allowed_list and user_email in [item.email for item in allowed_list]):
            # Update last login time
            admin = AllowList.query.filter_by(email=user_email).first()
            admin.last_login = datetime.utcnow()
            db.session.commit()
            return None
        elif not allowed_list and not allowed_endings:
            new_allowed = AllowList(email=user_email, last_login=datetime.utcnow())
            db.session.add(new_allowed)
            db.session.commit()
            return None
        elif (allowed_list and user_email not in [item.email for item in allowed_list]) and not allowed_endings:
            abort(401)
        elif (allowed_endings and email_ending not in [item.email_ending for item in allowed_endings]):
            abort(401)
        elif (allowed_endings and email_ending in [item.email_ending for item in allowed_endings]):
            new_allowed = AllowList(email=user_email, from_allowed_ending=True, last_login=datetime.utcnow())
            db.session.add(new_allowed)
            db.session.commit()
            return None
    
    abort(401)

@app.errorhandler(401)
def unauthorized(e):
    return render_template('unauthorized.html', logo_url=app.config['LOGO_URL']), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Apply database migrations
with app.app_context():
    apply_sqlite_migrations(db.engine, db.Model, 'migrations')