from flask import Flask, jsonify, request
import requests
import os
from database import conectar

app = Flask(__name__)

citas_url = os.getenv("CITAS_URL", "http://citas:5001")


@app.route("/pagos", methods=["GET"])
def listar_pagos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pagos")
    pagos = cursor.fetchall()
    
    # Convertir TIMESTAMP a string para evitar error de serialización en Flask
    for pago in pagos:
        if pago.get("creado_en"):
            pago["creado_en"] = str(pago["creado_en"])

    cursor.close()
    conexion.close()
    return jsonify(pagos), 200


@app.route("/pagos/<int:id>", methods=["GET"])
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM pagos WHERE id = %s"
    cursor.execute(sql, (id,))
    pago = cursor.fetchone()
    cursor.close()
    conexion.close()

    if pago is None:
        return jsonify({"mensaje": "pago no encontrado"}), 404

    if pago.get("creado_en"):
        pago["creado_en"] = str(pago["creado_en"])

    return jsonify(pago), 200


@app.route("/pagos/cita/<int:cita_id>", methods=["GET"])
def buscar_por_cita(cita_id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM pagos WHERE cita_id = %s"
    cursor.execute(sql, (cita_id,))
    pagos = cursor.fetchall()

    for pago in pagos:
        if pago.get("creado_en"):
            pago["creado_en"] = str(pago["creado_en"])

    cursor.close()
    conexion.close()
    return jsonify(pagos), 200


@app.route("/pagos", methods=["POST"])
def crear():
    nuevoPago = request.json
    cita_id = nuevoPago.get("cita_id")

    if not cita_id:
        return jsonify({"mensaje": "El id de la cita (cita_id) es requerido"}), 400

    # 1. Validar la existencia de la cita en el microservicio de citas
    try:
        resp_cita = requests.get(f"{citas_url.rstrip('/')}/citas/{cita_id}", timeout=5)
        if resp_cita.status_code == 404:
            return jsonify({"mensaje": f"La cita con id {cita_id} no existe"}), 404
        elif resp_cita.status_code != 200:
            return jsonify({"mensaje": "Error al verificar la cita en el servicio de citas"}), 502
        cita_data = resp_cita.json()
    except requests.exceptions.RequestException:
        return jsonify({"mensaje": "No se pudo conectar con el servicio de citas"}), 503

    # Obtener el paciente_id directamente del JSON recibido o heredarlo de la cita
    paciente_id = nuevoPago.get("paciente_id", cita_data.get("usuario_id"))

    # 2. Registrar el pago en la base de datos
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO pagos
        (cita_id, paciente_id, monto, metodo, estado)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        cita_id,
        paciente_id,
        nuevoPago["monto"],
        nuevoPago.get("metodo", "tarjeta"),
        nuevoPago.get("estado", "aprobado")
    )

    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()

    # 3. Actualizar la cita a 'confirmada' vinculando el nuevo pago_id
    try:
        cita_data["estado"] = "confirmada"
        cita_data["pago_id"] = nuevo_id
        requests.put(f"{citas_url.rstrip('/')}/citas/{cita_id}", json=cita_data, timeout=5)
    except requests.exceptions.RequestException:
        print(f"Advertencia: No se pudo actualizar el estado de la cita {cita_id}")

    return jsonify({"mensaje": "pago creado", "id": nuevo_id}), 201


@app.route("/pagos/<int:id>", methods=["PUT"])
def actualizar(id):
    pagoActualizado = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pagos WHERE id = %s", (id,))
    pago = cursor.fetchone()
    if pago is None:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "pago no encontrado"}), 404

    sql = """
        UPDATE pagos
        SET cita_id = %s, paciente_id = %s, monto = %s,
            metodo = %s, estado = %s
        WHERE id = %s
    """
    valores = (
        pagoActualizado["cita_id"],
        pagoActualizado["paciente_id"],
        pagoActualizado["monto"],
        pagoActualizado["metodo"],
        pagoActualizado["estado"],
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "pago actualizado"}), 200


@app.route("/pagos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pagos WHERE id = %s", (id,))
    pago = cursor.fetchone()

    if pago is None:
        cursor.close()
        conexion.close()
        return jsonify({"mensaje": "pago no encontrado"}), 404

    if pago.get("creado_en"):
        pago["creado_en"] = str(pago["creado_en"])

    sql = "DELETE FROM pagos WHERE id = %s"
    cursor.execute(sql, (id,))
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"mensaje": "pago eliminado", "pago": pago}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)