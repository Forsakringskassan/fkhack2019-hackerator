from flask import Blueprint, render_template

gui_blueprint = Blueprint('ui', __name__, template_folder='templates')
@gui_blueprint.route('/gui')
def view():
    return render_template("main.html")
