# coding=utf-8
__author__ = 'Miguel Antonio'

mostrarmenu2()
from gluon.tools import Crud
crud = Crud(db)
crud.settings.controller = 'solicitudes'
db.aspectossolicitud.evaluacionfinal.writable = 0
KEY = 's7gr2a8x7vc0aq' #clave usada para la codificación de las URL

def index():
    redirect(URL(c='default', f='index'))
    return

def solicitudespublicas():
    db.solicitudes.estado.readable = True
    form = SQLFORM.grid(db.solicitudes.publico == "Si", editable=False, csv=0, create=False, deletable=False,
                        paginate=10,
                        buttons_placement='right',
                        user_signature=0,
                        links=[dict(header="",
                                    body=lambda row: A(T('Evaluation'), _href=URL('mostrar_evaluaciones', args=row.id, hmac_key=KEY)))]
    )
    return dict(form=form)

def mostrar_evaluaciones():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    id_solicitud = request.args(0)
    form = SQLFORM.grid(db.aspectossolicitud.id_solicitudes == id_solicitud, editable=False, create=False, paginate=10,
                        user_signature=0, deletable=False, )
    return dict(form=form)

@auth.requires_login()
def nuevasolicitud():
    form1 = SQLFORM(db.solicitudes, submit_button=T('Next'))
    if form1.process().accepted:
        session.flash = T('Request added')
        redirect(URL('aspectos', args=form1.vars.id, hmac_key=KEY))
    elif form1.errors:
        response.flash = T('Please, complete data solicited in the form.')
    return dict(form1=form1)

@auth.requires_login()
def missolicitudes():
    form2 = SQLFORM.grid(db.solicitudes.id_usuario == auth.user_id, csv=0, paginate=10, create=0,
                         links=[dict(header="",
                                     body=lambda row: A(T('Evaluation'), _href=URL('mostrar_evaluaciones', args=row.id, hmac_key=KEY))),
                                dict(header="",
                                     body=lambda row: A(T('Aspects'), _href=URL('aspectos_por_solicitud', args=row.id, hmac_key=KEY)))])
    return dict(form2=form2)

@auth.requires_login()
def aspectos():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    id_solicitud = request.args(0)
    t = db.aspectossolicitud
    t.evaluacionfinal.readable = False
    t.evaluacionfinal.writable = False
    t.id_solicitudes.readable = True
    t.id_solicitudes.writable = False
    t.id_solicitudes.default = id_solicitud
    excluyea = db(db.aspectossolicitud.id_solicitudes == id_solicitud)
    t.id_aspecto.requires = IS_IN_DB(db(
        (db.aspectos.id > 0)), db.aspectos.id, '%(aspecto)s')
        # ,_and=IS_NOT_IN_DB(excluyea, 'aspectossolicitud.id_aspecto'))
    form1 = SQLFORM(t, submit_button=T('Insert'))
    existe = db(db.aspectossolicitud.id_solicitudes==id_solicitud).count()

    if existe == 0:
        form1.add_button(T('Add all'), URL('agregar_todos', args=id_solicitud, hmac_key=KEY))
    form1.add_button(T('Finish'), URL('aspectos_por_solicitud', args=id_solicitud, hmac_key=KEY))
    if form1.process().accepted:
        existe = db((db.aspectossolicitud.id_aspecto == form1.vars.id_aspecto) & (
            db.aspectossolicitud.id_solicitudes == id_solicitud)).count()
        if existe > 1:
            response.flash = T('Error, this aspect already exist')
            x = form1.vars.id
            db(db.aspectossolicitud.id == x).delete()
    # form2 = SQLFORM.grid(db.aspectossolicitud.id_solicitudes==id_solicitud,create=0,editable=0)
    return dict(form1=form1)

@auth.requires_login()
def agregar_todos():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    id_solicitud = request.args(0)
    aspectos = db(db.aspectos).select(db.aspectos.id)
    for aspecto in aspectos:
        db.aspectossolicitud.insert(id_solicitudes=id_solicitud, id_aspecto = aspecto.id, evaluacionfinal= '')
    session.flash = T('All the aspects are inserted')
    redirect(URL('aspectos_por_solicitud', args=id_solicitud, hmac_key=KEY))

