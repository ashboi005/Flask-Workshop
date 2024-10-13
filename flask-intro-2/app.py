from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("unsafe_index.html")

@app.route("/greet")
def greet():
    # Retrieve the name from the query parameters in the URL
    name = request.args.get("name", "World")
    return render_template("greet.html", name=name)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # Retrieve the name entered in the form
#         name = request.form.get("name", "World")
#         return render_template("greet.html", name=name)
#     return render_template("register.html", name="")

if __name__ == "__main__":
    app.run(debug=True)
