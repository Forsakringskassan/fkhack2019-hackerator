from flask import Blueprint, render_template, request
import db_functions as db
from json import dumps

user_blueprint = Blueprint('user', __name__, template_folder='templates', static_folder='gui/static')
@user_blueprint.route('/user/<kortnr>')
def user(kortnr):
    userdata = db.stamplingar(kortnummer=kortnr)
    usr = db.hamta_anvandare(kortnummer=kortnr)
    try:
        status = userdata[0]['status']
    except IndexError:
        status = 0
    # userdata.reverse()
    return render_template("user.html", kortnummer=kortnr, userdata=dumps(userdata),
                           status=status, rfid=usr['rfid'], request=request)
