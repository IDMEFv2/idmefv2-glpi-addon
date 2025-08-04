'''
Routes for the Flask application
'''
from flask import jsonify, request
from idmefv2.addon.glpi import app

@app.route('/ping', methods=['GET'])
def ping():
    '''
    Implements the /ping GET request
    Response is PONG + 'name' parameter of request
    '''
    name = request.args.get('name')
    pong = 'PONG ' + name if name is not None else 'PONG'
    data = {'answer': pong}
    return jsonify(data)
