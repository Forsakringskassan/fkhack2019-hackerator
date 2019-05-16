from flask import Blueprint, render_template
import db_functions as db
import json


gui_blueprint = Blueprint('ui', __name__, template_folder='templates', static_folder='gui/static')
@gui_blueprint.route('/latest')
def view():
    latest = db.stamplingar()
    return render_template("latest.html", latest=json.dumps(latest))
