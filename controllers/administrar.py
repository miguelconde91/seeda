# coding=utf-8


__author__ = 'Miguel Antonio'

mostrarmenu2()

db.evaluaciones.evaluacion.writable = False
db.evaluaciones.delphi.writable = False
db.aspectossolicitud.evaluacionfinal.writable = False


def index():
    redirect(URL(c='default', f='index'))
    return


@auth.requires_membership(role="Administrador")
def usuarios():
    notificacion = request.args(0)
    if notificacion == '1':
        response.flash = "Rol cambiado"
    form = SQLFORM.grid(db.auth_user, paginate=0, links=[dict(header="",
                                                              body=lambda row: A('Editar grupo',
                                                                                 _href=URL(
                                                                                     'editar_grupo',
                                                                                     args=row.id)))], create=1,
                        editable=1, user_signature=0)
    return dict(form=form)


@auth.requires_membership(role="Administrador")
def editar_grupo():
    id_user = request.args(0)
    t = db.auth_membership
    consulta = db(t.user_id == id_user).select(t.group_id)
    for c in consulta:
        t.group_id.default = c.group_id
    t.user_id.default = id_user
    form1 = SQLFORM(t, submit_button='Cambiar', showid=0)
    if form1.process().accepted:
        existe = db((t.user_id == form1.vars.user_id)).count()
        if existe > 1:
            db((t.user_id == form1.vars.user_id) & (t.group_id != form1.vars.group_id)).delete()
        redirect(URL('usuarios', args=1))
    return dict(form1=form1)


@auth.requires_membership(role="Administrador")
def aspectos():
    form3 = SQLFORM.grid(db.aspectos, paginate=10)
    return dict(form3=form3)


@auth.requires_membership(role="Administrador")
def solicitudes():
    mostrar_solicitudes = (db.solicitudes.estado == 'Pendiente') | (db.solicitudes.estado == 'Cancelada') | (
        db.solicitudes.estado == 'Rechazada')
    db.solicitudes.estado.writable = True
    db.solicitudes.estado.readable = True
    db.solicitudes.publico.writable = False
    db.solicitudes.observaciones.writable = True
    db.solicitudes.estado.requires = IS_IN_SET(['Evaluándose', 'Rechazada'])
    form4 = SQLFORM.grid(mostrar_solicitudes, create=False, paginate=10, links=[dict(header="",
                                                                                     body=lambda row: A(
                                                                                         T('Aspects to evaluate'),
                                                                                         _href=URL(
                                                                                             'aspectos_por_solicitud',
                                                                                             args=row.id)))])
    return dict(form4=form4)


@auth.requires_membership(role="Administrador")
def aspectos_por_solicitud():
    id_solicitud = request.args(0)
    db.aspectossolicitud.id_solicitudes.writable = False
    if id_solicitud == 'view' or id_solicitud == 'delete' or id_solicitud == 'edit' or id_solicitud == 'new':
        id_solicitud = request.args(2)
        consulta = (db.aspectossolicitud.id == id_solicitud)
        aspectos_seleccionados = SQLFORM.grid(consulta, user_signature=False)
    else:
        consulta = (db.aspectossolicitud.id_solicitudes == id_solicitud)
        conteo = db((db.solicitudes.id == id_solicitud) & ((db.solicitudes.estado == "Pendiente") | (
            db.solicitudes.estado == "Rechazada") | (db.solicitudes.estado == "Cancelada"))).count()
        aspectos_seleccionados = SQLFORM.grid(consulta, user_signature=False, create=0, editable=0, deletable=0)
        if conteo > 0:
            aspectos_seleccionados = SQLFORM(consulta, user_signature=False, create=0, editable=0,deletable=0)
            return dict(aspectos_seleccionados=aspectos_seleccionados)