from flask import jsonify, request
from idmefv2.addon.glpi import app

@app.route('/ping', methods=['GET'])
def ping():
    name = request.args.get('name')
    pong = 'PONG ' + name if name is not None else 'PONG'
    data = {'answer': pong}
    return jsonify(data)
