from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gaster753159822'
app.config['MYSQL_DB'] = 'SistemaReservas'

mysql = MySQL(app)


def validar_campos(datos, requeridos):
    if not datos:
        return 'Cuerpo de la peticion vacio o no es JSON'
    faltantes = [c for c in requeridos if c not in datos]
    if faltantes:
        return f"Faltan campos requeridos: {', '.join(faltantes)}"
    return None


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID, Nombre, Apellido, Email FROM Usuarios")
        rows = cur.fetchall()
        cur.close()
        usuarios = [{'UserID': r[0], 'Nombre': r[1], 'Apellido': r[2], 'Email': r[3]} for r in rows]
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID, Nombre, Apellido, Email FROM Usuarios WHERE UserID = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return jsonify({'UserID': row[0], 'Nombre': row[1], 'Apellido': row[2], 'Email': row[3]}), 200
        return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios', methods=['POST'])
def add_usuario():
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['Nombre', 'Apellido', 'Email', 'Contrasena'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Usuarios (Nombre, Apellido, Email, Contrasena) VALUES (%s, %s, %s, %s)",
            (datos['Nombre'], datos['Apellido'], datos['Email'], datos['Contrasena'])
        )
        mysql.connection.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        return jsonify({'mensaje': 'Usuario creado', 'UserID': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['Nombre', 'Apellido', 'Email'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID FROM Usuarios WHERE UserID = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        cur.execute(
            "UPDATE Usuarios SET Nombre=%s, Apellido=%s, Email=%s WHERE UserID=%s",
            (datos['Nombre'], datos['Apellido'], datos['Email'], id)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Usuario actualizado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID FROM Usuarios WHERE UserID = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        cur.execute("DELETE FROM Usuarios WHERE UserID=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Usuario eliminado'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/habitaciones', methods=['GET'])
def get_habitaciones():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT RoomID, TipoHabitacion, Descripcion, Precio, Disponibilidad FROM Habitaciones")
        rows = cur.fetchall()
        cur.close()
        habitaciones = [{
            'RoomID': r[0],
            'TipoHabitacion': r[1],
            'Descripcion': r[2],
            'Precio': float(r[3]) if r[3] is not None else None,
            'Disponibilidad': bool(r[4]) if r[4] is not None else None
        } for r in rows]
        return jsonify(habitaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/habitaciones/<int:id>', methods=['GET'])
def get_habitacion(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT RoomID, TipoHabitacion, Descripcion, Precio, Disponibilidad FROM Habitaciones WHERE RoomID = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return jsonify({
                'RoomID': row[0],
                'TipoHabitacion': row[1],
                'Descripcion': row[2],
                'Precio': float(row[3]) if row[3] is not None else None,
                'Disponibilidad': bool(row[4]) if row[4] is not None else None
            }), 200
        return jsonify({'mensaje': 'Habitacion no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/habitaciones', methods=['POST'])
def add_habitacion():
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['TipoHabitacion', 'Descripcion', 'Precio', 'Disponibilidad'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Habitaciones (TipoHabitacion, Descripcion, Precio, Disponibilidad) VALUES (%s, %s, %s, %s)",
            (datos['TipoHabitacion'], datos['Descripcion'], datos['Precio'], datos['Disponibilidad'])
        )
        mysql.connection.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        return jsonify({'mensaje': 'Habitacion creada', 'RoomID': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/habitaciones/<int:id>', methods=['PUT'])
def update_habitacion(id):
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['TipoHabitacion', 'Descripcion', 'Precio', 'Disponibilidad'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute("SELECT RoomID FROM Habitaciones WHERE RoomID = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'Habitacion no encontrada'}), 404
        cur.execute(
            "UPDATE Habitaciones SET TipoHabitacion=%s, Descripcion=%s, Precio=%s, Disponibilidad=%s WHERE RoomID=%s",
            (datos['TipoHabitacion'], datos['Descripcion'], datos['Precio'], datos['Disponibilidad'], id)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Habitacion actualizada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reservaciones', methods=['GET'])
def get_reservaciones():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT ReservationID, UserID, RoomID, FechaInicio, FechaFin, EstadoReserva FROM Reservaciones")
        rows = cur.fetchall()
        cur.close()
        reservaciones = [{
            'ReservationID': r[0],
            'UserID': r[1],
            'RoomID': r[2],
            'FechaInicio': str(r[3]) if r[3] is not None else None,
            'FechaFin': str(r[4]) if r[4] is not None else None,
            'EstadoReserva': r[5]
        } for r in rows]
        return jsonify(reservaciones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reservaciones/<int:id>', methods=['GET'])
def get_reservacion(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT ReservationID, UserID, RoomID, FechaInicio, FechaFin, EstadoReserva FROM Reservaciones WHERE ReservationID = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return jsonify({
                'ReservationID': row[0],
                'UserID': row[1],
                'RoomID': row[2],
                'FechaInicio': str(row[3]) if row[3] is not None else None,
                'FechaFin': str(row[4]) if row[4] is not None else None,
                'EstadoReserva': row[5]
            }), 200
        return jsonify({'mensaje': 'Reservacion no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reservaciones', methods=['POST'])
def add_reservacion():
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['UserID', 'RoomID', 'FechaInicio', 'FechaFin', 'EstadoReserva'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute("SELECT UserID FROM Usuarios WHERE UserID = %s", (datos['UserID'],))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'UserID no existe'}), 400
        cur.execute("SELECT RoomID FROM Habitaciones WHERE RoomID = %s", (datos['RoomID'],))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'RoomID no existe'}), 400
        cur.execute(
            "INSERT INTO Reservaciones (UserID, RoomID, FechaInicio, FechaFin, EstadoReserva) VALUES (%s, %s, %s, %s, %s)",
            (datos['UserID'], datos['RoomID'], datos['FechaInicio'], datos['FechaFin'], datos['EstadoReserva'])
        )
        mysql.connection.commit()
        nuevo_id = cur.lastrowid
        cur.close()
        return jsonify({'mensaje': 'Reservacion creada', 'ReservationID': nuevo_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reservaciones/<int:id>', methods=['PUT'])
def update_reservacion(id):
    try:
        datos = request.get_json(silent=True)
        error = validar_campos(datos, ['UserID', 'RoomID', 'FechaInicio', 'FechaFin', 'EstadoReserva'])
        if error:
            return jsonify({'mensaje': error}), 400
        cur = mysql.connection.cursor()
        cur.execute("SELECT ReservationID FROM Reservaciones WHERE ReservationID = %s", (id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'Reservacion no encontrada'}), 404
        cur.execute("SELECT UserID FROM Usuarios WHERE UserID = %s", (datos['UserID'],))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'UserID no existe'}), 400
        cur.execute("SELECT RoomID FROM Habitaciones WHERE RoomID = %s", (datos['RoomID'],))
        if not cur.fetchone():
            cur.close()
            return jsonify({'mensaje': 'RoomID no existe'}), 400
        cur.execute(
            "UPDATE Reservaciones SET UserID=%s, RoomID=%s, FechaInicio=%s, FechaFin=%s, EstadoReserva=%s WHERE ReservationID=%s",
            (datos['UserID'], datos['RoomID'], datos['FechaInicio'], datos['FechaFin'], datos['EstadoReserva'], id)
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensaje': 'Reservacion actualizada'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)