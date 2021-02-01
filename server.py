from flask import Flask, request
from powerplant_payload import processing_output
import json

app = Flask(__name__)


@app.route('/help')
def help():
    return "Coding challenge"


@app.route('/productionplan', methods=['POST'])
def productionplan():
    input = json.loads(request.json)
    output = processing_output(input)

    return output


if __name__ == '__main__':
    app.run('0.0.0.0', port=8888)
