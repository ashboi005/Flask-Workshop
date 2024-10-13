from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")  #removed the world here to implement the logic in html instead
        return render_template("greet.html", name=name)
    return render_template("register.html", name="")

if __name__ == "__main__":
    app.run(debug=True)
