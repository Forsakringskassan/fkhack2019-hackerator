from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from server.hackerator.gui.gui import gui_blueprint

application = Flask(__name__)
application.register_blueprint(gui_blueprint)
bootstrap = Bootstrap(application)

@application.route("/")
def hello():
    return "Hackeratorn says no!"

@application.route("/toggle/<id>")
def toggle(id):
    return "Toggle" + id
@application.route("/status/<id>")
def status(id):
    return "status" + id


if __name__ == "__main__":
    application.run()
