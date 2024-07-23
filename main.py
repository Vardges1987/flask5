from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from uuid import uuid4
from typing import List, Optional

app = Flask(__name__)


class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool


class CreateTask(BaseModel):
    title: str
    description: str
    completed: Optional[bool] = False


class UpdateTask(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]


tasks = []


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404


@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        task_data = CreateTask(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    task = Task(id=str(uuid4()), **task_data.dict())
    tasks.append(task.dict())
    return jsonify(task.dict()), 201


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    try:
        task_data = UpdateTask(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    task.update(task_data.dict(exclude_unset=True))
    return jsonify(task), 200


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
