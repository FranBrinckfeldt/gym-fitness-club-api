from flask import abort, g
import mysql.connector
from ..config import get_connection
from ..models import Evaluacion

evaluacion_schema = Evaluacion()
evaluaciones_schema = Evaluacion(many=True)

def get_all_evaluaciones():
    try:
        usuario = g.token_payload
        connection = get_connection()
        cursor = connection.cursor()
        stmt = 'SELECT e.id, e.uid, e.date, e.weight, e.height, e.imc FROM evaluations e WHERE e.uid = %s'
        cursor.execute(stmt, (usuario.get('sub'),))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        evaluaciones = []
        for item in rows:
            evaluacion = dict(
                id=item[0],
                uid=item[1],
                date=item[2],
                peso=item[3],
                estatura=item[4],
                imc=item[5]
            )
            evaluaciones.append(evaluacion)
        return evaluaciones_schema.dump(evaluaciones)
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()
        abort(500)

def get_evaluacion_by_id(id):
    try:
        usuario = g.token_payload
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT e.id, e.uid, e.date, e.weight, e.height, e.imc FROM evaluations e WHERE e.id = %s AND e.uid = %s', (id, usuario.get('sub')))
        item = cursor.fetchone()
        cursor.close()
        connection.close()
        if item is None:
            return
        evaluacion = dict(
            id=item[0],
            uid=item[1],
            date=item[2],
            peso=item[3],
            estatura=item[4],
            imc=item[5]
        )
        return evaluacion_schema.dump(evaluacion)
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()
        abort(500)


def insert_evaluacion(evaluacion):
    try:
        usuario = g.token_payload
        connection = get_connection()
        cursor = connection.cursor(prepared=True)
        stmt = 'INSERT INTO evaluations (uid, date, weight, height, imc) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(stmt, (usuario.get('sub'), evaluacion['date'], evaluacion['peso'], evaluacion['estatura'], evaluacion['imc']))
        connection.commit()
        evaluacion['id'] = cursor.lastrowid
        response = {'message' : 'INSERTED', 'record' : evaluacion}, 201
        cursor.close()
        connection.close()
        return response
    except KeyError: 
        cursor.close()
        connection.close()
        abort(400)
    except mysql.connector.Error as err:
        cursor.close()
        connection.close()
        print(f'db_error : {err.msg}')
        if err.errno == 1452 or err.errno == 1366:
            abort(400)
        else: 
            abort(500)
    except: 
        cursor.close()
        connection.close()
        abort(500)

def delete_evaluacion(id):
    try:
        usuario = g.token_payload
        connection = get_connection()
        cursor = connection.cursor(prepared=True)
        stmt = 'DELETE FROM evaluations WHERE id = %s AND uid = %s'
        cursor.execute(stmt, (id, usuario.get('sub')))
        connection.commit()
        response = {'message' : 'DELETED', 'id' : id}, 200
        cursor.close()
        connection.close()
        return response
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()
        abort(500)

def update_evaluacion(evaluacion, id):
    try:
        usuario = g.token_payload
        connection = get_connection()
        cursor = connection.cursor(prepared=True)
        stmt = 'UPDATE evaluations SET date = %s, weight = %s, height = %s, imc = %s WHERE id = %s AND uid = %s'
        cursor.execute(stmt, (evaluacion['date'], evaluacion['peso'], evaluacion['estatura'], evaluacion['imc'], id, usuario.get('sub')))
        connection.commit()
        row_count = cursor.rowcount
        response = {'message' : 'UPDATED', 'rowAffected' : row_count}, 200
        cursor.close()
        connection.close()
        return response
    except mysql.connector.Error as err:
        cursor.close()
        connection.close()
        print(f'db_error : {err.msg}')
        if err.errno == 1452 or err.errno == 1366:
            abort(400)
        else: 
            abort(500)
    except Exception as err: 
        print(err)
        cursor.close()
        connection.close()
        abort(500)