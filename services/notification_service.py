from flask import Flask, request, jsonify

app = Flask(__name__)

class NotificationService:
    def __init__(self):
        self.notifications = []

    def add_notification(self, message):
        self.notifications.append(message)
        return "Notification added"

    def get_notifications(self):
        return self.notifications

    def clear_notifications(self):
        self.notifications = []
        return "Notifications cleared"

notification_service = NotificationService()

@app.route('/')
def index():
    return "Welcome to the Notification Service API!"

@app.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    message = data['message']
    response = notification_service.add_notification(message)
    return jsonify({"message": response}), 201

@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = notification_service.get_notifications()
    return jsonify(notifications), 200

@app.route('/notifications/clear', methods=['POST'])
def clear_notifications():
    response = notification_service.clear_notifications()
    return jsonify({"message": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
