from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register")
@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/dashboard")
@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

@app.route("/data")
@app.route("/data.html")
def data():
    return render_template("data.html")

@app.route("/prediction")
@app.route("/index.html")
def prediction():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    prediction = "Loan Approved"
    return render_template("index.html", prediction=prediction)

@app.route("/analytics")
@app.route("/analytics.html")
def analytics():
    return render_template("analytics.html")

@app.route("/visualization")
@app.route("/visualization.html")
def visualization():
    return render_template("visualization.html")

@app.route("/reports")
@app.route("/reports.html")
def reports():
    return render_template("reports.html")

@app.route("/history")
@app.route("/history.html")
def history():
    return render_template("history.html")

@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)