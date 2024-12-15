# Servicio SOAP para consultar disponibilidad con GUI

import sqlite3
from spyne import Application, rpc, ServiceBase, Date, Unicode, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import tkinter as tk
from tkinter import messagebox

# Creación de la base de datos de Disponibilidad
def setup_availability_db():
    conn = sqlite3.connect('availability.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS availability (
                        room_id INTEGER PRIMARY KEY,
                        room_type TEXT,
                        available_date TEXT,
                        status TEXT
                      )''')
    conn.commit()
    conn.close()

# Servicio SOAP para consultar disponibilidad
class AvailabilityService(ServiceBase):
    @rpc(Date, Date, Unicode, _returns=Array(Unicode))
    def check_availability(ctx, start_date, end_date, room_type):
        conn = sqlite3.connect('availability.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT room_id FROM availability WHERE room_type = ? AND available_date BETWEEN ? AND ? AND status = "Available"''',
                       (room_type, str(start_date), str(end_date)))
        rooms = cursor.fetchall()
        conn.close()

        if not rooms:
            return []

        return [str(room[0]) for room in rooms]

# Configuración del servidor SOAP
soap_app = Application([
    AvailabilityService
],
    tns='hotel.availability',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
soap_server = WsgiApplication(soap_app)

# Interfaz gráfica (GUI) para consultar disponibilidad
def launch_gui():
    def check_availability_gui():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        room_type = room_type_entry.get()

        if not (start_date and end_date and room_type):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect('availability.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT room_id FROM availability WHERE room_type = ? AND available_date BETWEEN ? AND ? AND status = "Available"''',
                       (room_type, start_date, end_date))
        rooms = cursor.fetchall()
        conn.close()

        if not rooms:
            messagebox.showinfo("Disponibilidad", "No hay habitaciones disponibles")
        else:
            room_list = "\n".join([f"Habitación ID: {room[0]}" for room in rooms])
            messagebox.showinfo("Disponibilidad", f"Habitaciones disponibles:\n{room_list}")

    root = tk.Tk()
    root.title("Consulta de Disponibilidad de Habitaciones")

    tk.Label(root, text="Fecha de Inicio (YYYY-MM-DD)").grid(row=0, column=0)
    start_date_entry = tk.Entry(root)
    start_date_entry.grid(row=0, column=1)

    tk.Label(root, text="Fecha de Fin (YYYY-MM-DD)").grid(row=1, column=0)
    end_date_entry = tk.Entry(root)
    end_date_entry.grid(row=1, column=1)

    tk.Label(root, text="Tipo de Habitación").grid(row=2, column=0)
    room_type_entry = tk.Entry(root)
    room_type_entry.grid(row=2, column=1)

    tk.Button(root, text="Consultar Disponibilidad", command=check_availability_gui).grid(row=3, column=0, columnspan=2)

    root.mainloop()

# Inicialización de la base de datos y ejecución del servidor o GUI
if __name__ == '__main__':
    setup_availability_db()

    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        launch_gui()
    else:
        from wsgiref.simple_server import make_server
        server = make_server('0.0.0.0', 8000, soap_server)
        print("Servicio SOAP corriendo en http://0.0.0.0:8000")
        server.serve_forever()
