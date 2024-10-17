from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_adv_3.models import db, User
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Index route (Login)
@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and verify password
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('todo.todo_list'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('auth.index'))

    # If the user is logged in, redirect to the to-do list
    if 'user_id' in session:
        return redirect(url_for('todo.todo_list'))

    # Otherwise, render the login page
    return render_template('index.html')


# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password and create new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.index'))

    return render_template('register.html')

# Logout Route
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('auth.index'))
