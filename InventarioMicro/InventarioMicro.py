# Microservicio para la gestión de inventario con GUI

import sqlite3
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)

# Creación de la base de datos de Habitaciones
def setup_rooms_db():
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
                        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_number INTEGER,
                        room_type TEXT,
                        status TEXT
                      )''')
    conn.commit()
    conn.close()

# Endpoint para registrar nuevas habitaciones
@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    room_number = data['room_number']
    room_type = data['room_type']
    status = data['status']

    # Insertar la nueva habitación en la base de datos
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO rooms (room_number, room_type, status)
                      VALUES (?, ?, ?)''', (room_number, room_type, status))
    conn.commit()
    conn.close()

    return jsonify({"message": "Room created successfully"}), 201

# Endpoint para actualizar el estado de una habitación
@app.route('/rooms/<int:room_id>', methods=['PATCH'])
def update_room_status(room_id):
    data = request.json
    status = data['status']

    # Actualizar el estado de la habitación en la base de datos
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE rooms SET status = ? WHERE room_id = ?''', (status, room_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Room status updated successfully"}), 200

# Interfaz gráfica (GUI) para gestionar el inventario
def launch_gui():
    def add_room():
        room_number = room_number_entry.get()
        room_type = room_type_entry.get()
        status = status_entry.get()

        if not (room_number and room_type and status):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect('rooms.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO rooms (room_number, room_type, status)
                          VALUES (?, ?, ?)''', (room_number, room_type, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Habitación registrada correctamente")
        room_number_entry.delete(0, tk.END)
        room_type_entry.delete(0, tk.END)
        status_entry.delete(0, tk.END)

    def update_status():
        room_id = room_id_entry.get()
        status = new_status_entry.get()

        if not (room_id and status):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect('rooms.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE rooms SET status = ? WHERE room_id = ?''', (status, room_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Estado de la habitación actualizado correctamente")
        room_id_entry.delete(0, tk.END)
        new_status_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Gestión de Inventario de Habitaciones")

    tk.Label(root, text="Número de Habitación").grid(row=0, column=0)
    room_number_entry = tk.Entry(root)
    room_number_entry.grid(row=0, column=1)

    tk.Label(root, text="Tipo de Habitación").grid(row=1, column=0)
    room_type_entry = tk.Entry(root)
    room_type_entry.grid(row=1, column=1)

    tk.Label(root, text="Estado").grid(row=2, column=0)
    status_entry = tk.Entry(root)
    status_entry.grid(row=2, column=1)

    tk.Button(root, text="Agregar Habitación", command=add_room).grid(row=3, column=0, columnspan=2)

    tk.Label(root, text="ID de Habitación").grid(row=4, column=0)
    room_id_entry = tk.Entry(root)
    room_id_entry.grid(row=4, column=1)

    tk.Label(root, text="Nuevo Estado").grid(row=5, column=0)
    new_status_entry = tk.Entry(root)
    new_status_entry.grid(row=5, column=1)

    tk.Button(root, text="Actualizar Estado", command=update_status).grid(row=6, column=0, columnspan=2)

    root.mainloop()

# Inicialización de la base de datos y ejecución del servidor o GUI
if __name__ == '__main__':
    setup_rooms_db()

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        launch_gui()
    else:
        app.run(debug=True, port=6000)
