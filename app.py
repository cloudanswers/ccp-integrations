import webhooks.pivotaltracker
from flask import Flask
app = Flask(__name__)

# blueprints
app.register_blueprint(webhooks.pivotaltracker.app)

# root url
@app.route('/')
def index():
    return 'ok'

if __name__ == "__main__":
    app.debug = True
    app.run()