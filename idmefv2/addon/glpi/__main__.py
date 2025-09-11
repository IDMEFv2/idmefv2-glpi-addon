"""
Main for IDMEFv2 GLPI add-on
"""
import argparse
from configparser import ConfigParser
import logging
from flask import Flask, jsonify, request
from flask.views import View
import glpi_api
from .process import NullProcessor, DNSProcessor, GLPIProcessor


def _parse_options():
    parser = argparse.ArgumentParser(description="Launch the IDMEFv2 GLPI addon", prog="glpi-addon")
    parser.add_argument(
        "-c", "--conf", help="give configuration file", dest="conf_file", required=True
    )
    return parser.parse_args()


def _open_glpi(config: ConfigParser):
    url = config.get("glpi", "url")
    apptoken = config.get("glpi", "apptoken")
    auth = config.get("glpi", "auth")
    try:
        return glpi_api.GLPI(url=url, apptoken=apptoken, auth=auth)
    except glpi_api.GLPIError as e:
        logging.error("cannot connect to GLPI: %s", str(e))
        return None


class ProcessorView(View):
    """
    A derived class from flask View, which receives a IDMEFv2 message in
    a POST request and returns the processed message.
    """
    methods = ["POST"]

    def __init__(self, processor):
        self._processor = processor

    def dispatch_request(self):
        logging.debug("received request %s [%s]", str(request), str(request.get_data()))
        message = request.get_json(force=True)
        logging.debug("processing %s with %s", str(message), str(self._processor))
        self._processor.process(message)
        return jsonify(message)


def _main():
    options = _parse_options()

    config = ConfigParser()
    config.read(options.conf_file)

    logging.basicConfig(level=config.get("logging", "level", fallback="INFO"))

    glpi = _open_glpi(config)
    logging.debug("connected to GLPI (%s)", str(glpi))

    app = Flask(__name__)

    app.add_url_rule("/null", view_func=ProcessorView.as_view("null", NullProcessor()))
    app.add_url_rule("/dns", view_func=ProcessorView.as_view("dns", DNSProcessor()))
    app.add_url_rule("/glpi", view_func=ProcessorView.as_view("glpi", GLPIProcessor(glpi)))

    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    _main()
