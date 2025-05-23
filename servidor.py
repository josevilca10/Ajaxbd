# servidor.py
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
CORS(app)  

def crear_y_llenar_bd(nombre_bd):
    """Crea una base de datos y la llena con datos."""
    conn = sqlite3.connect(nombre_bd)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            director TEXT,
            año INTEGER
        )
    ''')

    peliculas = [
        ('Inception', 'Christopher Nolan', 2010),
        ('The Matrix', 'Lana Wachowski', 1999),
        ('El Padrino', 'Francis Ford Coppola', 1972),
        ('Pulp Fiction', 'Quentin Tarantino', 1994)
    ]

    cursor.executemany("INSERT INTO peliculas (titulo, director, año) VALUES (?, ?, ?)", peliculas)
    conn.commit()
    conn.close()


@app.route('/peliculas')
@cross_origin()
def obtener_peliculas():
    """Devuelve todas las películas como JSON."""
    try:
        conn = sqlite3.connect('imdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM peliculas")
        peliculas = cursor.fetchall()
        conn.close()

        data = []
        for p in peliculas:
            data.append({'id': p[0], 'titulo': p[1], 'director': p[2], 'año': p[3]})
        return jsonify(data)

    except sqlite3.Error as e:
        return jsonify({"error": f"Error al obtener datos: {e}"}), 500


if __name__ == '__main__':
    crear_y_llenar_bd('imdb.db')  
    app.run(debug=True, port=5000)

