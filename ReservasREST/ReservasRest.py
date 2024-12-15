# API REST para la gestión de reservas con GUI

import sqlite3
from flask import Flask, request, jsonify
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)

# Creación de la base de datos de Reservas
def setup_reservations_db():
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        room_number INTEGER,
                        customer_name TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        status TEXT
                      )''')
    conn.commit()
    conn.close()

# Endpoint para crear reservas
@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    room_number = data['room_number']
    customer_name = data['customer_name']
    start_date = data['start_date']
    end_date = data['end_date']
    status = 'Confirmed'

    # Crear la reserva en la base de datos
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO reservations (room_number, customer_name, start_date, end_date, status)
                      VALUES (?, ?, ?, ?, ?)''', (room_number, customer_name, start_date, end_date, status))
    conn.commit()
    conn.close()

    return jsonify({"message": "Reservation created successfully"}), 201

# Endpoint para consultar una reserva
@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM reservations WHERE reservation_id = ?''', (reservation_id,))
    reservation = cursor.fetchone()
    conn.close()

    if not reservation:
        return jsonify({"error": "Reservation not found"}), 404

    reservation_data = {
        "reservation_id": reservation[0],
        "room_number": reservation[1],
        "customer_name": reservation[2],
        "start_date": reservation[3],
        "end_date": reservation[4],
        "status": reservation[5]
    }

    return jsonify(reservation_data)

# Endpoint para cancelar una reserva
@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    conn = sqlite3.connect('reservations.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM reservations WHERE reservation_id = ?''', (reservation_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Reservation cancelled successfully"}), 200

# Interfaz gráfica (GUI) para gestionar reservas
def launch_gui():
    def create_reservation_gui():
        room_number = room_number_entry.get()
        customer_name = customer_name_entry.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if not (room_number and customer_name and start_date and end_date):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect('reservations.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO reservations (room_number, customer_name, start_date, end_date, status)
                          VALUES (?, ?, ?, ?, 'Confirmed')''', (room_number, customer_name, start_date, end_date))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Reserva creada correctamente")
        room_number_entry.delete(0, tk.END)
        customer_name_entry.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)

    def cancel_reservation_gui():
        reservation_id = reservation_id_entry.get()

        if not reservation_id:
            messagebox.showerror("Error", "El campo ID de reserva es obligatorio")
            return

        conn = sqlite3.connect('reservations.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM reservations WHERE reservation_id = ?''', (reservation_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
        reservation_id_entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Gestión de Reservas")

    tk.Label(root, text="Número de Habitación").grid(row=0, column=0)
    room_number_entry = tk.Entry(root)
    room_number_entry.grid(row=0, column=1)

    tk.Label(root, text="Nombre del Cliente").grid(row=1, column=0)
    customer_name_entry = tk.Entry(root)
    customer_name_entry.grid(row=1, column=1)

    tk.Label(root, text="Fecha de Inicio (YYYY-MM-DD)").grid(row=2, column=0)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=2, column=1)

    tk.Label(root, text="Fecha de Fin (YYYY-MM-DD)").grid(row=3, column=0)
    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=3, column=1)

    tk.Button(root, text="Crear Reserva", command=create_reservation_gui).grid(row=4, column=0, columnspan=2)

    tk.Label(root, text="ID de Reserva").grid(row=5, column=0)
    reservation_id_entry = tk.Entry(root)
    reservation_id_entry.grid(row=5, column=1)

    tk.Button(root, text="Cancelar Reserva", command=cancel_reservation_gui).grid(row=6, column=0, columnspan=2)

    root.mainloop()

# Inicialización de la base de datos y ejecución del servidor o GUI
if __name__ == '__main__':
    setup_reservations_db()

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        launch_gui()
    else:
        app.run(debug=True, port=5000)
