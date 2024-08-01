from flask import Flask, request, jsonify

app = Flask(__name__)

class ReceiptService:
    def __init__(self, id, items, total_amount, date):
        self.id = id
        self.items = items
        self.total_amount = total_amount
        self.date = date

    def get_receipt_details(self):
        return {
            "id": self.id,
            "items": self.items,
            "total_amount": self.total_amount,
            "date": self.date
        }

    def add_item(self, item, amount):
        self.items.append(item)
        self.total_amount += amount
        return f"Item {item} added with amount {amount}"

receipts = {}

@app.route('/')
def index():
    return "Welcome to the Receipt Service API!"

@app.route('/receipts', methods=['POST'])
def create_receipt():
    data = request.get_json()
    receipt_id = data['id']
    items = data['items']
    total_amount = data['total_amount']
    date = data['date']
    receipt = ReceiptService(receipt_id, items, total_amount, date)
    receipts[receipt_id] = receipt
    return jsonify({"message": "Receipt created"}), 201

@app.route('/receipts/<int:receipt_id>', methods=['GET'])
def get_receipt_details(receipt_id):
    receipt = receipts.get(receipt_id)
    if receipt:
        return jsonify(receipt.get_receipt_details()), 200
    else:
        return jsonify({"error": "Receipt not found"}), 404

@app.route('/receipts/<int:receipt_id>/items', methods=['POST'])
def add_item_to_receipt(receipt_id):
    data = request.get_json()
    item = data['item']
    amount = data['amount']
    receipt = receipts.get(receipt_id)
    if receipt:
        message = receipt.add_item(item, amount)
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": "Receipt not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
