from project import habitacion
from flask import g,render_template,redirect,request,url_for,Blueprint,flash

from werkzeug.exceptions import LengthRequired, abort

from project.auth import login_required

from project.db import get_db

bp = Blueprint('reserva',__name__,url_prefix='/reserva')

# Ver reservas
@bp.route('/lista_reservas',methods=['POST','GET'])
@login_required
def lista_reservas():
    db, c = get_db()

    c.execute('select * from tbl_cliente_reserva where 1')
    relaciones = c.fetchall()

    c.execute('select * from tbl_cliente where 1')
    clientes = c.fetchall()

    c.execute('select * from tbl_reserva where 1')
    reservas = c.fetchall()

    c.execute('select * from tbl_habitacion where 1')
    habitaciones = c.fetchall()

    c.execute('select * from tbl_empleado where 1')
    empleados = c.fetchall()



    return render_template('reserva/lista_reservas.html',relaciones = relaciones, clientes = clientes, reservas = reservas,habitaciones = habitaciones,empleados=empleados)

# Crear Reserva

@bp.route('/crear_reserva',methods=["POST",'GET'])
@login_required
def crear_reserva():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        estado = request.form['estado']
        habitacion = request.form['habitacion']
        empleado = g.user['idtbl_empleado']

        tamClientes = request.form['tam-clientes']
        tamClientes = int(tamClientes)
        i=1
        clientes = []
        while( i <= tamClientes):
            stringCliente = str(i)
            cliente = request.form.get(stringCliente)
            clientes.append(cliente)
            i=i+1

        error = None
        

        db, c = get_db()
        
        # Conseguir datos de la habitacion
        c.execute('select * from tbl_habitacion where idtbl_habitacion = %s',(habitacion,))
        datos_habitacion = c.fetchone()

        # Comprobar Clientes
        i = 0
        clientesMalos = []
        if(tamClientes>1):
            while(i<tamClientes):
                c.execute('select * from tbl_cliente where dni = %s',(clientes[i],))
                clienteMalo = c.fetchone()
                if(clienteMalo is None):
                    clientesMalos.append(clientes[i])
                i=i+1

        if not fecha_inicio:
            error = 'Ingrese la fecha de inicio'
        if not fecha_fin:
            error = 'Ingrese la fecha de fin'
        if not estado:
            error = 'Ingrese El estado de la reserva'
        if not habitacion:
            error = "Ingrese la habitacion de la reserva"
        elif datos_habitacion is None:
            error= 'Ingrese una habitacion valida'
        if not empleado:
            error = 'Ingrese el empleado que hizo la reserva'
        if len(clientesMalos)>0:
            error = 'Los siguientes clientes no estan registrados'+clientesMalos[0]


        if error is None:
            c.execute('insert into tbl_reserva(fecha_inicio,fecha_fin,estado,habitacion,empleado) values (%s,%s,%s,%s,%s)',(fecha_inicio,fecha_fin,estado,habitacion,empleado))
            db.commit()
            c.execute('SELECT MAX(idtbl_reserva) FROM tbl_reserva')
            idtbl_reserva = c.fetchone()
            i=0
            while(i<tamClientes):
                c.execute('select * from tbl_cliente where dni = %s ',(clientes[i],))
                cliente = c.fetchone()
                c.execute('insert into tbl_cliente_reserva(cliente,reserva) values (%s,%s)',(str(cliente['idtbl_cliente']),str(idtbl_reserva['MAX(idtbl_reserva)'])))
                db.commit()
                i=i+1

            return redirect(url_for('reserva.lista_reservas'))
        flash(error)
    return render_template('reserva/crear_reserva.html')

# Conseguir reserva
def get_reserva(idtbl_reserva):
    db,c = get_db()
    c.execute('select * from tbl_reserva where idtbl_reserva = %s',(idtbl_reserva,))
    datos_reserva = c.fetchone()
    if not datos_reserva:
        abort(404,'No se encontro la habitacion')
    else:
        return datos_reserva


