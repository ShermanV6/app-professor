
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dbcontainer'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 8306

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def professor_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return json.dumps(data)


@app.route('/professorlist', methods=['GET'])
def professor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('list.html', professors=data)


# Eliminar


@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM professor WHERE id = %s', (id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/professorlist')


# Actualizar pagina
@app.route('/updatepage', methods=['POST'])
def updatepages():
    if request.method == 'POST':
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM professor WHERE id=%s', (id))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        return render_template('actualizar.html', professors=data)


# Actualizar lista
@app.route('/updatelist', methods=['POST'])
def updatelist():
    if request.method == 'POST':
        firts_name = request.form['firts_name']
        last_name = request.form['last_name']
        city = request.form['city']
        address = request.form['address']
        salary = request.form['salary']
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'UPDATE professor SET firts_name=%s,last_name=%s,city=%s,address=%s,salary=%s WHERE id = %s', (firts_name, last_name, city, address, salary, id))
        mysql.connection.commit()
        cursor.close()
        return redirect('/professorlist')


# Crear


@app.route('/create', methods=['POST'])
def create():
    if request.method == 'GET':
        return render_template('list.html')

    if request.method == 'POST':
        firts_name = request.form['firts_name']
        last_name = request.form['last_name']
        city = request.form['city']
        address = request.form['address']
        salary = request.form['salary']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO professor(firts_name, last_name, city, address, salary) VALUES (%s,%s,%s,%s,%s)', (firts_name, last_name, city, address, salary))
        mysql.connection.commit()
        cursor.close()
        return redirect('/professorlist')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
