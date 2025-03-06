from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Configuración de la base de datos desde variables de entorno

DB_CONFIG = {
    "host": os.getenv("MYSQLHOST", "localhost"),
    "user": os.getenv("MYSQLUSER", "root"),
    "password": os.getenv("MYSQLPASSWORD", "password"),
    "database": os.getenv("MYSQLDATABASE", "railway"),
    "port": int(os.getenv("MYSQLPORT", 3306))
}


def insertar_voto(direccion):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votos (direccion) VALUES (%s)", (direccion,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/votar', methods=['POST'])
def votar():
    data = request.json
    direccion = data.get("direccion")
    if direccion in ["UP", "DOWN", "LEFT", "RIGHT"]:
        insertar_voto(direccion)
        return jsonify({"message": "Voto registrado"}), 200
    return jsonify({"error": "Dirección inválida"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
