from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulación de base de datos en memoria
tasks = {}

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas."""
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtener una tarea específica por su ID."""
    task = tasks.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Crear una nueva tarea."""
    new_id = len(tasks) + 1
    task_data = request.json
    tasks[new_id] = task_data
    return jsonify({new_id: task_data}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Modificar una tarea existente."""
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    task_data = request.json
    tasks[task_id] = task_data
    return jsonify({task_id: task_data})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar una tarea."""
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Task deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)
