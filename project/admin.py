
from flask import blueprints, g, render_template, redirect, url_for, flash, Blueprint, request
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash

from project.db import get_db
from project.auth import login_required_admin

bp = Blueprint('admin',__name__,url_prefix='/admin')

# CRUD Empleado

# Crear empleado
@bp.route('/crear_empleado',methods=['POST',"GET"])
def crear_empleado():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        cargo = request.form['cargo']
        password = request.form['password']
        password_check = request.form['password_check']

        error = None

        db, c = get_db()
        c.execute('select * from tbl_empleado where dni = %s',(dni,))

        repeat_dni = c.fetchone()

        if not nombres:
            error = "Ingrese sus Nombres"
        if not apellidos:
            error = "Ingrese sus Apellidos"
        if not dni:
            error = "Ingrese el número de su documento"
        if repeat_dni is not None:
            error = "El dni ingresado ya esta registrado"
        if cargo is None:
            error = "Ingrese un cargo valido"
        if cargo == "3":
            error= "Ingrese un cargo valido"
        if password is None:
            error = "Ingrese su contraseña"
        if password != password_check:
            error= "Las contraseñas no coinciden"
        
        if error is None:
            c.execute('insert into tbl_empleado (nombres,apellidos,dni,cargo,pass) values(%s,%s,%s,%s,%s)',(nombres,apellidos,dni,cargo,generate_password_hash(password)))
            db.commit()
            return redirect(url_for('.lista_empleados'))
    
        flash(error)
    return render_template('admin/crear_empleado.html')

# Ver Empleados
@bp.route('/lista_empleados',methods=['POST','GET'])
@login_required_admin
def lista_empleados():
    db, c = get_db()
    c.execute('Select * from tbl_empleado where 1')
    empleados = c.fetchall()
    return render_template('admin/lista_empleados.html',empleados=empleados)


#Editar Empleados 
# Conseguir empleado
def get_empleado(idtbl_empleado):
    db, c = get_db()
    c.execute('select * from tbl_empleado where idtbl_empleado = %s',(idtbl_empleado,))
    datos_empleado = c.fetchone()
    if datos_empleado == None:
        abort(404,"El empleado a editar no existe")
    else:
        return datos_empleado

@bp.route('/<int:idtbl_empleado>/editar_empleado',methods=['POST',"GET"])
@login_required_admin
def editar_empleado(idtbl_empleado):
    empleado = get_empleado(idtbl_empleado)
    password_check =None
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        cargo = request.form['cargo']
        password = request.form['password']
        password_new = request.form['password_new']

        error = None
        
        db, c = get_db()
        c.execute('select * from tbl_empleado where dni = %s',(dni,))

        repeat_dni = c.fetchone()

        if not nombres:
            error = "Ingrese sus Nombres"
        if not apellidos:
            error = "Ingrese sus Apellidos"
        if not dni:
            error = "Ingrese el número de su documento"
        if dni != empleado['dni']:
            if repeat_dni is not None:
                error = "El dni ingresado ya esta registrado"
        if cargo is None:
            error= "Ingrese un cargo valido"

        if not password_new:
            error= None
        elif not check_password_hash(empleado['pass'],password):
            error= "La contraseña Anterior es incorrecta"
        else:
            c.execute('update tbl_empleado set nombres = %s, apellidos = %s, dni = %s, cargo = %s, pass = %s where idtbl_empleado = %s',(nombres,apellidos,dni,cargo,generate_password_hash(password_new),empleado['idtbl_empleado']))
            db.commit()

            
        
        if error is None:
            c.execute('update tbl_empleado set nombres = %s, apellidos = %s, dni = %s, cargo = %s where dni = %s',(nombres,apellidos,dni,cargo,empleado['dni']))
            db.commit()
            error = "se ha actualizado"
        
        flash(error)
    return render_template('admin/editar_empleado.html', empleado = empleado,password_check=password_check)
# Eliminar empleado

@bp.route('/<int:idtbl_empleado>/eliminar_empleado')
@login_required_admin
def eliminar_empleado(idtbl_empleado):
    db, c = get_db()
    c.execute('select * from tbl_empleado where idtbl_empleado = %s' % (idtbl_empleado,))
    empleado = c.fetchone()
    if empleado is None:
        abort(404,'El usuario a eliminar no existe')
    else:
        c.execute('delete from tbl_empleado where idtbl_empleado = %s' % (idtbl_empleado,))
        db.commit()
        return redirect(url_for('.lista_empleados'))

