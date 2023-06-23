import serial
import dbconnection as db
from pyfirmata import Arduino
import time

# Configura el puerto serial
puerto = 'COM3'  # Cambia esto según el puerto que estés utilizando
velocidad = 9600  # Ajusta la velocidad según las especificaciones del lector RFID
dbconn = db.DBConnection()
dbconn.connect()
ledVerde = 5
ledRojo = 3
arduino = Arduino('COM3')

try:
    # Abre el puerto serial
    ser = serial.Serial(puerto, velocidad, timeout=1)
    print("Conexión exitosa con el lector RFID")
except serial.SerialException as e:
    print("Error al abrir el puerto serial:", str(e))
    exit()

try:
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        if line.startswith('UID:'):
            uid = line.split(':')[1]
            print(f"UID recibido: {uid}")
            # Consultar en la base de datos si el UID recibido existe
            query = 'SELECT * FROM "User" WHERE rfid = %s'
            params = (uid,)
            results = dbconn.execute_query(query, params)
            if len(results) > 0:
                user_rfid = results[0][6]
                if(user_rfid == uid):
                    print("Acceso concedido")
                    arduino.digital[ledVerde].write(1)
                    time.sleep(500)  
            else:
                print("Acceso denegado")
                arduino.digital[ledRojo].write(1)
                time.sleep(500)
        
except KeyboardInterrupt:
    # Cierra el puerto serial y finaliza el programa si se presiona Ctrl+C
    ser.close()
    print("Programa finalizado por el usuario")