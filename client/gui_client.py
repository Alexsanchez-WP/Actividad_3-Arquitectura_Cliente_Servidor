import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

# URL de la API donde se encuentran las tareas
API_URL = "http://127.0.0.1:5000/tasks"

class TaskManagerApp:
    def __init__(self, root):
        """Inicializa la aplicación de gestión de tareas."""
        self.root = root
        self.root.title("Gestión de Tareas")
        self.root.geometry("400x300")  # Tamaño de la ventana

        self.create_widgets()  # Crea los botones y widgets

    def create_widgets(self):
        """Crea los botones de la interfaz gráfica."""
        # Cada botón está asociado a una función específica
        tk.Button(self.root, text="Ver todas las tareas", command=self.get_tasks).pack(fill='x', pady=5)
        tk.Button(self.root, text="Ver una tarea específica", command=self.get_task).pack(fill='x', pady=5)
        tk.Button(self.root, text="Crear una nueva tarea", command=self.create_task).pack(fill='x', pady=5)
        tk.Button(self.root, text="Modificar una tarea existente", command=self.update_task).pack(fill='x', pady=5)
        tk.Button(self.root, text="Borrar una tarea", command=self.delete_task).pack(fill='x', pady=5)
        tk.Button(self.root, text="Salir", command=self.root.quit).pack(fill='x', pady=5)

    def get_tasks(self):
        """Recupera y muestra todas las tareas desde el servidor."""
        try:
            response = requests.get(API_URL)
            tasks = response.json()
            # Formatea las tareas para mostrarlas en una ventana emergente
            task_list = "\n".join([f"ID {id}: {task['title']} - {task['description']}" for id, task in tasks.items()])
            messagebox.showinfo("Todas las Tareas", task_list or "No hay tareas disponibles.")
        except requests.exceptions.RequestException as e:
            # Muestra un error si no se puede conectar al servidor
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def get_task(self):
        """Recupera y muestra una tarea específica por su ID."""
        task_id = simpledialog.askstring("Obtener Tarea", "Ingrese el ID de la tarea:")
        if task_id:
            try:
                response = requests.get(f"{API_URL}/{task_id}")
                if response.status_code == 200:
                    task = response.json()
                    # Muestra el título y la descripción de la tarea en una ventana emergente
                    messagebox.showinfo(f"Tarea {task_id}", f"Título: {task['title']}\nDescripción: {task['description']}")
                else:
                    messagebox.showerror("Error", "Tarea no encontrada.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def create_task(self):
        """Crea una nueva tarea en el servidor."""
        title = simpledialog.askstring("Crear Tarea", "Título de la tarea:")
        description = simpledialog.askstring("Crear Tarea", "Descripción de la tarea:")
        if title and description:
            task = {"title": title, "description": description}
            try:
                response = requests.post(API_URL, json=task)
                # Muestra un mensaje de éxito al crear la tarea
                messagebox.showinfo("Tarea Creada", f"Tarea creada con éxito: {response.json()}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def update_task(self):
        """Modifica una tarea existente en el servidor."""
        task_id = simpledialog.askstring("Modificar Tarea", "Ingrese el ID de la tarea a modificar:")
        if task_id:
            title = simpledialog.askstring("Modificar Tarea", "Nuevo título de la tarea:")
            description = simpledialog.askstring("Modificar Tarea", "Nueva descripción de la tarea:")
            if title and description:
                task = {"title": title, "description": description}
                try:
                    response = requests.put(f"{API_URL}/{task_id}", json=task)
                    if response.status_code == 200:
                        messagebox.showinfo("Tarea Modificada", f"Tarea actualizada: {response.json()}")
                    else:
                        messagebox.showerror("Error", "Tarea no encontrada.")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def delete_task(self):
        """Elimina una tarea en el servidor."""
        task_id = simpledialog.askstring("Borrar Tarea", "Ingrese el ID de la tarea a eliminar:")
        if task_id:
            try:
                response = requests.delete(f"{API_URL}/{task_id}")
                if response.status_code == 200:
                    messagebox.showinfo("Tarea Eliminada", "Tarea eliminada con éxito.")
                else:
                    messagebox.showerror("Error", "Tarea no encontrada.")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

if __name__ == "__main__":
    # Inicializa la aplicación de Tkinter y ejecuta el bucle principal
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
