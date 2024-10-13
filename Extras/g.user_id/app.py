from flask import Flask, g, session

app = Flask(__name__)

# Simulated user data
users = {'1': 'Alice', '2': 'Bob'}

# Before request handler to load user data into `g`
@app.before_request
def load_user():
    # Let's assume we are retrieving user_id from the session or a token
    user_id = session.get('user_id')  # You might retrieve this from a session or authentication token
    if user_id:
        g.user_id = user_id  # Store it in `g`
        g.user_name = users.get(user_id)  # Optionally store more data

@app.route('/profile')
def profile():
    # Access user_id and user_name from `g`
    if hasattr(g, 'user_id'):
        return f"User ID: {g.user_id}, User Name: {g.user_name}"
    else:
        return "No user logged in."

if __name__ == "__main__":
    app.run(debug=True)
