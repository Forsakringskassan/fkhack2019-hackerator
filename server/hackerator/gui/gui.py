from flask import Blueprint, render_template

gui_blueprint = Blueprint('ui', __name__, template_folder='templates', static_folder='gui/static')
@gui_blueprint.route('/gui')
def view():
    return render_template("main_mivi.html")
