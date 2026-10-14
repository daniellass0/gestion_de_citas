from flask import Flask, jsonify, request
from database import conectar
import os
app = Flask(__name__)


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(usuarios), 200


@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT * FROM usuarios
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    if usuario is None:
        return jsonify({"mensaje": "usuario no encontrado"}), 404
    return jsonify(usuario), 200


@app.route("/usuarios", methods=["POST"])
def crear():
    nuevoUsuario = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO usuarios
        (nombre, documento, email, telefono, rol, especialidad, horario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        nuevoUsuario["nombre"],
        nuevoUsuario["documento"],
        nuevoUsuario.get("email"),
        nuevoUsuario.get("telefono"),
        nuevoUsuario["rol"],
        nuevoUsuario.get("especialidad"),
        nuevoUsuario.get("horario")
    )

    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "usuario creado", "id": nuevo_id}), 201


@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar(id):
    usuarioActualizado = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if usuario is None:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "usuario no encontrado"}), 404

    sql = """
        UPDATE usuarios
        SET nombre = %s, documento = %s, email = %s,
            telefono = %s, rol = %s, especialidad = %s,
            horario = %s
        WHERE id = %s
    """

    valores = (
        usuarioActualizado.get("nombre", usuario["nombre"]),
        usuarioActualizado.get("documento", usuario["documento"]),
        usuarioActualizado.get("email", usuario["email"]),
        usuarioActualizado.get("telefono", usuario["telefono"]),
        usuarioActualizado.get("rol", usuario["rol"]),
        usuarioActualizado.get("especialidad", usuario["especialidad"]),
        usuarioActualizado.get("horario", usuario["horario"]),
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "usuario actualizado"}), 200


@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
    if usuario is None:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "usuario no encontrado"}), 404

    sql = """
        DELETE FROM usuarios
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "usuario eliminado", "usuario": usuario}), 200



app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
