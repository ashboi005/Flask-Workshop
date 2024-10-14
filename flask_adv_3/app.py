from flask import Flask
from auth.auth_bp import auth_bp
from todo.todo_bp import todo_bp
from config import init_app, db

app = Flask(__name__)


# Initialize the database with the Flask app
init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(todo_bp)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
