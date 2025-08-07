import argparse
from configparser import ConfigParser
import importlib
import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

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

def _parse_options():
    parser = argparse.ArgumentParser(description="Launch the IDMEFv2 GLPI addon")
    parser.add_argument('-c', '--conf', help='give configuration file', dest='conf_file')
    return parser.parse_args()

def _open_glpi(config: ConfigParser):
    return ('foo', 'bar')

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

    processors = _create_processors(config, glpi)
    print(processors)

    app.run()

if __name__ == '__main__':
    _main()
