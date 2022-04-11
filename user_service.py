import hashlib

from flask import Flask, Response, request, redirect
import jwt

app = Flask(__name__)
users = {}

SALT = "5gz"

@app.route('/users', methods=['POST'])
def main():
    if request.method == 'POST':
        data = request.json
        
        if data: 
            username = data['username']
            password = data['password'] + SALT 
            
            hash = hashlib.md5(password.encode())

            users[username] = { 'username': username, 'password': hash }

            return Response(status=200)

@app.route('/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        
        if data: 
            username = data['username']

            if users[username]:
                user = users[username]
                password = data['password'] + SALT 

                hash = hashlib.md5(password.encode())
                if hash.digest() == user.password.digest():
                    # JWT Token
                    token = jwt.encode({'public_id' : user})
 
                    return Response(token, status=200)
                else:
                    return Response(status=403)
            else:
                return Response(status=403)
        else:
            return Response(status=403)

if __name__ == '__main__':
   app.run(debug = True)