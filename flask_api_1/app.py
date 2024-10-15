import os

from flask import Flask, request, jsonify
from models import db, Todo
from flask_cors import CORS

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize the database with the Flask app
db.init_app(app)

#CORS (Cross-Origin Resource Sharing)
#pip install flask-cors
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})



# Create the database tables
with app.app_context():
    db.create_all()

# API Routes
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todo', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(task=data['task'], description=data.get('description'))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201

@app.route('/api/todo/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.task = data.get('task', todo.task)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/api/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
