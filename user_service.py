import hashlib

from flask import Flask, Response, request, redirect
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
                    token = jwt.encode({'public_id' : user}, SECRET_KEY, algorithm=ALGORITHM)
                    return Response(token, status=HTTPStatus.OK)
                else:
                    return Response(status=HTTPStatus.BAD_REQUEST)
            else:
                return Response(status=HTTPStatus.BAD_REQUEST)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

if __name__ == '__main__':
   app.run(debug = True)