import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_api_2.auth_bp.auth_bp import auth_bp
from flask_api_2.task_bp.task_bp import task_bp
from flask_api_2.project_bp.project_bp import project_bp
from flask_api_2.models import db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db') #we hard code a fallback value otherwise can use just DATABASE_URL too
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))

# Initialize the database with the Flask app
db.init_app(app)

# Enable CORS if needed (optional)
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp , url_prefix = '/task')
app.register_blueprint(project_bp , url_prefix='/projects')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
