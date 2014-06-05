from commands.sync_pivotal_to_toggl import sync
from flask import Blueprint
app = Blueprint('pivotaltracker_webhook', __name__)


@app.route("/pivotaltracker/webhook", methods=['POST'])
def pivotaltracker_webhook():
    # FIXME only sync the object that was modified, currently doing full sync
    sync.sync()
    return "ok"
