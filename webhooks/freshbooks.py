from flask import Blueprint, request
app = Blueprint('freshbooks_webhook', __name__)


@app.route("/webhooks/freshbooks", methods=['POST'])
def freshbooks_webhook():
    # just needed during setup
    print request.data
    return "ok"
