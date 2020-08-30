from flask import abort
import mysql.connector
import bcrypt
from ..config import get_connection
from ..models import Usuario
from ..utils import generate_token

def user_register(user):
    try:
        Usuario().load(user)
        hashed_password = bcrypt.hashpw(user['clave'].encode('utf-8'), bcrypt.gensalt())
        connection = get_connection()
        cursor = connection.cursor(prepared=True)
        stmt = 'INSERT INTO users (username, firstname, lastname, birth, height, password) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(stmt, (
            user['usuario'], 
            user['nombre'], 
            user['apellido'], 
            user['fechaNacimiento'],
            user['estatura'],
            hashed_password.decode('utf-8')));
        connection.commit()
        user['id'] = cursor.lastrowid
        user['clave'] = hashed_password.decode('utf-8')
        response = {'message' : 'REGISTERED', 'record' : user}, 201
        cursor.close()
        connection.close()
        return response
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()
        abort(500)

def user_login(username, password):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        stmt = 'SELECT id, username, password, height FROM users WHERE username = %s'
        cursor.execute(stmt, (username,))
        row = cursor.fetchone()
        if row is None:
            abort(403)
        is_valid = bcrypt.checkpw(password.encode('utf-8'), row[2].encode('utf-8'))
        if is_valid:
            token = generate_token({'username' : username, 'sub' : row[0], 'height' : row[3]})
        else: 
            abort(403)
        cursor.close()
        connection.close()
        return {'accessToken' : token.decode('utf-8')}
    except Exception as err:
        print(err)
        cursor.close()
        connection.close()
        abort(500)