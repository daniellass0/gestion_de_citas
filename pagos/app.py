from flask import Flask, jsonify, request
from database import conectar

app = Flask(__name__)


@app.route("/pagos", methods=["GET"])
def listar_pagos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pagos")
    pagos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify(pagos), 200

@app.route("/pagos/<int:id>", methods=["GET"])
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
        return jsonify({"mensaje": "Pago no encontrado"}), 404

    return jsonify(pago), 200

@app.route("/pagos", methods=["POST"])
def crear():

    nuevo_pago = request.get_json(silent=True)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        INSERT INTO pagos (monto, estado, creado)
        VALUES (%s, %s, %s)
    """

    valores = (
        nuevo_pago["monto"],
        nuevo_pago["estado"],
        nuevo_pago["creado"]
    )

    cursor.execute(sql, valores)
    conexion.commit()

    nuevo_id = cursor.lastrowid

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago creado con éxito",
        "id": nuevo_id
    }), 201


@app.route("/pagos/<int:id>", methods=["PUT"])
def actualizar(id):
    pago_actualizado = request.get_json(silent=True)


    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM pagos WHERE id = %s",
        (id,)
    )

    if cursor.fetchone() is None:
        cursor.close()
        conexion.close()

        return jsonify({
            "mensaje": "Pago no encontrado"
        }), 404

    sql = """
        UPDATE pagos
        SET monto = %s, estado = %s, creado = %s
        WHERE id = %s
    """

    valores = (
        pago_actualizado["monto"],
        pago_actualizado["estado"],
        pago_actualizado["creado"],
        id
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago actualizado con éxito"
    }), 200



@app.route("/pagos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
        DELETE FROM pagos
        WHERE id = %s
    """

    cursor.execute(sql, (id,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify({
        "mensaje": "Pago eliminado con éxito"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
