# coding=utf-8

__author__ = 'Miguel Antonio'

import datetime


#Definición de las tablas de la aplicación con sus funciones disparadaras (Triggers) y restricciones
#-------------------------------------------------------------------------------------------------------#
#Tabla Aspectos
db.define_table('aspectos',
                Field('aspecto', 'string', required=True, unique=True, label=T('Aspect')),
                format='%(aspecto)s')
#Triggers

#Restricciones
db.aspectos.id.readable = False
db.aspectos.id.writable = False

#-------------------------------------------------------------------------------------------------------#
#Tabla Solicitudes
db.define_table('solicitudes',
                Field('proyecto', 'string', required=True, label=T('Strategy Proyect name'), requires=IS_NOT_EMPTY()),
                Field('archivos', 'upload', required=True, label=T('File'), requires=IS_NOT_EMPTY(),
                      autodelete=True, uploadseparate=True),
                Field('estado', default="Pendiente",
                      requires=IS_IN_SET(['Pendiente', 'Rechazada', 'Cancelada', 'Evaluándose',
                                          'Evaluada']), label=T('State')),
                Field('fecha', 'datetime', default=datetime.datetime.now(), label=T('Create date')),
                Field('publico', required=True, label=T('Public'),
                      requires=IS_IN_SET(['Si', 'No']), default='Si'),
                Field('observaciones', 'text', default='Sin observaciones', label=T('Observations')),
                Field('id_usuario', 'reference auth_user', required=True, default=auth.user_id, label=T('User')),
                format='%(proyecto)s')
#Triggers
def solicitudes_before_insert(f):
    consulta = db(db.solicitudes.proyecto == f['proyecto']).count()
    if consulta > 0:
        return True

def solicitudes_after_update(s, f):
    if f['estado'] == 'Evaluándose':
        conteo = db(db.auth_membership.group_id == 2).count()
        if conteo > 6:
            expertos = db(db.auth_membership.group_id == 2).select(db.auth_membership.user_id)
            solicitud = db.solicitudes(f['id'])
            for experto in expertos:
                db.expertosasociados.insert(id_usuario=experto.user_id, id_solicitudes=solicitud.id)
            expertos = db(db.expertosasociados.id_solicitudes == solicitud.id).select(
            db.expertosasociados.ALL)
            aspectos = db(db.aspectossolicitud.id_solicitudes == solicitud.id).select(db.aspectossolicitud.ALL)
            for aspecto in aspectos:
                for experto in expertos:
                    db.evaluaciones.insert(id_solicitudes=solicitud.id, id_aspectossolicitud=aspecto.id,
                                       id_experto=experto.id)
        else:
            c = (db.solicitudes.id == f['id'])
            miset = db(c)
            miset.update(estado="Cancelada", observaciones='La cantidad de expertos existentes no es suficiente para evaluar esta solicitud')

#Restricciones
db.solicitudes.fecha.writable = False
db.solicitudes.publico.requires = IS_IN_SET(('Si', 'No'))
db.solicitudes.observaciones.writable = False
db.solicitudes.id_usuario.writable = False
db.solicitudes.id.readable = False
db.solicitudes.id.writable = False
db.solicitudes.estado.writable = False
db.solicitudes.publico.readable = False
db.solicitudes._after_update.append(solicitudes_after_update)
db.solicitudes._before_insert.append(solicitudes_before_insert)
#-------------------------------------------------------------------------------------------------------#

#Tabla Aspectos-solicitudes
db.define_table('aspectossolicitud',
                Field('id_solicitudes', 'reference solicitudes', required=True,
                      label=T('Proyect name')),
                Field('id_aspecto', 'reference aspectos', label=T('Aspect to evaluate'), required=True),
                Field('evaluacionfinal', default='',
                      requires=IS_IN_SET(['Muy Mal', 'Mal', 'Regular', 'Bien', 'Muy Bien']),
                      label="Evaluación Final"),
                format=lambda row: row.id_aspecto.aspecto)
