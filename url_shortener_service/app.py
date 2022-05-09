import os

import uuid
import json

import validators
from flask import Flask, Response, request, redirect
from http import HTTPStatus
import requests

app = Flask(__name__)
routes = {} # { username, route }

USER_SERVICE_PATH = os.getenv('USER_SERVICE_PATH')
SHORT_URL_LEN = 8

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def main():
    if request.method == 'GET':
        # return all keys
        return Response(f"{json.dumps(list(routes.keys()))}", status=HTTPStatus.OK)
    elif request.method == 'POST':
        validated = validate_authorization(request)  
        if (validated == None):
            return Response(status=HTTPStatus.FORBIDDEN)

        url = request.data

        if url: 
            url = url.decode("utf-8")

        # Validation check if URL is valid URL
        if url and validators.url(url):
            # Generate a randomised unused key
            random_string = None
            while random_string is None or random_string in routes:
                random_string = str(uuid.uuid4())[:SHORT_URL_LEN]
            routes[random_string] = { 'owner': validated, 'url': url } 
            return Response(f"{random_string}", status=HTTPStatus.CREATED)
        else:
            return Response(f"error", status=HTTPStatus.BAD_REQUEST)
    else:
        return Response(status=HTTPStatus.NOT_FOUND)

@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_id(id):
    if id in routes:
        if request.method == 'GET':
            url = routes[id]['url']
            return redirect(f"{url}", code=HTTPStatus.MOVED_PERMANENTLY) # http.status.ok 
        elif request.method == 'PUT':
            validated = validate_authorization(request)  
            if (validated == None): 
                return Response(status=HTTPStatus.FORBIDDEN)

            if routes[id]['owner'] != validated:
                return Response(status=HTTPStatus.FORBIDDEN)

            url = request.data

            if url: 
                url = url.decode("utf-8")

            if url and validators.url(url):
                routes[id]['url'] = url
                return Response(status=HTTPStatus.OK)
            else:
                return Response(f"error", status=HTTPStatus.BAD_REQUEST)
        elif request.method == 'DELETE':
            validated = validate_authorization(request)  
            if (validated == None): 
                return Response(status=HTTPStatus.FORBIDDEN)

            if routes[id]['owner'] != validated:
                return Response(status=HTTPStatus.FORBIDDEN)

            del routes[id]
            return Response(status=HTTPStatus.NO_CONTENT)
    else:
        return Response(status=HTTPStatus.NOT_FOUND)

def validate_authorization(request):
    token = request.headers.get('Authorization')
    if 'Bearer' in token:
        token = token.split(" ")[-1]
    
    if not token:
        return None

    # decoding the payload to fetch the stored details
    response = requests.post(f'http://{USER_SERVICE_PATH}/users/validate', json={ "token": token })
    if (response.status_code == HTTPStatus.OK):
        return response.text
    else:
        return None

if __name__ == '__main__':
   app.run(debug = True)