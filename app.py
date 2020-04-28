#!/usr/bin/env python

# vim: bg=dark

import os

from flask import Flask, request

from pub import grind

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hallo'

@app.route('/grind', methods=['GET', 'POST'])
def do_the_grind():

    req_data = request.get_json()

    try:
        secret = req_data['secret']
        assert secret == os.environ.get('SECRET', 'NOSECRET')
    except:
        return 'not authenticated', 400

    try:
        grind_time = int(req_data['grind_time'])
        grind(grind_time=grind_time)
        return 'nice', 200
    except:
        return 'Bad time', 400

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
