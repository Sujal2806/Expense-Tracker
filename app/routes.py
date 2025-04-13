# backend/app/routes.py
from flask import request, jsonify, render_template
from . import create_app, db
from .models import Expense

app = create_app()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/expenses", methods=["GET", "POST"])
def manage_expenses():
    if request.method == "GET":
        expenses = Expense.query.all()
        return jsonify([
            {"id": e.id, "amount": e.amount, "category": e.category, "date": e.date}
            for e in expenses
        ])
    
    if request.method == "POST":
        data = request.json
        expense = Expense(
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"]
        )
        db.session.add(expense)
        db.session.commit()
        return jsonify({"message": "Expense added!"}), 201
    
@app.route("/expenses/<int:id>", methods=["PUT", "DELETE"])
def modify_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == "PUT":
        data = request.json
        expense.amount = float(data["amount"])
        expense.category = data["category"]
        expense.date = data["date"]
        db.session.commit()
        return jsonify({"message": "Expense updated!"})

    if request.method == "DELETE":
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted!"})
