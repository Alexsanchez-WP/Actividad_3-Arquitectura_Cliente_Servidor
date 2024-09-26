import os
import requests

import dotenv

dotenv.load_dotenv()

# URL del servidor de la API, se trae desde el archivo .env
api_server_url = os.environ.get("SERVER_API_URL")


def show_menu():
    """Muestra el menú principal de opciones en la consola."""
    print("\nGestión de Tareas")
    print("1. Ver todas las tareas")
    print("2. Ver una tarea específica")
    print("3. Crear una nueva tarea")
    print("4. Modificar una tarea existente")
    print("5. Borrar una tarea")
    print("6. Salir")


def get_tasks():
    """Solicita y muestra todas las tareas del servidor."""
    try:
        response = requests.get(api_server_url)
        tasks = response.json()
        print("\nTareas:")
        for id, task in tasks.items():
            print(f"{id}: {task}")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")


def get_task():
    """Solicita y muestra una tarea específica por su ID."""
    task_id = input("Ingrese el ID de la tarea: ")
    try:
        response = requests.get(f"{api_server_url}/{task_id}")
        if response.status_code == 200:
            task = response.json()
            print(f"\nTarea {task_id}: {task}")
        else:
            print("Tarea no encontrada.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")


def create_task():
    """Crea una nueva tarea en el servidor."""
    title = input("Título de la tarea: ")
    description = input("Descripción de la tarea: ")
    task = {"title": title, "description": description}
    try:
        response = requests.post(api_server_url, json=task)
        print("Tarea creada:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")


def update_task():
    """Modifica una tarea existente en el servidor."""
    task_id = input("Ingrese el ID de la tarea a modificar: ")
    title = input("Nuevo título de la tarea: ")
    description = input("Nueva descripción de la tarea: ")
    task = {"title": title, "description": description}
    try:
        response = requests.put(f"{api_server_url}/{task_id}", json=task)
        if response.status_code == 200:
            print("Tarea actualizada:", response.json())
        else:
            print("Tarea no encontrada.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")


def delete_task():
    """Elimina una tarea existente en el servidor."""
    task_id = input("Ingrese el ID de la tarea a eliminar: ")
    try:
        response = requests.delete(f"{api_server_url}/{task_id}")
        if response.status_code == 200:
            print("Tarea eliminada.")
        else:
            print("Tarea no encontrada.")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Seleccione una opción: ")

        if choice == '1':
            get_tasks()
        elif choice == '2':
            get_task()
        elif choice == '3':
            create_task()
        elif choice == '4':
            update_task()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            break
        else:
            print("Opción no válida.")
