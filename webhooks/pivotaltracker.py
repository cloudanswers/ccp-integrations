import json
import logging
from commands.sync_pivotal_to_toggl import sync
from flask import Blueprint, request
app = Blueprint('pivotaltracker_webhook', __name__)


@app.route("/webhooks/pivotaltracker", methods=['POST'])
def pivotaltracker_webhook():
    data = json.loads(request.data)
    story_ids = map(lambda x: x.get('id'),
                    data.get('primary_resources'))
    sync(story_ids)
    return "ok"
