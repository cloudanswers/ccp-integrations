import sync

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'ok'


@app.route("/pivotaltracker/webhook", methods=['POST', 'GET'])
def pivotaltracker_webhook():
    sync.sync()
    return "ok"

if __name__ == "__main__":
    app.run()