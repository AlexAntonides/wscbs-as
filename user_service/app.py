import hashlib

import datetime

from flask import Flask, Response, request
from http import HTTPStatus
import jwt

app = Flask(__name__)
users = {}

SALT = "5gz"
SECRET_KEY = "secret"
ALGORITHM = "HS256"

@app.route('/users', methods=['POST'])
def main():
    if request.method == 'POST':
        data = request.json
        
        if data: 
            username = data['username']

            if username not in users:
                password = data['password'] + SALT 
                
                hash = hashlib.md5(password.encode())

                users[username] = { 'username': username, 'password': hash }

                return Response(status=HTTPStatus.OK)
            else:
                return Response(status=HTTPStatus.BAD_REQUEST)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)
    else:
        return Response(status=HTTPStatus.NOT_FOUND)

@app.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        
        if data: 
            username = data['username']

            if username in users:
                user = users[username]
                password = data['password'] + SALT 

                hash = hashlib.md5(password.encode())
                if hash.digest() == user['password'].digest():
                    token = encode_auth_token(user)
                    return Response(token, status=HTTPStatus.OK) 
                else:
                    return Response(status=HTTPStatus.FORBIDDEN)
            else:
                return Response(status=HTTPStatus.FORBIDDEN)
        else:
            return Response(status=HTTPStatus.FORBIDDEN)
    else:
        return Response(status=HTTPStatus.NOT_FOUND)
        
@app.route('/users/validate', methods=['POST'])
def validate():
    if request.method == 'POST':
        data = request.json
        
        if data: 
            token = data['token']
            return Response(validate_token(token), status=HTTPStatus.OK)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)
    else:
        return Response(status=HTTPStatus.NOT_FOUND)

def encode_auth_token(user):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'iat': datetime.datetime.utcnow(),                                              # Issued At
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=1),      # Expiration Date
        'sub': user['username']                                                         # Subject
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def validate_token(encoded_token):
    """
    Generates the Auth Token
    :return: string
    """
    token = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])

    if token['iat'] < token['exp']:
        return token['sub']

if __name__ == '__main__':
   app.run(debug = True)