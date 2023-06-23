from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://expenseuser:passwrd@localhost/expense_tracker"

# bind db object to app/ add db connectivity
db = SQLAlchemy(app)
CORS(app)

# db table: id, created at, description, amount, category
# migrate to PGAdmin
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    description = db.Column(db.String, nullable=True)
    amount = db.Column(db.Float, nullable=True)
    category = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"Expense: {self.description} {self.amount} {self.category}"
    
    def __init__(self, description, amount, category):
        self.description = description
        self.amount = amount
        self.category = category



@app.route("/expenses", methods=["POST"])
def create_expense():
    description = request.json["desciption"]
    amount = request.json["amount"]
    category = request.category["category"]

    # invoke __init__  when create instance of a class
    expense = Expense(description, amount, category)

    # create a record in the db, always commit
    db.session.add(expense)
    db.session.commit()

    created_expense = {
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category
    }

    return created_expense

@app.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    expense_list = []

    # for each expense created from the record, add to the list
    for expense in expenses:
        retrieved_expense = {
            "id": expense.id,
            "created_at": expense.created_at,
            "description": expense.description,
            "amount": expense.amount,
            "category": expense.category
        }
        expense_list.append(retrieved_expense)
    
    return expense_list







if __name__ == "__main__":
    app.run(debug=True)