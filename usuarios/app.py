from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)


@app.route ("/usuarios")
def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor (dictionary=True)
    cursor.execute(
        "SELECT  * FROM usuarios"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(usuarios)

@app.route("/usuarios/<int:id>")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql= """
        SELECT * FROM usuarios
        WHERE id = %s
    """
    cursor.execute(sql,(id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    if usuario is None:
        return jsonify({"mensaje": "usuario no encontrada"}), 404
    return jsonify(usuario)

@app.route("/mascotas", methods = ["POST"])
def crear():
    nuevoUsuario = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql="""
        INSERT INTO usuarios
        (nombre, documento, email, telefono, rol, especilidad, horario)
        VALUES (%s, %s, %s,%s, %s,%s, %s)
    """
    valores =(nuevoUsuario["nombre"], nuevoUsuario["documento"], nuevoUsuario["email"], nuevoUsuario["telefono"], nuevoUsuario["rol"], nuevoUsuario["especialidad"], nuevoUsuario["horario"])

    cursor.execute(sql, valores)
    cursor.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "usuario creado", "id": nuevo_id}), 201


@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar(id):
    usuarioActualizado = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        UPDATE usuarios
        SET nombre = %s, documento = %s, email = %s,
            telefono = %s, rol = %s, especialidad = %s,
            horario = %s
        WHERE id = %s
    """

    valores = ( usuarioActualizado["nombre"], usuarioActualizado["documento"], usuarioActualizado["email"], usuarioActualizado["telefono"], usuarioActualizado["rol"], usuarioActualizado["especialidad"], usuarioActualizado["horario"], id )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "usuario actualizado"}), 200

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql= """
        DELETE * FROM usuarios
        WHERE id = %s
    """
    cursor.execute(sql,(id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    if usuario is None:
        return jsonify({"mensaje": "usuario no encontrada"}), 404
    return jsonify(usuario)

app.run (host="0.0.0.0", port=5000)
