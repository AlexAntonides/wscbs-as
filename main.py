import uuid
import json

import validators
from flask import Flask, Response, request, redirect

app = Flask(__name__)
routes = {}

SHORT_URL_LEN = 8

@app.route('/', methods=['GET', 'POST', 'DELETE'])
def main():
   if request.method == 'GET':
        # return all keys
        return Response(f"{json.dumps(list(routes.keys()))}", status=200)
   elif request.method == 'POST':
        url = request.data

        if url: 
            url = url.decode("utf-8")

        if url and validators.url(url):
            random_string = str(uuid.uuid4())[:SHORT_URL_LEN]
            routes[random_string] = url
            return Response(f"{random_string}", status=201)
        else:
            return Response(f"error", status=400)
   else:
        return Response(status=404)

@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_id(id):
    if id in routes:
        if request.method == 'GET':
            url = routes[id]
            return redirect(f"{url}", code=301)
        elif request.method == 'PUT':
            url = request.data

            if url: 
                url = url.decode("utf-8")

            if url and validators.url(url):
                routes[id] = url
                return Response(status=200)
            else:
                return Response(f"error", status=400)
        elif request.method == 'DELETE':
            del routes[id]
            return Response(status=204)
    else:
            return Response(status=404)

if __name__ == '__main__':
   app.run(debug = True)