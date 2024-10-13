from flask import Flask, render_template, redirect, url_for, flash
from forms import RegistrationForm  # Import the form class

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process the form data
        name = form.name.data
        email = form.email.data
        flash(f'Registration successful for {name}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
