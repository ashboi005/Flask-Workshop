from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)

# Secret key for session management (generated randomly)
app.secret_key = os.urandom(24)

# List of valid hobbies to prevent tampering
VALID_HOBBIES = ["Reading", "Sports", "Coding", "Music", "Traveling"]

# Route for the form and session handling
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect user details from the form
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        hobbies = request.form.getlist("hobbies")

        # Basic form validation
        if not name or not email or not age or not hobbies:
            flash("All fields, including hobbies, are required!", "error")
            return redirect(url_for('index'))

        if not age.isdigit():
            flash("Age must be a number!", "error")
            return redirect(url_for('index'))

        # Validate hobbies: ensure all selected hobbies are valid
        for hobby in hobbies:
            if hobby not in VALID_HOBBIES:
                flash("Invalid hobby selected!", "error")
                return redirect(url_for('index'))

        # Store user details and hobbies in the session
        session['user_details'] = {
            'name': name,
            'email': email,
            'age': age,
            'hobbies': hobbies
        }
        flash("Details added successfully!")
        return redirect(url_for('view_data'))

    return render_template("register.html", valid_hobbies=VALID_HOBBIES)

# Route to view the stored session data
@app.route("/view")
def view_data():
    # Fetch user details from the session
    user_details = session.get('user_details', None)
    # if user_details:
    #     print("Current Session Data:", user_details)
    # else:
    #     print("No session data found.")
    return render_template("view_data.html", user_details=user_details)

# Route to clear the session
@app.route("/delete_session")
def delete_session():
    session.pop('user_details', None)  # Clear session data
    flash("Session cleared!")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
