from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/create', methods=['POST'])
def create_todo():
    data = request.json
    new_item = ToDo(todo=data['todo'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"id": new_item.id, "todo": new_item.todo})

@app.route('/delete/<int:num>', methods=['DELETE'])
def delete_todo(num):
    todo = ToDo.query.get(num)
    if todo:
        db.session.delete(todo)  # Corrected delete operation
        db.session.commit()
        return jsonify({"message": "Todo deleted successfully"})
    return jsonify({"error": "Todo not found"}), 404

@app.route('/update/<int:num>', methods=['PUT'])
def update_todo(num):
    todo = ToDo.query.get(num)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404  
    data = request.json
    if "todo" in data:
        todo.todo = data["todo"]
        db.session.commit()
        return jsonify({"id": todo.id, "todo": todo.todo})
    return jsonify({"error": "Invalid request"}), 400  

@app.route('/list/<int:num>', methods=['GET']) 
def show_todo(num): 
    todo = ToDo.query.get(num)
    if todo:
        return jsonify({"id": todo.id, "todo": todo.todo})
    return jsonify({"error": "Todo not found"}), 404

if __name__ == '__main__': 
    app.run(debug=True)
