from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from server.hackerator.gui.gui import gui_blueprint
from flask_socketio import SocketIO, emit
import time

application = Flask(__name__, static_folder="gui/static")
application.register_blueprint(gui_blueprint)
bootstrap = Bootstrap(application)
socketio = SocketIO(application)
@socketio.on('connect', namespace='/gui')
def gui_connect():
    print("Client connected")

@socketio.on('disconnect', namespace='/gui')
def gui_disconnect():
    print("Client disconnected")


@application.route("/")
def hello():
    return "Hackeratorn says no!"

@application.route("/toggle/<id>")
def toggle(id):
    now = time.time()
    emit('toggle', {'id': id, 'timestmp:': now}, namespace='/gui', broadcast=True)
    return "Toggle" + id

@application.route("/status/<id>")
def status(id):
    return "status" + id


if __name__ == "__main__":
    socketio.run(application)
