import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory data store for the backend API
tasks = [{"id": 1, "title": "Learn DevSecOps", "completed": False}]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({"error": "Title is required and cannot be empty"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'].strip(),
        "completed": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    task['title'] = data.get('title', task['title']).strip()
    task['completed'] = data.get('completed', task['completed'])
    return jsonify(task), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
        
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"message": "Task deleted successfully"}), 200

if __name__ == "__main__":
    # 1. Pull debug state from an environment variable (Defaults to False if not set)
    is_debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")
    
    # 2. Use '# nosec B104' to override Bandit's warning on binding to 0.0.0.0
    app.run(host="0.0.0.0", port=5000, debug=is_debug)  # nosec B104
