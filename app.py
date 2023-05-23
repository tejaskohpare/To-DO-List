from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["todo_list_db"]
todos_collection = db["todos"]

# API endpoints
# Fetch all todos
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = list(todos_collection.find({}, {'_id': 0}))
    return jsonify({'todos': todos})



@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = list(todos_collection.find())
    return jsonify(todos)

@app.route("/api/todos", methods=["POST"])
def create_todo():
    new_todo = {
        "title": request.json["title"],
        "completed": False
    }
    todos_collection.insert_one(new_todo)
    return jsonify(new_todo)

@app.route("/api/todos/<id>", methods=["PUT"])
def update_todo(id):
    todo = todos_collection.find_one({"_id": id})
    todo["completed"] = not todo["completed"]
    todos_collection.update_one({"_id": id}, {"$set": todo})
    return jsonify(todo)

@app.route("/api/todos/<id>", methods=["DELETE"])
def delete_todo(id):
    todos_collection.delete_one({"_id": id})
    return jsonify({"message": "Todo deleted"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
