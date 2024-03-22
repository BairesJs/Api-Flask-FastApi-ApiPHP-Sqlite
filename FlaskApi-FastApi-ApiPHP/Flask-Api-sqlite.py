from flask import Flask, jsonify, request, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

# Conexión a la base de datos SQLite (o la creación si no existe)
conn = sqlite3.connect('db.sqlite', check_same_thread=False)
cur = conn.cursor()

# Crear la tabla si no existe
cur.execute('''
    CREATE TABLE IF NOT EXISTS datos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT,
        email TEXT
    )
''')
conn.commit()

def guardar_datos_en_sqlite(datos):
    cur.execute('''
        INSERT INTO datos (nombre, direccion, telefono, email)
        VALUES (?, ?, ?, ?)
    ''', (datos['nombre'][0], datos['direccion'][0], datos['telefono'][0], datos['email'][0]))
    conn.commit()

@app.route('/data', methods=['GET'])
def get_data():
    try:
        df = pd.read_sql_query('SELECT * FROM datos', conn)
        data = df.to_dict(orient='records')
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/form', methods=['GET'])
def show_form():
    return render_template('form.html')

@app.route('/form', methods=['POST'])
def handle_form():
    try:
        request_data = request.form.to_dict(flat=False)
        print("Datos recibidos del formulario:", request_data)  # Mensaje de depuración
        guardar_datos_en_sqlite(request_data)
        return jsonify({'message': 'Data received and saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/update', methods=['POST'])
def handle_update():
    try:
        request_data = request.form.to_dict(flat=False)
        print("Datos recibidos para actualizar:", request_data)  # Mensaje de depuración
        guardar_datos_en_sqlite(request_data)
        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    try:
        cur.execute('DELETE FROM datos WHERE id = ?', (id,))
        conn.commit()
        return jsonify({'message': f'Data with ID {id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
