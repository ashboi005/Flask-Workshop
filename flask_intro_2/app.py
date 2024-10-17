from flask import Flask, render_template, request

app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("unsafe_index.html")
#
# @app.route("/greet")
# def greet():
#     # gets the name from the query parameters in the URL
#     name = request.args.get("name", "World")
#     return render_template("greet.html", name=name)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # gets the name entered in the form by the user
        name = request.form.get("name")
        return render_template("greet.html", name=name)
    return render_template("index.html", name="")

if __name__ == "__main__":
    app.run(debug=True)
