import functools

from flask import g, render_template, redirect, url_for, flash, Blueprint, request, session
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash
from project.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        dni = request.form['dni']
        password = request.form['password']

        db,c = get_db()

        error = None

        c.execute('Select * from tbl_empleado where dni = %s', (dni,))

        empleado = c.fetchone()

        if empleado is None:
            error = "Usuario y/o contraseña incorrectos"
        elif not check_password_hash(empleado['pass'],password):
            error = "Usuario y/o contraseña incorrectos"
        
        if error is None:
            session.clear()
            session['dni_empleado'] = empleado['dni']
            if empleado['cargo'] == 1:
                return redirect(url_for('admin.lista_empleados'))
            else:
                return redirect(url_for('empleado.home'))                
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request

def load_user_in_g():
    dni_empleado = session.get('dni_empleado')
    db, c = get_db()
    c.execute('select * from tbl_empleado where dni = %s',(dni_empleado,))
    empleado = c.fetchone()
    g.user = empleado
    if empleado is None:
        g.empleado = None
        g.administrador = None
    else:
        if empleado['cargo'] == 1:
            g.administrador = empleado
            g.empleado = None
        else:
            g.empleado = empleado
            g.administrador = None




def login_required_empleado(view):
    @functools.wraps(view)
    def wrapped_empleado(**kwargs):
        if g.administrador is None:
            if g.empleado is None:
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        else:
            return redirect(url_for('auth.logout'))
    return wrapped_empleado

def login_required_admin(view):
    @functools.wraps(view)
    def wrapped_administrador(**kwargs):
        if g.empleado is None:
            if g.administrador is None:
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        else:
            return redirect(url_for('auth.logout'))
    return wrapped_administrador

def login_required(view):
    @functools.wraps(view)
    def wrapped_user(**kwargs):
        if g.administrador is None and g.empleado is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('public.home'))