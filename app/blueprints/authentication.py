from flask import Blueprint, request, jsonify, render_template,redirect, url_for
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required,verify_jwt_in_request,get_jwt)
import logging
from app.dataBaseConnection import database 
import re
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env


authentication_bp = Blueprint("authentication", __name__)
# Initialize JWT Manager
jwt = JWTManager()


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Access the 'users' collection from the database
users_collection = database['users']

def validate_signup_data(username, email, password):
    # Check if all fields are not empty
    if not username or not email or not password:
        return "All fields are required."
    # Username allows letters, numbers, underscores, and spaces, between 3-50 characters
    if not re.match(r"^[a-zA-Z0-9_ ]{3,50}$", username):
        return "Username must be 3-50 characters long and can include letters, numbers, underscores, and spaces."
    # Validate email format
    if not re.match(r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", email):
        return "Invalid email format."
    # Password must be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one special character
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

@authentication_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('registration.html'), 200
    
    # Handle POST request for signup
    username = request.form.get('name').strip()
    email = request.form.get('email').strip().lower()
    password = request.form.get('password')
    
    # Validate the provided sign-up data
    error = validate_signup_data(username, email, password)
    if error:
        return jsonify({'message': error}), 422
    
    # Check if the email already exists in the MongoDB collection
    if users_collection.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 422
    
    # Hash the password and insert the new user into the MongoDB collection
    hashed_password = generate_password_hash(password)
    new_user = {
        'username': username,
        'email': email,
        'password': hashed_password
    }
    users_collection.insert_one(new_user)
    logger.info(f"User {email} created successfully.")
    return jsonify({'message': 'User created successfully'}), 201

@authentication_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        # Check if the user already has a valid token
        verify_jwt_in_request(optional=True)
        jwt_data = get_jwt()
        if jwt_data:
            return redirect(url_for('mind_map.func'))  # Redirect to mind map if token exists
    except:
        pass  # No valid token, proceed with login process
    
    if request.method == 'GET':
        return render_template('registration.html'), 200
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Fetch the user document from the MongoDB collection
    user = users_collection.find_one({'email': email})
    if not user:
        return jsonify({'login': False, 'message': 'Invalid credentials.'}), 401
    
    # Check if the provided password matches the hashed password stored in the database
    if not check_password_hash(user['password'], password):
        return jsonify({'login': False, 'message': 'Invalid credentials.'}), 401
    
    # Generate an access token
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
    
    response = jsonify({'login': True, 'message': 'Signed in successfully.'}) 
    response.status_code = 200
    set_access_cookies(response, access_token)
    
    return response

@authentication_bp.route('/logout', methods=['POST'])
@jwt_required()  # Ensure the user is logged in
def logout():
    response = jsonify({"message": "Successfully logged out"})
    unset_jwt_cookies(response)  # Clear the JWT cookies
    response.status_code = 200
    return response  # Ensure to return the response object