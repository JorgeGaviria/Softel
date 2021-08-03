
from flask import blueprints, g, render_template, redirect, url_for, flash, Blueprint, request
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash

from project.db import get_db
from project.auth import login_required_empleado

bp = Blueprint('empleado',__name__,url_prefix='/empleado')

# CRUD Empleado

# Crear empleado
@bp.route('/home',methods=['POST',"GET"])
@login_required_empleado
def home():
    return render_template('empleado/home.html')


