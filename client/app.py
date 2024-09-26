import os

import streamlit as st
import requests
import dotenv

dotenv.load_dotenv()

# URL del servidor de la API, se trae desde el archivo .env
api_server_url = os.environ.get("SERVER_API_URL")


def get_tasks():
    """Obtener todas las tareas desde el servidor."""
    response = requests.get(api_server_url)
    return response.json()


def create_task(task_data):
    """
    Crear una nueva tarea en el servidor.

    :param task_data: Datos de la tarea a crear.
    """
    response = requests.post(api_server_url, json=task_data)
    return response.json()


def update_task(task_id, task_data):
    """
    Actualizar una tarea existente en el servidor.

    :param task_id: ID de la tarea a actualizar.
    :param task_data: Datos de la tarea actualizada.
    """
    response = requests.put(f"{api_server_url}/{task_id}", json=task_data)
    return response.json()


def delete_task(task_id):
    """
    Eliminar una tarea del servidor.

    :param task_id: ID de la tarea a eliminar.
    """
    response = requests.delete(f"{api_server_url}/{task_id}")
    return response.json()


###### Interfaz de usuario con Streamlit ######

# Título de la aplicación
st.title("Task Manager")

# Obtener y mostrar todas las tareas
st.subheader("Tareas")
tasks = get_tasks()
for task_id, task in tasks.items():
    st.write(f"ID: {task_id}, Tarea: {task.get(
        "title")} - {task.get("description")}")

# Crear nueva tarea
st.subheader("Crear nueva tarea")
task_name = st.text_input("Nombre de la tarea", )
task_description = st.text_input("Descripción de la tarea")
if st.button("Agregar tarea"):
    if task_name == "":
        st.error("Error al crear la tarea")
    else:
        new_task = {"title": task_name, "description": task_description}
        result = create_task(new_task)
        st.success(f"Tarea creada: {result}")

# Actualizar tarea
st.subheader("Actualizar tarea")
task_id_to_update = st.number_input("ID de la tarea a actualizar", min_value=1)
updated_task_name = st.text_input("Nuevo nombre de la tarea")
update_task_description = st.text_input("Nueva descripción de la tarea")
if st.button("Actualizar tarea"):
    if updated_task_name == "":
        st.error("Error al actualizar la tarea")
    else:
        updated_task = {
            "title": updated_task_name,
            "description": update_task_description}
        result = update_task(task_id_to_update, updated_task)
        if "error" in result:
            st.error(f"Error al actualizar la tarea: {result['error']}")
        else:
            st.success(f"Tarea actualizada: {result}")

# Eliminar tarea
st.subheader("Eliminar tarea")
task_id_to_delete = st.number_input("ID de la tarea a eliminar", min_value=1)
if st.button("Eliminar tarea"):
    result = delete_task(task_id_to_delete)
    st.success(f"Tarea eliminada: {result}")