@bp.route('/<int:idtbl_reserva>/editar_reserva',methods=["POST","GET"])
@login_required
def editar_reserva(idtbl_reserva):
    # Consiguiendo la reserva
    reserva = get_reserva(idtbl_reserva)
    # Consiguiendo los CLientes
    db,c = get_db()
    # Consiguiendo los CLientes
    c.execute('select * from tbl_cliente where 1') 
    clientes = c.fetchall()
    # Consiguiendo la relacion
    c.execute('select * from tbl_cliente_reserva where reserva = %s',(reserva['idtbl_reserva'],))
    relacion = c.fetchall()
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        estado = request.form['estado']
        habitacion = request.form['habitacion']
        empleado = g.user['idtbl_empleado']

        tamClientes = request.form['tam-clientes']
        tamClientes = int(tamClientes)
        i=1
        clientes = []
        while( i <= tamClientes):
            stringCliente = str(i)
            cliente = request.form.get(stringCliente)
            clientes.append(cliente)
            i=i+1

        error = None
        

        db, c = get_db()
        
        # Conseguir datos de la habitacion
        c.execute('select * from tbl_habitacion where idtbl_habitacion = %s',(habitacion,))
        datos_habitacion = c.fetchone()

        # Comprobar Clientes
        i = 0
        clientesMalos = []
        if(tamClientes>1):
            while(i<tamClientes):
                c.execute('select * from tbl_cliente where dni = %s',(clientes[i],))
                clienteMalo = c.fetchone()
                if(clienteMalo is None):
                    clientesMalos.append(clientes[i])
                i=i+1

        if not fecha_inicio:
            error = 'Ingrese la fecha de inicio'
        if not fecha_fin:
            error = 'Ingrese la fecha de fin'
        if not estado:
            error = 'Ingrese El estado de la reserva'
        if not habitacion:
            error = "Ingrese la habitacion de la reserva"
        elif datos_habitacion is None:
            error= 'Ingrese una habitacion valida'
        if not empleado:
            error = 'Ingrese el empleado que hizo la reserva'
        if len(clientesMalos)>0:
            error = 'Los siguientes clientes no estan registrados'+clientesMalos[0]


        if error is None:
            c.execute('UPDATE `tbl_reserva` SET ,`fecha_inicio`=%s,`fecha_fin`=%s,`estado`=%s,`habitacion`=%s,`empleado`=%s WHERE idtbl_reserva = %s',(fecha_inicio,fecha_fin,estado,habitacion,empleado,reserva['idtbl_reserva']))
            db.commit()
            c.execute('select * from tbl_cliente_reserva where reserva = %s',(reserva['idtbl_reserva'],))
            relacion = c.fetchall()
            i=0
            while(i<tamClientes):
                c.execute('select * from tbl_cliente where dni = %s ',(clientes[i],))
                cliente = c.fetchone()
                c.execute('insert into tbl_cliente_reserva(cliente,reserva) values (%s,%s)',(str(cliente['idtbl_cliente']),str(idtbl_reserva['MAX(idtbl_reserva)'])))
                db.commit()
                i=i+1

            return redirect(url_for('reserva.lista_reservas'))
        flash(error)
    return render_template('reserva/editar_reserva.html',reserva=reserva,clientes=clientes,relacion= relacion) 

@bp.route('/<int:idtbl_reserva>/eliminar_reserva')
@login_required
def eliminar_reserva(idtbl_reserva):
    reserva = get_reserva(idtbl_reserva)
    if reserva is None:
        abort(404,'La habitacion que desea eliminar no esta disponible')
    else:
        db, c = get_db()
        c.execute('delete from tbl_cliente_reserva where reserva = %s',(reserva['idtbl_reserva'],))
        c.execute('delete from tbl_reserva where idtbl_reserva = %s',(reserva['idtbl_reserva'],))
        db.commit()
        return redirect(url_for('.lista_reservas'))
    

        

