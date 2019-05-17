import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../')
from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
from server.hackerator.gui.index import gui_blueprint
from server.hackerator.gui.user import user_blueprint
import argparse
from flask_socketio import SocketIO, emit
import json
import db_functions as db

application = Flask(__name__, static_folder="gui/static")
application.register_blueprint(gui_blueprint)
application.register_blueprint(user_blueprint)
bootstrap = Bootstrap(application)
socketio = SocketIO(application)


@application.route("/toggle/<id>")
def toggle(id):
    next = request.args.get('next')
    user = db.hamta_anvandare(rfid=id)

    if user is None:
        returnjson = {'kortnummer': 0, 'status': '-1', 'timestamp': 0}
    else:

        dbanswer = db.stampla(user['kortnummer'])
        returnjson = {'kortnummer': user['kortnummer'], 'status': dbanswer['status'], 'datum': dbanswer['datum']}
        emit('toggle', returnjson, namespace='/gui', broadcast=True)
    if next:
        return redirect(url_for(next))
    return json.dumps(returnjson)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameters for socketio')
    parser.add_argument('--host', default="127.0.0.1", help='Host')
    parser.add_argument('--port', default="5000", help='Port')
    parser.add_argument('--debug', default=False, action='store_true', help='Debug')
    args = parser.parse_args()

    socketio.run(application, host=args.host, port=args.port, debug=args.debug)
