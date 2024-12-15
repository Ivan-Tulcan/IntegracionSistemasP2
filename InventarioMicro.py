# Microservicio para la gestión de inventario

import sqlite3
from flask import Flask, request, jsonify

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

# Inicialización de la base de datos y ejecución del servidor
if __name__ == '__main__':
    setup_rooms_db()
    app.run(debug=True, port=6000)
