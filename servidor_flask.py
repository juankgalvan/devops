# servidor_flask.py
 
from flask import Flask, request, jsonify
import sqlite3
 
app = Flask(__name__)
 
# Conexión a la BD
def get_conn():
    conn = sqlite3.connect("usuarios.db")
    conn.row_factory = sqlite3.Row
    return conn
 
# Crear tabla
def init_db():
    conn = get_conn()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
     
    init_db()
 
# Insertar
@app.route('/insertar', methods=['POST'])
def insertar():
    data = request.json
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({"error": "Nombre requerido"}), 400
    conn = get_conn()
    conn.execute("INSERT INTO usuario (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Usuario insertado"}), 201
 
# Mostrar
@app.route('/usuarios', methods=['GET'])
def usuarios():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario")
    data = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)
 
# Buscar
@app.route('/buscar/<int:codigo>', methods=['GET'])
def buscar(codigo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE codigo = ?", (codigo,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404
 
# Modificar
@app.route('/modificar', methods=['PUT'])
def modificar():
    data = request.json
    codigo = data.get('codigo')
    nombre = data.get('nombre', '').strip()
    if not codigo or not nombre:
        return jsonify({"error": "Datos requeridos"}), 400
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE usuario SET nombre = ? WHERE codigo = ?", (nombre, codigo))
    conn.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario modificado"})
 
# Eliminar
@app.route('/eliminar/<int:codigo>', methods=['DELETE'])
def eliminar(codigo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE codigo = ?", (codigo,))
    conn.commit()
    if cur.rowcount == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario eliminado"})
     
if __name__ == '__main__':
    app.run(debug=True)
