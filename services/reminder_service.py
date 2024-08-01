from flask import Flask, request, jsonify
import datetime

class ReminderService:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, title, description, date_time):
        """Add a new reminder."""
        reminder = {
            "title": title,
            "description": description,
            "date_time": date_time
        }
        self.reminders.append(reminder)
        return "Reminder added"

    def get_reminders(self):
        """Get a list of all reminders."""
        return self.reminders

    def get_reminders_by_date(self, date):
        """Get reminders for a specific date."""
        return [reminder for reminder in self.reminders if reminder['date_time'].date() == date.date()]

    def delete_reminder(self, title):
        """Delete a reminder by title."""
        initial_length = len(self.reminders)
        self.reminders = [reminder for reminder in self.reminders if reminder['title'] != title]
        if len(self.reminders) < initial_length:
            return "Reminder deleted"
        else:
            return "Reminder not found"

app = Flask(__name__)
reminder_service = ReminderService()

@app.route('/')
def index():
    return "Welcome to the Reminder Service API!"

@app.route('/reminders', methods=['POST'])
def add_reminder():
    data = request.get_json()
    title = data['title']
    description = data['description']
    date_time_str = data['date_time']
    try:
        date_time = datetime.datetime.fromisoformat(date_time_str)
    except ValueError:
        return jsonify({"error": "Invalid date_time format. Use ISO 8601 format."}), 400
    response = reminder_service.add_reminder(title, description, date_time)
    return jsonify({"message": response}), 201

@app.route('/reminders', methods=['GET'])
def get_reminders():
    return jsonify(reminder_service.get_reminders()), 200

@app.route('/reminders/date/<string:date>', methods=['GET'])
def get_reminders_by_date(date):
    try:
        date_obj = datetime.datetime.fromisoformat(date).date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO 8601 format."}), 400
    reminders = reminder_service.get_reminders_by_date(date_obj)
    return jsonify(reminders), 200

@app.route('/reminders/<string:title>', methods=['DELETE'])
def delete_reminder(title):
    response = reminder_service.delete_reminder(title)
    if response == "Reminder deleted":
        return jsonify({"message": response}), 200
    else:
        return jsonify({"error": response}), 404

if __name__ == '__main__':
    app.run(debug=True)