#Triggers
# def aspectossolicitud_before_insert(f):
#     print(f)
#     solicitud = f['id_solicitudes']
#     aspecto = f['id_aspecto']
#     conteo = db(
#         (db.aspectossolicitud.id_solicitudes == solicitud) & (db.aspectossolicitud.id_aspecto == aspecto)).count()
#     print(conteo)
#     if conteo > 0:
#         return True

#Restricciones
db.aspectossolicitud.id_solicitudes.requires = IS_IN_DB(db, db.solicitudes, '%(proyecto)s')
db.aspectossolicitud.id_aspecto.requires = IS_IN_DB(db, db.aspectos, '%(aspecto)s')
db.aspectossolicitud.id.writable = False
db.aspectossolicitud.id.readable = False
# db.aspectossolicitud._before_insert.append(aspectossolicitud_before_insert)
#-------------------------------------------------------------------------------------------------------#

#Tabla expertosasociados
db.define_table('expertosasociados',
                Field('id_solicitudes', 'reference solicitudes', required=True, label=T('Proyect name')),
                Field('id_usuario', 'reference auth_user', required=True, default=auth.user_id, label=T('User')),
                format='%(id_usuario)s')
#Triggers

#Restricciones
db.expertosasociados.id_solicitudes.requires = IS_IN_DB(db, db.solicitudes, '%(proyecto)s')
db.expertosasociados.id.readable = False
db.expertosasociados.id.writable = False
#-------------------------------------------------------------------------------------------------------#

#Tabla Evaluaciones
db.define_table('evaluaciones',
                Field('id_solicitudes', 'reference solicitudes', required=True, label=T('Proyect name'),
                      writable=0),
                Field('id_aspectossolicitud', 'reference aspectossolicitud', label=T('Aspect'), writable=0),
                Field('id_experto', 'reference expertosasociados', label=T('Expert')),
                Field('evaluacion', default='Sin evaluación',
                      requires=IS_IN_SET(['Muy Mal', 'Mal', 'Regular', 'Bien', 'Muy Bien']),
                      label=T('Evaluation')),
                Field('evaluacion2', default='Sin evaluación',
                      requires=IS_IN_SET(['Muy Mal', 'Mal', 'Regular', 'Bien', 'Muy Bien']),
                      label="Evaluación en ronda 2"),
                Field('ronda', default=1),
                Field('delphi', 'string', default='Sin ejecutar'))

#Triggers

#Restricciones
db.evaluaciones.id_experto.readable = False
db.evaluaciones.id_experto.writable = False
db.evaluaciones.id.writable = False
db.evaluaciones.id.readable = False
db.evaluaciones.id_solicitudes.requires = IS_IN_DB(db, db.solicitudes, '%(proyecto)s')
#-------------------------------------------------------------------------------------------------------#

#Tabla del inverso de la distribución normal estándar acumulativa de los valores probabilísticos entre 0 y 1
db.define_table('valores',
                Field('valor', 'float', unique=True),
                Field('idnea', 'float'))


db.define_table('tabla1',
                Field('year','integer',unique=True, label=T('Year')),
                Field('azucar','float', label=T('Sugar')),
                Field('cacao','float', label=T('Cacao')),
                Field('cafe','float', label=T('Coffee')),
                Field('copra','float', label=T('Copra')))

db.tabla1.id.writable = False
db.tabla1.id.readable = False

db.define_table('tabla2',
                Field('producto','text', label=T('Product')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))

db.define_table('tabla3',
                Field('producto','text', label=T('Product')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))

db.define_table('tabla4',
                Field('producto','text', label=T('Product')),
                Field('destino','text', label=T('Destiny')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))

db.define_table('tabla5',
                Field('producto','text', label=T('Product')),
                Field('origen','text', label=T('Origin')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))

db.define_table('tabla6',
                Field('producto','text', label=T('Product')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))

db.define_table('tabla7',
                Field('producto','text', label=T('Product')),
                Field('year','integer', label=T('Year')),
                Field('kilogramos','string',default='0', label=T('Kilograms')),
                Field('valor','string',default='0', label=T('Value')))
