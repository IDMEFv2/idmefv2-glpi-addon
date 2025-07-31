from idmefv2.addon.glpi import app

@app.route('/ping')
def ping():
    return 'PONG'
