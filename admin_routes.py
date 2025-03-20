from routes import url_for

from routes import redirect

from routes import session

from flask import jsonify, request
from models import db, AllowList, BlockList, AllowedEmailEndings
from datetime import datetime
from app_init import app

# API route to create new company admin
@app.route('/api/company_admins/create', methods=['POST'])
def create_company_admin():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required'}), 400
        
    try:
        # Check if admin already exists
        existing_admin = AllowList.query.filter_by(email=email).first()
        if existing_admin:
            return jsonify({'status': 'error', 'message': 'Admin already exists'}), 400
        
        new_admin = AllowList(email=email, last_login=datetime.utcnow())
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Admin added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API route to create new allowed email ending
@app.route('/api/allowed_email_endings/create', methods=['POST'])
def create_email_ending():
    data = request.get_json()
    email_ending = data.get('email_ending')
    
    if not email_ending:
        return jsonify({'status': 'error', 'message': 'Email ending is required'}), 400
        
    try:
        # Check if domain already exists
        existing_domain = AllowedEmailEndings.query.filter_by(email_ending=email_ending).first()
        if existing_domain:
            return jsonify({'status': 'error', 'message': 'Domain already exists'}), 400
        
        new_ending = AllowedEmailEndings(email_ending=email_ending)
        db.session.add(new_ending)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'New domain allowed successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API route to delete admin
@app.route('/api/delete_admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    try:
        admin = AllowList.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Admin deleted successfully'})
        return jsonify({'status': 'error', 'message': 'Admin not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API route to delete email ending
@app.route('/api/delete_email_ending/<int:ending_id>', methods=['DELETE'])
def delete_email_ending(ending_id):
    try:
        ending = AllowedEmailEndings.query.get(ending_id)
        if ending:
            db.session.delete(ending)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Email ending deleted successfully'})
        return jsonify({'status': 'error', 'message': 'Email ending not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API route to block admin
@app.route('/api/block_admin/<int:admin_id>', methods=['POST'])
def block_admin(admin_id):
    try:
        admin = AllowList.query.get(admin_id)
        if admin:
            blocked = BlockList(email=admin.email)
            db.session.add(blocked)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Admin blocked successfully'})
        return jsonify({'status': 'error', 'message': 'Admin not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# API route to unblock admin
@app.route('/api/unblock_admin/<int:admin_id>', methods=['POST'])
def unblock_admin(admin_id):
    try:
        admin = AllowList.query.get(admin_id)
        if admin:
            blocked = BlockList.query.filter_by(email=admin.email).first()
            if blocked:
                db.session.delete(blocked)
                db.session.commit()
                return jsonify({'status': 'success', 'message': 'Admin unblocked successfully'})
            return jsonify({'status': 'error', 'message': 'Admin not found in block list'}), 404
        return jsonify({'status': 'error', 'message': 'Admin not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home_route'))
