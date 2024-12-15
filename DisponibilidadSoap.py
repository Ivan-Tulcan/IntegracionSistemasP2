# Servicio SOAP para consultar la disponibilidad de habitaciones

import sqlite3
from spyne import Application, rpc, ServiceBase, Unicode, Date, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

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

# Definición del servicio SOAP
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

# Inicialización del servidor
if __name__ == '__main__':
    setup_availability_db()
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 8000, soap_server)
    print("Servicio SOAP corriendo en http://0.0.0.0:8000")
    server.serve_forever()
