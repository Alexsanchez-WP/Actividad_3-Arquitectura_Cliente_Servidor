from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulación de base de datos en memoria
tasks = {}
error_task = {'error': 'Tarea no encontrada'}


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Obtener todas las tareas."""
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtener una tarea específica por su ID.

    :param task_id: ID de la tarea a recuperar.
    """
    task = tasks.get(task_id)
    if task is None:
        return jsonify(error_task), 404
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
    """
    Modificar una tarea existente.

    :param task_id: ID de la tarea a modificar.    
    """
    if task_id not in tasks:
        return jsonify(error_task), 404
    task_data = request.json
    tasks[task_id] = task_data
    return jsonify({task_id: task_data})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Eliminar una tarea.

    :param task_id: ID de la tarea a eliminar.
    """
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Tarea eliminada'}), 200
    return jsonify(error_task), 404


if __name__ == "__main__":
    """Ejecutar el servidor."""
    app.run(debug=True)
