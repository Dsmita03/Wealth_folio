from flask import Flask, request, jsonify

app = Flask(__name__)

class GoalService:
    def __init__(self):
        self.goals = {}

    def set_goal(self, name, amount, deadline):
        self.goals[name] = {'amount': amount, 'deadline': deadline}
        return f"Goal {name} set with amount {amount} and deadline {deadline}"

    def get_goal(self, name):
        return self.goals.get(name, "No goal set with this name")

    def check_goal(self, name, current_amount):
        if name in self.goals:
            return current_amount >= self.goals[name]['amount']
        else:
            return False

goal_service = GoalService()

@app.route('/')
def index():
    return "Welcome to the Goal Service API!"


@app.route('/goals', methods=['POST'])
def set_goal():
    data = request.get_json()
    name = data['name']
    amount = data['amount']
    deadline = data['deadline']
    response = goal_service.set_goal(name, amount, deadline)
    return jsonify({"message": response}), 201

@app.route('/goals/<string:name>', methods=['GET'])
def get_goal(name):
    goal = goal_service.get_goal(name)
    if isinstance(goal, str):
        return jsonify({"error": goal}), 404
    return jsonify(goal), 200

@app.route('/goals/check', methods=['POST'])
def check_goal():
    data = request.get_json()
    name = data['name']
    current_amount = data['current_amount']
    result = goal_service.check_goal(name, current_amount)
    return jsonify({"goal_achieved": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
