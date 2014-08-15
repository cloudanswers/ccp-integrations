import logging
from flask import Flask
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

import webhooks
app.register_blueprint(webhooks.pivotaltracker.app)
app.register_blueprint(webhooks.freshbooks.app)
app.register_blueprint(webhooks.helpscout.app)

# root url
@app.route('/')
def index():
    return 'ok'

if __name__ == "__main__":
    app.debug = True
    app.run()