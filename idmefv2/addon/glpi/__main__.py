import argparse
from configparser import ConfigParser
import importlib
import logging
from flask import Flask, jsonify, request
import glpi_api

app = Flask(__name__)

PROCESSORS = []

@app.route('/ping', methods=['GET'])
def _ping():
    name = request.args.get('name')
    pong = 'PONG ' + name if name is not None else 'PONG'
    data = {'answer': pong}
    return jsonify(data)

@app.route('/dns', methods=['POST'])
def _dns():
    message = request.get_json(force = True)
    logging.debug('processing %s with %s', str(message), str(PROCESSORS))
    for p in PROCESSORS:
        message = p.process(message)
    return jsonify(message)

def _parse_options():
    parser = argparse.ArgumentParser(description="Launch the IDMEFv2 GLPI addon")
    parser.add_argument('-c', '--conf', help='give configuration file', dest='conf_file')
    return parser.parse_args()

def _open_glpi(config: ConfigParser):
    url = config.get('glpi', 'url')
    apptoken = config.get('glpi', 'apptoken')
    auth = config.get('glpi', 'auth')
    return glpi_api.GLPI(url=url, apptoken=apptoken, auth=auth)

def _create_processors(config: ConfigParser, glpi):
    pn = list(map(lambda n : n.strip(), config.get('idmefv2', 'processors').split(',')))
    m = importlib.import_module('idmefv2.addon.glpi')
    pc = []
    for c in map(lambda n: getattr(m, n), pn):
        pc.append(c(glpi))
    return pc

def _main():
    options = _parse_options()

    config = ConfigParser()
    config.read(options.conf_file)

    logging.basicConfig(level=config.get('logging', 'level', fallback='INFO'))

    glpi = _open_glpi(config)
    logging.debug('connected to GLPI (%s)', str(glpi))

    #pylint: disable=global-statement
    global PROCESSORS
    PROCESSORS = _create_processors(config, glpi)

    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    _main()
