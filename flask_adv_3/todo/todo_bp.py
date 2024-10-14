from flask import render_template, redirect, url_for, request, flash, session
from flask_adv_3.models import db, Todo

from flask import Blueprint
todo_bp = Blueprint('todo', __name__)

# To-Do List Route (Create, View To-Dos)
@todo_bp.route('/todo', methods=['GET', 'POST'])
def todo_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))

    user_id = session['user_id']

    if request.method == 'POST':
        task = request.form['task']
        description = request.form.get('description', '')
        deadline = request.form.get('deadline', '')
        new_todo = Todo(task=task, description=description, deadline=deadline, user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()
        flash('Task added!', 'success')

    todos = Todo.query.filter_by(user_id=user_id).all()
    return render_template('todo.html', todos=todos)

# Mark Task as Completed
@todo_bp.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = True
    db.session.commit()
    flash('Task marked as completed!', 'success')
    return redirect(url_for('todo.todo_list'))

# Edit To-Do
@todo_bp.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == 'POST':
        todo.task = request.form['task']
        todo.description = request.form['description']
        todo.deadline = request.form['deadline']
        db.session.commit()
        flash('Task updated!', 'success')
        return redirect(url_for('todo.todo_list'))

    return render_template('edit_todo.html', todo=todo)

# Delete To-Do
@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('todo.todo_list'))
