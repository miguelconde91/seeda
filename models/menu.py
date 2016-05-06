# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################


response.logo = A(B('SEEDA'),
                  _class="brand", _href="http://10.53.3.56:8000/seeda/default/index")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Miguel Antonio Conde'
response.meta.keywords = 'web2py, python, framework, UCI, Delphi,Agricultura'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Menu'), False, URL(""), [
        (T('Home'), False, URL('default', 'index')),
        (T('Up strategy'), False, URL("solicitudes", "nuevasolicitud" )),
        (T('My strategies'), False, URL("solicitudes", "missolicitudes")),
        (T('Published strategies'), False, URL('solicitudes', "solicitudespublicas")),
        (T('Help'), False, URL('default', 'ayuda'))
    ]),
    (T('Tables'), False, URL(""),[
        (T('Principal products'),False, URL('default','tabla1')),
        (T('Imported fertilizers'),False, URL('default','tabla2')),
        (T('Exported fertilizers'),False, URL('default','tabla3')),
        (T('Imported insecticides'),False, URL('default','tabla4')),
        (T('Exported insecticides'),False, URL('default','tabla5')),
        (T('Imported machinaries'),False, URL('default','tabla6')),
        (T('Exported machinaries'),False, URL('default','tabla7'))
    ])
]

#Cambiarlo a falso una vez terminada la aplicacion
DEVELOPMENT_MENU = False
response.menuespecial = []


#Menú de rol para todas las páginas de la app excepto index
def mostrarmenu2():
    if auth.user is None:
        pass
    elif auth.has_membership(user_id=auth.user_id, role="Administrador"):
        response.menuespecial = [
            (T('Administration'), False, None, [
                (T('Users'), False, URL("administrar", "usuarios")),
                (T('Strategies'), False, URL("administrar", "solicitudes")),
                (T('Aspects'), False, URL("administrar", "aspectos"))
            ])
        ]
    elif auth.has_membership(user_id=auth.user_id, role="Experto"):
        response.menuespecial = [
            (T('Experts'), False, None, [
                ("Evaluar en ronda 1", False, URL("experto", "evaluar")),
                ("Evaluar en ronda 2", False, URL("experto", "evaluar2")),
                (T('My evaluations'), False, URL("experto", "mis_evaluaciones"))
            ])
        ]

#Menú de rol para el index de la app que incluye la notificación a usuarios sobre el estado de sus solicitudes,
#a expertos sobre las solicitudes pendientes a evaluar y al admin sobre las solicitudes pendientes a revisar
def mostrarmenu():
    if ~auth.has_membership(user_id=auth.user_id, role="Experto") and ~auth.has_membership(user_id=auth.user_id,
                                                                                           role="Administrador") and auth.user_id > 0:
        r = db((db.solicitudes.estado == "Rechazada") & (db.solicitudes.id_usuario == auth.user_id)).count()
        a = db((db.solicitudes.estado == "Aceptada") & (db.solicitudes.id_usuario == auth.user_id)).count()
        c = db((db.solicitudes.estado == "Cancelada") & (db.solicitudes.id_usuario == auth.user_id)).count()
        if c > 0:
            response.flash = "Tiene " + str(r) + " solicitud(es) rechazada(s), " + str(
                a) + " solicitud(es) aceptada(s) y " + str(
                c) + " solicitud(es) cancelada(s)"
        if r > 0 or a > 0:
            response.flash = "Tiene " + str(r) + " solicitud(es) rechazada(s) y " + str(
                a) + " solicitud(es) aceptada(s)"
    if auth.user is None:
        pass
    elif auth.has_membership(user_id=auth.user_id, role="Administrador"):
        response.menuespecial = [
            (T('Administration'), False, None, [
                (T('Users'), False, URL("administrar", "usuarios")),
                (T('Strategies'), False, URL("administrar", "solicitudes")),
                (T('Aspects'), False, URL("administrar", "aspectos"))
            ])
        ]
        p = db(db.solicitudes.estado == "Pendiente").count()
        if p == 1:
            response.flash = "Hay 1 solicitud pendiente, por favor revísela"
        elif p > 1:
            response.flash = "Hay " + str(p) + " solicitudes pendientes"
        else:
            response.flash = "No hay solicitudes por revisar"
    elif auth.has_membership(user_id=auth.user_id, role="Experto"):
        id_expertos = db(db.expertosasociados.id_usuario == auth.user_id).select(db.expertosasociados.id)
        r1 = 0

        for id_experto in id_expertos:
            conteo_en_r1 = db(
                (db.evaluaciones.id_experto == id_experto) & (db.evaluaciones.evaluacion == "Sin evaluación")).count()
            r1 += conteo_en_r1
        if r1 > 0:
            response.flash = "Evaluación(es) pendientes: " + str(r1) + ""
        else:
            response.flash = "No tiene nada pendiente"
        response.menuespecial = [
            (T('Experts'), False, None, [
                ("Evaluar en ronda 1", False, URL("experto", "evaluar")),
                ("Evaluar en ronda 2", False, URL("experto", "evaluar2")),
                (T('My evaluations'), False, URL("experto", "mis_evaluaciones"))
            ])
        ]


if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
