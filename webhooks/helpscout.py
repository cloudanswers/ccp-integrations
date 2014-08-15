from flask import Blueprint, request, jsonify
import time
app = Blueprint('helpscout_webhook', __name__)


@app.route("/webhooks/helpscout", methods=['POST'])
def helpscout_webhook():
    return jsonify({"html": "<b>test</b> test %s" % time.gmtime()})
