from flask import Flask, request, jsonify

app = Flask(__name__)

class TransactionService:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, amount, category, date):
        self.transactions.append({"amount": amount, "category": category, "date": date})
        return "Transaction added"

    def get_transactions(self):
        return self.transactions

    def get_transactions_by_category(self, category):
        return [transaction for transaction in self.transactions if transaction['category'] == category]

transaction_service = TransactionService()


@app.route('/')
def index():
    return "Welcome to the Transaction Service API!"

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    amount = data['amount']
    category = data['category']
    date = data['date']
    message = transaction_service.add_transaction(amount, category, date)
    return jsonify({"message": message}), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = transaction_service.get_transactions()
    return jsonify(transactions), 200

@app.route('/transactions/category/<string:category>', methods=['GET'])
def get_transactions_by_category(category):
    transactions = transaction_service.get_transactions_by_category(category)
    return jsonify(transactions), 200

if __name__ == '__main__':
    app.run(debug=True)
