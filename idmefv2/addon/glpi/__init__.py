from flask import Flask

app = Flask(__name__)

import idmefv2.addon.glpi.routes
