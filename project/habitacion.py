from flask import g,render_template,url_for,redirect,request,flash,Blueprint


from werkzeug.exceptions import abort

from project.auth import login_required

from project.db import get_db

bp = Blueprint('habitacion',__name__,url_prefix='/habitacion')

# Lista Habitaciones 
@bp.route('/lista_habitaciones')
@login_required
def lista_habitaciones():
    db, c = get_db()
    c.execute('select * from tbl_habitacion where 1 ')
    habitaciones = c.fetchall()
    return render_template('habitacion/lista_habitaciones.html',habitaciones=habitaciones)

# Crear Habitacion

@bp.route('/crear_habitacion',methods=['POST','GET'])
@login_required
def crear_habitacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        valor = request.form['valor']
        capacidad = request.form['capacidad']
        estado = request.form['estado']
        descripcion = request.form['descripcion']

        error = None

        db,c = get_db()
        c.execute('select * from tbl_habitacion where nombre = %s',(nombre,))
        repeat_nombre = c.fetchone()

        if not nombre:
            error = 'Ingrese el nombre de la habitación'
        if repeat_nombre is not None:
            error = 'El nombre de la habitación ya esta registrado'
        if not valor:
            error = 'Ingrese el valor de la habitación'
        if not capacidad:
            error = 'Ingrese la capacidad de la habitación'
        # else:
            # if capacidad % 1 != 0:
            #     error ="La capacidad tiene que ser un numero entero"
        if not estado:
            error = 'Ingrese el estado de la habitación'
        if not descripcion:
            error = 'Ingrese una descripcion de la habitación'
        
        if error == None:
            c.execute('insert into tbl_habitacion (nombre,valor,capacidad,estado,descripcion) values(%s,%s,%s,%s,%s)',(nombre,valor,capacidad,estado,descripcion))
            db.commit()
            return redirect(url_for('habitacion.lista_habitaciones'))
        flash(error)
    return render_template('habitacion/crear_habitacion.html')

# Conseguir habitacion
def get_habitacion(idtbl_habitacion):
    db, c = get_db()
    c.execute('select * from tbl_habitacion where idtbl_habitacion = %s',(idtbl_habitacion,))
    datos_habitacion = c.fetchone()
    if datos_habitacion is None:
        abort(404,'La habitacion que desea editar no existe')
    else:
        return datos_habitacion

# editar habitacion

@bp.route('/<int:idtbl_habitacion>/editar_habitacion',methods=['POST','GET'])
@login_required
def editar_habitacion(idtbl_habitacion):
    habitacion = get_habitacion(idtbl_habitacion)
    if request.method == 'POST':
        nombre = request.form['nombre']
        valor = request.form['valor']
        capacidad = request.form['capacidad']
        descripcion = request.form['descripcion']
        estado = request.form['estado']

        db,c = get_db()
        c.execute('select* from tbl_habitacion where nombre = %s',(nombre,))
        nombre_repeat = c.fetchone()

        error = None

        if not nombre:
            error = 'Ingrese el nombre de la habitación'
        if nombre != habitacion['nombre']:
            if nombre_repeat is not None:
                error = 'El nombre ya esta registrado'
        if not valor:
            error = 'Ingrese el valor de la habitación'
        if not capacidad:
            error = 'Ingrese la capacidad de la habitación'
        if not descripcion:
            error = 'Ingrese la descripcion de la habitación'
        if not estado:
            error = 'Ingrese el estado de la habitación'

        if error is None:
            c.execute("update tbl_habitacion set nombre=%s ,valor=%s,capacidad= %s,estado = %s,descripcion=%s where idtbl_habitacion = %s",(nombre,valor,capacidad,estado,descripcion,habitacion['idtbl_habitacion']))
            db.commit()
            return redirect(url_for('habitacion.lista_habitaciones'))
        flash(error)
    return render_template('habitacion/editar_habitacion.html',habitacion=habitacion)


# eliminar habitacion

@bp.route('/<int:idtbl_habitacion>/eliminar habitacion')
@login_required
def eliminar_habitacion(idtbl_habitacion):
    habitacion = get_habitacion(idtbl_habitacion)
    if habitacion is None:
        abort(404,'La habitacion que intenta eliminar no existe')
    else:
        db,c = get_db()
        c.execute('delete from tbl_habitacion where idtbl_habitacion = %s',(habitacion['idtbl_habitacion'],))
        db.commit()
        return redirect(url_for('habitacion.lista_habitaciones'))
