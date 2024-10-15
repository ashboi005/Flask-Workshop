from flask import Blueprint, request, jsonify, session
from flask_api_2.models import db, Task, Project

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/<int:project_id>/add', methods=['POST'])
def add_task(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    task_name = data.get('task_name')
    description = data.get('description')

    # Check if the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    new_task = Task(task_name=task_name, description=description, project_id=project.id)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task added successfully'}), 201



@task_bp.route('/<int:project_id>/list', methods=['GET'])
def list_tasks(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    # Ensure the project belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    tasks = Task.query.filter_by(project_id=project_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@task_bp.route('/<int:project_id>/update/<int:task_id>', methods=['PUT'])
def update_task(project_id, task_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    # Check if the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    task = Task.query.filter_by(id=task_id, project_id=project_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()
    task.task_name = data.get('task_name', task.task_name)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return jsonify(task.to_dict()), 200


@task_bp.route('/<int:project_id>/delete/<int:task_id>', methods=['DELETE'])
def delete_task(project_id, task_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    # Ensure the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    task = Task.query.filter_by(id=task_id, project_id=project_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@task_bp.route('/<int:project_id>/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(project_id, task_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    # Ensure the project exists and belongs to the user
    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found or unauthorized'}), 404

    task = Task.query.filter_by(id=task_id, project_id=project_id).first()
    if not task:
        return jsonify({'message': 'Task not found'}), 404

    task.completed = True
    db.session.commit()
    return jsonify({'message': 'Task marked as completed'}), 200
