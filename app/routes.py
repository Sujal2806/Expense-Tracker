# backend/app/routes.py
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from .models import Expense, db

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    return render_template("index.html")

@main.route("/expenses", methods=["GET", "POST"])
@login_required
def manage_expenses():
    try:
        if request.method == "GET":
            expenses = Expense.query.filter_by(user_id=current_user.id).all()
            return jsonify([
                {"id": e.id, "amount": e.amount, "category": e.category, "date": e.date}
                for e in expenses
            ])
        
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            if not all(k in data for k in ["amount", "category", "date"]):
                return jsonify({"error": "Missing required fields"}), 400
                
            try:
                amount = float(data["amount"])
                if amount <= 0:
                    return jsonify({"error": "Amount must be positive"}), 400
            except ValueError:
                return jsonify({"error": "Invalid amount"}), 400

            expense = Expense(
                amount=amount,
                category=data["category"],
                date=data["date"],
                user_id=current_user.id
            )
            db.session.add(expense)
            db.session.commit()
            return jsonify({
                "message": "Expense added!",
                "expense": {
                    "id": expense.id,
                    "amount": expense.amount,
                    "category": expense.category,
                    "date": expense.date
                }
            }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@main.route("/expenses/<int:id>", methods=["PUT", "DELETE"])
@login_required
def modify_expense(id):
    try:
        expense = Expense.query.filter_by(id=id, user_id=current_user.id).first_or_404()

        if request.method == "PUT":
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            if not all(k in data for k in ["amount", "category", "date"]):
                return jsonify({"error": "Missing required fields"}), 400
                
            try:
                amount = float(data["amount"])
                if amount <= 0:
                    return jsonify({"error": "Amount must be positive"}), 400
            except ValueError:
                return jsonify({"error": "Invalid amount"}), 400

            expense.amount = amount
            expense.category = data["category"]
            expense.date = data["date"]
            db.session.commit()
            return jsonify({
                "message": "Expense updated!",
                "expense": {
                    "id": expense.id,
                    "amount": expense.amount,
                    "category": expense.category,
                    "date": expense.date
                }
            })

        if request.method == "DELETE":
            db.session.delete(expense)
            db.session.commit()
            return jsonify({"message": "Expense deleted!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
