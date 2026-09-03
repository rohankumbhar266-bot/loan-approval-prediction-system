from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# ---------------- DATA + ML ----------------

df = pd.read_csv(
    "loan_approval_dataset.csv",
    encoding="utf-16",
    sep="\t"
)

df.columns = df.columns.str.strip()

df["education"] = df["education"].str.strip().map({
    "Graduate": 1,
    "Not Graduate": 0
})

df["self_employed"] = df["self_employed"].str.strip().map({
    "Yes": 1,
    "No": 0
})

df["loan_status"] = df["loan_status"].str.strip().map({
    "Approved": 1,
    "Rejected": 0
})

features = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value"
]

X = df[features]
y = df["loan_status"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PREDICT ----------------

@app.route("/predict", methods=["POST"])
def predict():

    education = 1 if request.form["education"] == "Graduate" else 0
    self_employed = 1 if request.form["self_employed"] == "Yes" else 0

    values = [
        int(request.form["dependents"]),
        education,
        self_employed,
        int(request.form["income"]),
        int(request.form["loan_amount"]),
        int(request.form["loan_term"]),
        int(request.form["cibil_score"]),
        int(request.form["residential_assets"]),
        int(request.form["commercial_assets"]),
        int(request.form["luxury_assets"]),
        int(request.form["bank_assets"])
    ]

    prediction = model.predict([values])[0]

    result = "LOAN APPROVED" if prediction == 1 else "LOAN REJECTED"


    # ---------------- MYSQL ----------------

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="prathuu",
        database="loan_approval"
    )

    cursor = db.cursor()

    sql = """
    INSERT INTO loan_predictions
    (
        no_of_dependents,
        education,
        self_employed,
        income_annum,
        loan_amount,
        loan_term,
        cibil_score,
        residential_assets_value,
        commercial_assets_value,
        luxury_assets_value,
        bank_asset_value,
        prediction
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = (
        values[0],
        request.form["education"],
        request.form["self_employed"],
        values[3],
        values[4],
        values[5],
        values[6],
        values[7],
        values[8],
        values[9],
        values[10],
        result
    )

    cursor.execute(sql, data)
    db.commit()

    cursor.close()
    db.close()

    return render_template("index.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True)