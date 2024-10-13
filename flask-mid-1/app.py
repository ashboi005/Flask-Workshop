from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dictionary to store data
data_store = {}

# Route to enter data
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        key = request.form.get("key")
        value = request.form.get("value")
        if key and value:
            data_store[key] = value
        return redirect(url_for('view_data'))
    return render_template("register.html")

# Route to view stored data
@app.route("/view")
def view_data():
    #print("Current Data Store:", data_store)
    return render_template("view_data.html", data_store=data_store)

# Route to delete specific data
@app.route("/delete/<key>")
def delete_data(key):
    if key in data_store:
        del data_store[key]
    return redirect(url_for('view_data'))

# About route to explain app
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
