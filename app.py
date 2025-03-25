from flask import Flask, render_template, request, redirect, flash
import mysql.connector   # type: ignore

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="articulos"
    )
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, introduccion, fecha, autores FROM creacion")
    arti = cursor.fetchall()
    conn.close()
    return render_template('index.html', arti=arti)

@app.route('/add', methods=['POST'])
def add():
    titulo = request.form['titulo']
    introduccion = request.form['introduccion']
    fecha = request.form['fecha']
    autores = request.form['autores']  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM creacion WHERE titulo = %s", (titulo,))
    if cursor.fetchone():
        flash("Error: Ya existe un artículo con ese título", "danger")
        conn.close()
        return redirect('/')
    cursor.execute("INSERT INTO creacion (titulo, introduccion, autores, fecha) VALUES (%s, %s, %s, %s)", 
                   (titulo, introduccion, autores, fecha))
    conn.commit()
    conn.close()

    flash("Artículo publicado con éxito.", "success")
    return redirect('/')

# Ruta para eliminar artículo
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM creacion WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    flash("Artículo eliminado con éxito.", "success")
    return redirect('/')

# Ruta para actualizar artículo
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    titulo = request.form['titulo']
    introduccion = request.form['introduccion']
    fecha = request.form['fecha']
    autores = request.form['autores']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el título ya existe para otro artículo
    cursor.execute("SELECT * FROM creacion WHERE titulo = %s AND id != %s", (titulo, id))
    if cursor.fetchone():
        flash("Error: Ya existe un artículo con ese título.", "danger")
        conn.close()
        return redirect('/')

    # Actualizar el artículo
    cursor.execute("UPDATE creacion SET titulo = %s, introduccion = %s, autores = %s, fecha = %s WHERE id = %s",
                   (titulo, introduccion, autores, fecha, id))
    conn.commit()
    conn.close()

    flash("Artículo actualizado con éxito.", "success")
    return redirect('/')

