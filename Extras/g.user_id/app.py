import supabase
from flask import Flask, request, g

app = Flask(__name__)

# Initialize Supabase client
supabase_url = "https://your-supabase-url"
supabase_key = "your-supabase-api-key"
supabase_client = supabase.create_client(supabase_url, supabase_key)


@app.before_request
def authenticate_user():
    # Assume token is sent in the Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]  # "Bearer <token>"

        # Verify token with Supabase
        user_info = supabase_client.auth.api.get_user(token)
        if user_info:
            g.user_id = user_info.id
            g.email = user_info.email
        else:
            g.user_id = None
    else:
        g.user_id = None


@app.route('/profile')
def profile():
    if hasattr(g, 'user_id') and g.user_id:
        return f"User ID: {g.user_id}, Email: {g.email}"
    else:
        return "No user authenticated."


if __name__ == "__main__":
    app.run(debug=True)
