from flask import g, Blueprint, render_template, url_for, redirect, flash, request

from project.auth import login_required

from werkzeug.exceptions import abort

from project.db import get_db

bp = Blueprint('cliente',__name__,url_prefix="/cliente")

# Conseguir nacionalidad
def paises():
    db,c = get_db()
    c.execute('select * from tbl_paises where 1')
    g.paises = c.fetchall()
    return g.paises

# Mostrar clientes
@bp.route('/lista_cliente',methods = ['POST','GET'])
@login_required
def lista_clientes():
    db,c = get_db()
    paises()
    c.execute('select * from tbl_cliente where 1')
    clientes = c.fetchall()
    return render_template('cliente/lista_clientes.html',clientes=clientes)

# Crear cliente
@bp.route('/crear_cliente', methods = ['POST','GET'])
@login_required
def crear_cliente():
    paises()
    if request.method == 'POST':
        dni = request.form['dni']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nacionalidad = request.form['nacionalidad']

        error = None

        db,c = get_db()


        c.execute('select * from tbl_cliente where dni = %s',(dni,))
        dniRegistrado = c.fetchone()

        if not dni:
            error= 'Ingrese el documento del cliente'
        if not nombres:
            error='Ingrese el nombre del cliente'
        if not apellidos:
            error = 'Ingrese el apellido del cliente'
        if not fecha_nacimiento:
            error = 'Ingrese la fecha de nacimiento del cliente'
        if not nacionalidad:
            error = 'Ingrese la nacionalidad del cliente'
        if dniRegistrado is not None:
            error = 'El usuario ya esta registrado'

        if error is None:
            c.execute('insert into tbl_cliente(dni, nombres, apellidos, fecha_nacimiento, nacionalidad) values (%s,%s,%s,%s,%s)',(dni,nombres,apellidos,fecha_nacimiento,nacionalidad))
            db.commit()
            return redirect(url_for('cliente.lista_clientes'))
        
        flash(error)
    return render_template('cliente/crear_cliente.html',paises=paises)

# Conseguir cliente a editar
def get_cliente(idtbl_cliente):
    db,c = get_db()
    c.execute('select * from tbl_cliente where idtbl_cliente = %s',(idtbl_cliente,))
    datos_cliente = c.fetchone()
    if datos_cliente is None:
        abort(404,'El cliente a editar no exite')
    else:
        return datos_cliente

# Editar cliente
@bp.route('/<int:idtbl_cliente>/editar_cliente',methods =['POST','GET'])
@login_required
def editar_cliente(idtbl_cliente):
    paises()
    cliente = get_cliente(idtbl_cliente)
    if request.method == 'POST':
        dni = request.form['dni']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nacionalidad = request.form['nacionalidad']

        error = None
        db, c = get_db()

        c.execute('select * from tbl_cliente where dni = %s',(dni,))
        dniRepetido = c.fetchone()

        if not dni:
            error = 'Ingrese el dni del cliente'
        if dni != cliente['dni']:
            if dniRepetido is not None:
                error = 'El documento ya esta registrado'
        if not nombres:
            error = 'Ingrese los nombres del cliente'
        if not apellidos:
            error = 'Ingrese los apellidos del cliente'
        if not fecha_nacimiento:
            error = 'Ingrese la fecha nacimiento del cliente'
        if not nacionalidad:
            error = 'Ingrese su nacionalidad'
        
        if error is None:
            c.execute('update tbl_cliente set nombres = %s, apellidos = %s, dni = %s, fecha_nacimiento = %s, nacionalidad = %s where dni = %s',(nombres,apellidos,dni,fecha_nacimiento,nacionalidad,cliente['dni']))
            db.commit()
            return redirect(url_for('cliente.lista_clientes'))
        flash(error)
    return render_template('cliente/editar_cliente.html',cliente=cliente)


# Eliminar cliente
@bp.route('/<int:idtbl_cliente>/eliminar_cliente')
@login_required
def eliminar_cliente(idtbl_cliente):
    db,c = get_db()
    c.execute('select * from tbl_cliente where idtbl_cliente = %s',(idtbl_cliente,))
    cliente = c.fetchone()
    if cliente is not None:
        c.execute('delete from tbl_cliente where idtbl_cliente = %s',(idtbl_cliente,))
        db.commit()
        return redirect(url_for('cliente.lista_clientes'))
    else:
        abort(404,'El cliente que desea eliminar no existe')
    





