from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from server.hackerator.gui.gui import gui_blueprint
from flask_socketio import SocketIO, emit
import json
import db_functions as db

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

    user=db.hamta_anvandare(rfid=id)

    if user is None:
        returnjson = {'kortnummer': 0, 'status': 'fail', 'timestamp': 0}
    else:
        dbanswer = db.stampla(user['kortnummer'])
        returnjson = {'kortnummer': user['kortnummer'], 'status': dbanswer['status'], 'timestamp': dbanswer['datum']},
        emit('toggle', returnjson, namespace='/gui',
             broadcast=True)

    return json.dumps(returnjson)


@application.route("/status/<id>")
def status(id):
    return "status" + id


application.route("/stamps/<kortnummer>")
def stamps(kortnummer):
    a=db.hamta_anvandare(kortnummer = kortnummer)
    if not a:
        print("Anvandaren finns inte.")

    alla_stamplingar = db.stamplingar(kortnummer)

    emit('stamps', {'kortnummer': kortnummer, 'stamps': stamps}, namespace='/gui', broadcast=True)
    return "Stamps" + kortnummer


if __name__ == "__main__":
    socketio.run(application)
