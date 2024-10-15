from flask import Blueprint, request, jsonify, session
from flask_api_2.models import db, Project

project_bp = Blueprint('project', __name__)


# Create a new project
@project_bp.route('/create', methods=['POST'])
def create_project():
    data = request.get_json()

    # Ensure that the project_name is provided
    if not data or not data.get('project_name'):
        return jsonify({"error": "Project name is required"}), 400

    new_project = Project(name=data['project_name'], description=data.get('description', ''),
                          user_id=1)  # Assuming you're using user_id=1 for now
    db.session.add(new_project)
    db.session.commit()

    return jsonify(new_project.to_dict()), 201


# List all projects for the current user
@project_bp.route('/list', methods=['GET'])
def list_projects():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    projects = Project.query.filter_by(user_id=session['user_id']).all()
    return jsonify([project.to_dict() for project in projects]), 200


# Update an existing project
@project_bp.route('/update/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404

    data = request.get_json()
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)

    db.session.commit()
    return jsonify({'message': 'Project updated successfully'}), 200


# Delete a project
@project_bp.route('/delete/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    project = Project.query.filter_by(id=project_id, user_id=session['user_id']).first()
    if not project:
        return jsonify({'message': 'Project not found'}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200
