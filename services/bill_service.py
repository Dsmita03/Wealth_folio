from flask import Flask, request, jsonify
import datetime

class BillService:
    def __init__(self):
        self.bills = []

    def add_bill(self, name, amount, due_date):
        bill = {
            "name": name,
            "amount": amount,
            "due_date": due_date
        }
        self.bills.append(bill)
        return "Bill added"

    def get_bills(self):
        return self.bills

    def get_bill_by_name(self, name):
        for bill in self.bills:
            if bill['name'] == name:
                return bill
        return "Bill not found"

    def delete_bill(self, name):
        initial_length = len(self.bills)
        self.bills = [bill for bill in self.bills if bill['name'] != name]
        if len(self.bills) < initial_length:
            return "Bill deleted"
        else:
            return "Bill not found"

app = Flask(__name__)
bill_service = BillService()

@app.route('/')
def index():
    return "Welcome to the Bill Service API!"

@app.route('/bills', methods=['POST'])
def add_bill():
    data = request.get_json()
    name = data['name']
    amount = data['amount']
    due_date_str = data['due_date']
    try:
        due_date = datetime.datetime.fromisoformat(due_date_str)
    except ValueError:
        return jsonify({"error": "Invalid due_date format. Use ISO 8601 format."}), 400
    response = bill_service.add_bill(name, amount, due_date)
    return jsonify({"message": response}), 201

@app.route('/bills', methods=['GET'])
def get_bills():
    return jsonify(bill_service.get_bills()), 200

@app.route('/bills/<string:name>', methods=['GET'])
def get_bill_by_name(name):
    bill = bill_service.get_bill_by_name(name)
    if bill == "Bill not found":
        return jsonify({"error": bill}), 404
    return jsonify(bill), 200

@app.route('/bills/<string:name>', methods=['DELETE'])
def delete_bill(name):
    response = bill_service.delete_bill(name)
    if response == "Bill deleted":
        return jsonify({"message": response}), 200
    else:
        return jsonify({"error": response}), 404

if __name__ == '__main__':
    app.run(debug=True)
