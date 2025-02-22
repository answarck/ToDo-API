from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

db = SQLAlchemy(app)


SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", strict_slashes=False, methods=["GET"])
def redirect_swagger():
    return redirect("/swagger")

@app.route('/create', methods=['POST'], strict_slashes=False)
def create_todo():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    if not isinstance(data, dict) or "todo" not in data:
        return jsonify({"error": "Missing 'todo' field"}), 400

    todo_text = data["todo"].strip()
    if not todo_text or len(todo_text) > 255:
        return jsonify({"error": "Invalid 'todo': must be 1-255 characters"}), 400

    new_item = ToDo(todo=todo_text)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"id": new_item.id, "todo": new_item.todo}), 201

@app.route('/delete/<int:num>', methods=['DELETE'])
def delete_todo(num):
    todo = ToDo.query.get(num)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    db.session.delete(todo) 
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"}), 200

@app.route('/update/<int:num>', methods=['PUT'])
def update_todo(num):
    todo = ToDo.query.get(num)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404  

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json
    if not isinstance(data, dict) or "todo" not in data:
        return jsonify({"error": "Missing 'todo' field"}), 400

    todo_text = data["todo"].strip()
    if not todo_text or len(todo_text) > 255:
        return jsonify({"error": "Invalid 'todo': must be 1-255 characters"}), 400

    todo.todo = todo_text
    db.session.commit()
    return jsonify({"id": todo.id, "todo": todo.todo}), 200

@app.route('/list/<string:num>', methods=['GET']) 
def show_todo(num): 
    if num == "all":
        todos = ToDo.query.all()
        return jsonify({"todos": [{"id": todo.id, "todo": todo.todo} for todo in todos]})

    if not num.isdigit():
        return jsonify({"error": "Invalid ID format"}), 400

    todo = ToDo.query.get(int(num))
    if todo:
        return jsonify({"id": todo.id, "todo": todo.todo})
    return jsonify({"error": "Todo not found"}), 404

