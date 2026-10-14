from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)

# URL del servicio de usuarios (ej: http://usuarios:5000). Si no se define, no se valida el usuario.
#USUARIOS_URL = os.getenv("USUARIOS_URL")


#def usuario_existe(usuario_id):
#    """True si existe, False si no existe, None si no se puede validar."""
#    if not USUARIOS_URL:
#        return None
#    try:
#        respuesta = requests.get(f"{USUARIOS_URL}/usuarios/{usuario_id}", timeout=3)
#        return respuesta.status_code == 200
#    except requests.RequestException:
#        return None


@app.route("/pagos")
def listar_pagos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM pagos"
    )
    pagos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(pagos)


@app.route("/pagos/<int:id>")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT * FROM pagos
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    pago = cursor.fetchone()
    cursor.close()
    conexion.close()
    if pago is None:
        return jsonify({"mensaje": "pago no encontrado"}), 404
    return jsonify(pago)



@app.route("/pagos", methods=["POST"])
def crear():
    nuevoPago = request.json

    #existe = usuario_existe(nuevoPago["usuario_id"])
    #if existe is False:
        #return jsonify({"mensaje": "usuario no encontrado"}), 404
# esto es para que si un guarde pagos de usuarios inecistentes 
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO pagos
        (usuario_id, monto, metodo, estado, concepto)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (nuevoPago["usuario_id"], nuevoPago["monto"], nuevoPago["metodo"], nuevoPago["estado"], nuevoPago["concepto"])

    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "pago creado", "id": nuevo_id}), 201


@app.route("/pagos/<int:id>", methods=["PUT"])
def actualizar(id):
    pagoActualizado = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
        UPDATE pagos
        SET usuario_id = %s, monto = %s, metodo = %s,
            estado = %s, concepto = %s
        WHERE id = %s
    """

    valores = (pagoActualizado["usuario_id"], pagoActualizado["monto"], pagoActualizado["metodo"], pagoActualizado["estado"], pagoActualizado["concepto"], id)

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "pago actualizado"}), 200


@app.route("/pagos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        DELETE FROM pagos
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    conexion.commit()
    eliminados = cursor.rowcount
    cursor.close()
    conexion.close()
    if eliminados == 0:
        return jsonify({"mensaje": "pago no encontrado"}), 404
    return jsonify({"mensaje": "pago eliminado"}), 200


app.run(host="0.0.0.0", port=5000)