from flask import Flask, request, jsonify

app = Flask(__name__)

class BudgetService:
    def __init__(self):
        self.budgets = {}

    def set_budget(self, category, amount):
        self.budgets[category] = amount
        return f"Budget for {category} set to {amount}"

    def get_budget(self, category):
        return self.budgets.get(category, "No budget set for this category")

    def check_budget(self, category, amount_spent):
        if category in self.budgets:
            return amount_spent <= self.budgets[category]
        else:
            return False

budget_service = BudgetService()

@app.route('/')
def index():
    return "Welcome to the Budget Service API!"

@app.route('/budgets', methods=['POST'])
def set_budget():
    data = request.get_json()
    category = data['category']
    amount = data['amount']
    response = budget_service.set_budget(category, amount)
    return jsonify({"message": response}), 201

@app.route('/budgets/<string:category>', methods=['GET'])
def get_budget(category):
    budget = budget_service.get_budget(category)
    if isinstance(budget, str):
        return jsonify({"error": budget}), 404
    return jsonify({"amount": budget}), 200

@app.route('/budgets/check', methods=['POST'])
def check_budget():
    data = request.get_json()
    category = data['category']
    amount_spent = data['amount_spent']
    result = budget_service.check_budget(category, amount_spent)
    return jsonify({"within_budget": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
