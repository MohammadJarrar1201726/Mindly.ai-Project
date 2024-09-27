from flask import Flask, request, jsonify , render_template
from werkzeug.security import generate_password_hash,check_password_hash
import re


from .blueprints.summarization_routes import summarization_bp
from .blueprints.mind_map import mind_map_bp
from .blueprints.home_page import home_page_bp
from .blueprints.authentication import authentication_bp
from app.blueprints.export_pdf_file import export_pdf_file_bp

from .blueprints.authentication import authentication_bp ,jwt
from .dataBaseConnection import database 

from dotenv import load_dotenv
from typing import Dict
from .injectors import inject_config_variables_into_templates
from datetime import timedelta
import os
# load environment variables
load_dotenv()


# Initialize new flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure your app's secret key and JWT settings
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_SECURE'] = False  # Set to True for production with HTTPS
app.config['JWT_ACCESS_TOKEN_EXPIRES'] =timedelta(days=1)
app.config['JWT_ALGORITHM'] = "HS256"
app.config['JWT_COOKIE_HTTPONLY'] = True  # Prevent client-side access to the cookie


# Initialize the JWT manager with the Flask application
jwt.init_app(app)

# Register blueprints
app.register_blueprint(summarization_bp)
app.register_blueprint(mind_map_bp)
app.register_blueprint(home_page_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(export_pdf_file_bp)  


# Wrap our project with inject_config_variables_into_templates 
# to inject global templates variables
app.context_processor(inject_config_variables_into_templates)



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


@app.route('/signup', methods=['POST'])
def signup():
    # get user data
    data = request.get_json()

    # save user data into variable
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # validate user data
    error = validate_signup_data(username, email, password)
    if error:
        return jsonify({'message': error}), 422  

    # check if user already exists
    user_collection = database.get_collection('users')

    # check if username or email already exists
    if user_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 422  

    # check if email already exists
    if user_collection.find_one({'email': {'$exists': True, '$eq': email}}):
        return jsonify({'message': 'Email already exists'}), 422  

    # hash password
    hashed_password = generate_password_hash(password)

    user_data = {
        'username': username,
        'email': email,
        'password_hash': hashed_password
    }

    # insert user data
    user_collection.insert_one(user_data)
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password') 
    
    # validate user data
    if not username or not password:
        return jsonify({'message': 'username and password are required'}), 422  
    
    # Get user data
    user_collection = database.get_collection('users')
    
    # Check if user exists
    user = user_collection.find_one({'username': username})
    
    if not user:
        return jsonify({'message': 'Invalid input '}), 401
    
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'message': 'Invalid input'}), 401
    
    return jsonify({'message': 'Sign in successful'}), 200


# 4xx error handling 
@app.errorhandler(404)
@app.errorhandler(405)
def code_4xx_handling(e):
    # error_code = e.code if hasattr(e, "code") else 500
    # return render_template("errorPages/4xxError.html", error_type=error_code), error_code

    error_messages = {
            404: "The page you are looking for does not exist.How you got here is a mystery.But you can click the button below to go back to the homepage.",
            405: "Method Not Allowed.The method is not allowed for the requested URL.",
    }

    # Get the status code from the error object
    error_code = e.code if hasattr(e, "code") else 500

    # Retrieve the error message based on the error code
    error_message = error_messages.get(
        error_code, "An unexpected error occurred. Please try again later."
    )

    return (
        render_template(
            "errorPages/404Error.html",
            error_type=str(error_code),
            error_message=error_message,
        ),
        error_code,
    )

# 5xx errors handling 
@app.errorhandler(500)
@app.errorhandler(502)
@app.errorhandler(503)
@app.errorhandler(504)
@app.errorhandler(505)
def code_5xx_handling(e):
    error_messages = {
        500: "Oops! Something went wrong on our end. We’re working to fix it. Please try again later.",
        502: "It looks like there’s an issue with our service. We’re investigating the problem and will have it fixed soon. Please try again in a few minutes.",
        503: "Our server is currently down for maintenance or experiencing high traffic. We’ll be back up soon. Please try again later.",
        504: "The server took too long to respond. We’re working on resolving the issue. Please try your request again in a few minutes.",
        505: "We’re unable to process your request due to an unsupported HTTP version. Please check your request and try again.",
    }

    # Get the status code from the error object
    error_code = e.code if hasattr(e, "code") else 500

    # Retrieve the error message based on the error code
    error_message = error_messages.get(
        error_code, "An unexpected error occurred. Please try again later."
    )

    return (
        render_template(
            "errorPages/5xxError.html",
            error_type=str(error_code),
            error_message=error_message,
        ),
        error_code,
    )

if __name__ == "__main__":
    app.run(debug=True)