@auth.requires_login()
def aspectos_por_solicitud():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    id_solicitud = request.args(0)
    db.aspectossolicitud.id_solicitudes.writable = False
    consulta = (db.aspectossolicitud.id_solicitudes == id_solicitud)
    conteo = db((db.solicitudes.id == id_solicitud) & ((db.solicitudes.estado == "Pendiente") | (
    db.solicitudes.estado == "Rechazada")| (db.solicitudes.estado == "Cancelada"))).count()
    if conteo > 0:
        aspectos_seleccionados = SQLFORM.grid(consulta, user_signature=False, create=0, editable=0, deletable=0,
                                                  links=[dict(header="",
                                                              body=lambda row: A('Agregar aspecto',
                                                                                 _href=URL('agregar_aspectos',
                                                                                           args=(row.id_solicitudes,
                                                                                                 row.id_aspecto), hmac_key=KEY))),
                                                         dict(header="",
                                                              body=lambda row: A('Eliminar',
                                                                                 _href=URL(c='solicitudes',f='borrar_aspecto',
                                                                                           args=(row.id), hmac_key=KEY))),
                                                         dict(header="",
                                                              body=lambda row: A('Editar aspecto',
                                                                                 _href=URL('editar_aspecto',
                                                                                           args=(row.id_solicitudes,
                                                                                                 row.id_aspecto), hmac_key=KEY)))])
    else: redirect (URL("solicitudes", "aspectos_no_editables"))
    return dict(aspectos_seleccionados=aspectos_seleccionados)


def borrar_aspecto():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    x = request.args(0)
    crud.settings.controller = 'solicitudes'
    crud.settings.captcha = None
    solicitud = db(db.aspectossolicitud.id==x).select(db.aspectossolicitud.id_solicitudes)
    j = solicitud[0]
    solicitud = db(db.solicitudes.id==j['id_solicitudes']).select(db.solicitudes.id)
    solicitud = solicitud[0]
    crud.settings.delete_next = URL('aspectos_por_solicitud',args=solicitud['id'],hmac_key=KEY)
    formulario=crud.delete(db.aspectossolicitud, x)
    return dict(formulario=formulario)

def aspectos_no_editables():
    return locals()

def agregar_aspectos():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    db.aspectossolicitud.id_solicitudes.writable = 0
    id_solicitud = request.args(0)
    t = db.aspectossolicitud
    t.id_solicitudes.default = id_solicitud
    t.id_aspecto.requires = IS_IN_DB(db(
        (db.aspectos)
    ), db.aspectos.id, '%(aspecto)s')
    form1 = SQLFORM(t, submit_button='Insertar', showid=0)
    form1.add_button('Regresar', URL('aspectos_por_solicitud', args=id_solicitud, hmac_key=KEY))
    if form1.process(keepvalues=True,detect_record_change=True).accepted:
        existe = db((db.aspectossolicitud.id_aspecto == form1.vars.id_aspecto) & (
            db.aspectossolicitud.id_solicitudes == id_solicitud)).count()
        response.flash = T('Completed!')
        if existe > 1:
            response.flash = T('Error, this aspect already exist')
            x = form1.vars.id
            db(db.aspectossolicitud.id == x).delete()
    return dict(form1=form1)


def editar_aspecto():
    if not URL.verify(request, hmac_key=KEY): redirect(URL('missolicitudes'))
    db.aspectossolicitud.id_solicitudes.writable = 0
    id_solicitud = request.args(0)
    aspecto = request.args(1)
    t = db.aspectossolicitud
    t.id_solicitudes.default = id_solicitud
    t.id_aspecto.default = aspecto
    t.id_aspecto.requires = IS_IN_DB(db(
        (db.aspectos)
    ), db.aspectos.id, '%(aspecto)s')
    form1 = SQLFORM(t, submit_button='Cambiar', showid=0,)
    form1.add_button('Regresar', URL('aspectos_por_solicitud', args=id_solicitud, hmac_key=KEY))
    if form1.process(keepvalues=True,detect_record_change=True).accepted:
        existe = db((db.aspectossolicitud.id_aspecto == form1.vars.id_aspecto) & (
            db.aspectossolicitud.id_solicitudes == id_solicitud)).count()
        response.flash = T('Aspect changed')
        if existe > 1:
            response.flash = T('Error, this aspect already exist')
            x = form1.vars.id
            db(db.aspectossolicitud.id == x).delete()
        else:
            db((db.aspectossolicitud.id == id_solicitud) and (db.aspectossolicitud.id_aspecto == aspecto)).delete()
    return dict(form1=form1)
