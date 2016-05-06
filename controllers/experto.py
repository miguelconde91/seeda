# coding=utf-8
__author__ = 'Miguel Antonio'

from gluon.tools import Expose

mostrarmenu2()


def index():
    redirect(URL(c='default', f='index'))
    return


@auth.requires_membership(role="Experto")
def evaluar():
    db.evaluaciones.id_solicitudes.readable = False
    db.evaluaciones.evaluacion2.readable = False
    db.evaluaciones.ronda.writable = False
    db.evaluaciones.delphi.readable = False
    db.evaluaciones.evaluacion2.writable = False
    db.evaluaciones.delphi.writable = False
    consulta = (db.evaluaciones.evaluacion == "Sin evaluación") & (
        db.evaluaciones.id_experto == db.expertosasociados.id) & (
                   db.expertosasociados.id_usuario == auth.user_id)
    form_evaluar = SQLFORM.grid(consulta, deletable=False, create=False, paginate=10, details=False,
                                field_id=db.evaluaciones.id)
    if request.args(0) == 'edit':
        formulario = form_evaluar.components[1]
        if formulario.process().accepted:
            aux2(request.args(2))
            redirect(URL(c='experto', f='evaluar'))
    return dict(form=form_evaluar)


@auth.requires_membership(role="Experto")
def evaluar2():
    db.evaluaciones.evaluacion2.readable = False
    db.evaluaciones.evaluacion2.writable = True
    db.evaluaciones.evaluacion.writable = 0
    db.evaluaciones.delphi.writable = 0
    consulta = (db.evaluaciones.evaluacion2 == "Sin evaluación") & (
        db.evaluaciones.id_experto == db.expertosasociados.id) & (
                   db.expertosasociados.id_usuario == auth.user_id)  & (
                   db.evaluaciones.ronda == 2)
    form_evaluar2 = SQLFORM.grid(consulta, create=False, user_signature=0, field_id=db.evaluaciones.id,
                                 deletable=False, paginate=10
    )
    if request.args(0) == 'edit':
        formulario = form_evaluar2.components[1]
        if formulario.process().accepted:
            aux2(request.args(2))
            redirect(URL(c='experto', f='evaluar2'))
    return dict(form=form_evaluar2)


@auth.requires_membership(role="Experto")
def ronda1():
    id_solicitud = request.args(0)
    id_aspecto = request.args(1)
    consulta = (db.evaluaciones.id_solicitudes == id_solicitud) & (
        db.evaluaciones.id_aspectossolicitud == id_aspecto) & (db.evaluaciones.evaluacion != "")
    form_ronda1 = SQLFORM.grid(consulta, user_signature=0, deletable=False, editable=False, paginate=10, create=False)
    return dict(form=form_ronda1)


@auth.requires_membership(role="Experto")
def mis_evaluaciones():
    db.evaluaciones.id_solicitudes.readable = False
    db.evaluaciones.ronda.readable = True
    consulta = (db.evaluaciones.evaluacion != 'Null') & (db.evaluaciones.id_experto == db.expertosasociados.id) & (
        db.expertosasociados.id_usuario == auth.user_id)
    form1 = SQLFORM.grid(consulta, deletable=False, create=False, details=False, paginate=10, editable=False)
    return dict(form1=form1)


def aux2(id_evaluacion):
    consulta = db(db.evaluaciones.id == id_evaluacion).select(db.evaluaciones.id_solicitudes,
                                                              db.evaluaciones.ronda).first()
    id_solicitud = consulta['id_solicitudes']
    print(id_solicitud)
    ronda = consulta['ronda']
    contar = db((db.evaluaciones.id_solicitudes == id_solicitud) & (db.evaluaciones.evaluacion == "Sin evaluación") & (
        db.evaluaciones.ronda == 1)).count()
    if ((contar == 0) & (ronda == "1")):
        delphi(id_solicitud)
        c = (db.solicitudes.id == id_solicitud)
        miset = db(c)
        miset.update(estado="En ronda 2")
        c2 = db(db.evaluaciones.id_solicitudes == id_solicitud).update(ronda=2)
    elif ((contar>0)&(ronda=="1")):
        return locals()
    contar = db((db.evaluaciones.id_solicitudes == id_solicitud) & (
            db.evaluaciones.ronda == 2) & (db.evaluaciones.evaluacion2 == "Sin evaluación")).count()
    if contar == 0:
        delphi(id_solicitud)
        c = (db.solicitudes.id == id_solicitud)
        miset = db(c)
        miset.update(estado="Evaluada")




def delphi(id_solicitud):

    #Consulta para obtener los datos sobre los que se va a trabajar
    evaluaciones = db(db.evaluaciones.id_solicitudes == id_solicitud) \
        .select(db.evaluaciones.id_solicitudes, db.evaluaciones.id_aspectossolicitud, db.evaluaciones.evaluacion,
                db.evaluaciones.delphi, orderby=db.evaluaciones.id_aspectossolicitud)
    cant_aspectos = db(db.evaluaciones.id_solicitudes == id_solicitud).select(
        db.evaluaciones.id_aspectossolicitud, groupby=db.evaluaciones.id_aspectossolicitud)
    print('eva, cant asp')
    print(evaluaciones,cant_aspectos)
    #Conteo de la cantidad de aspectos a evaluar y cantidad de evaluaciones emitidas
    contar_aspectos = 0
    for cant_aspecto in cant_aspectos:
        contar_aspectos += 1
    contar_evaluaciones = 0
    for evaluacion in evaluaciones:
        contar_evaluaciones += 1
        #Declaraciones de listas y variables auxiliares
    conteo_de_evaluaciones = [0] * 5
    x = 0
    y = 0
    c = 0
    mf = [0] * contar_aspectos
    lista_d_evaluaciones = [0] * contar_evaluaciones

    #(-_-)#PASO 1 DEL METODO DELPHI#(-_-)#
    #Creación de la matriz de frecuencia#
    for evaluacion in evaluaciones:
        lista_d_evaluaciones[y] = evaluacion.evaluacion
        y += 1
    while x < contar_evaluaciones:
        y = 0
        while y < contar_evaluaciones / contar_aspectos:
            if lista_d_evaluaciones[x] == "Muy Mal":
                var0 = conteo_de_evaluaciones[0]
                conteo_de_evaluaciones[0] = var0 + 1
            elif lista_d_evaluaciones[x] == "Mal":
                var1 = conteo_de_evaluaciones[1]
                conteo_de_evaluaciones[1] = var1 + 1
            elif lista_d_evaluaciones[x] == "Regular":
                var2 = conteo_de_evaluaciones[2]
                conteo_de_evaluaciones[2] = var2 + 1
            elif lista_d_evaluaciones[x] == "Bien":
                var3 = conteo_de_evaluaciones[3]
                conteo_de_evaluaciones[3] = var3 + 1
            else:
                var4 = conteo_de_evaluaciones[4]
                conteo_de_evaluaciones[4] = var4 + 1
            y += 1
            x += 1
        mf[c] = conteo_de_evaluaciones
        conteo_de_evaluaciones = [0] * 5
        c += 1
    print('MF',mf)
    #(-_-)#PASO 2 DEL METODO DELPHI#(-_-)#
    #Creación de la matriz de frecuencias acumuladas#
    mfa = []
    lista_aux = []
    x = 0
    while x < contar_aspectos:
        y = 0
        lista_aux.append(mf[x][0])
        while y < 4:
            var1 = lista_aux[y]
            var2 = mf[x][y + 1]
            lista_aux.append(var1 + var2)
            y += 1
        x += 1
        mfa.append(lista_aux)
        lista_aux = []
    print('MFA')
    print(mfa)
    #(-_-)#PASO 3 DEL METODO DELPHI#(-_-)#
    #Creación de la matriz de frecuencias acumuladas relativas#
    mfar = [0] * contar_aspectos
    x = 0
    while x < contar_aspectos:
        y = 0
        while y < 5:
            lista_aux.append(mfa[x][y] * 1.00 / (contar_evaluaciones / contar_aspectos))
            y += 1
        mfar[x] = lista_aux
        lista_aux = []
        x += 1
    print('MFAR')
    print(mfar)
    #(-_-)#PASO 4 DEL METODO DELPHI#(-_-)#
    #Obtención del inverso de la distribución normal estándar acumulativa#
    mfinal = [0] * contar_aspectos
    x = 0
    while x < contar_aspectos:
        y = 0
        while y < 5:
            print(mfar[x][y])
            z = mfar[x][y] * 1000
            w = z.__int__()
            z = w / 100.0
            print(z,w,z)
            datos = db(db.valores.valor == z).select(db.valores.idnea)
            for dato in datos:
                print(dato.idnea)
                lista_aux.append(dato.idnea)
            y += 1
        mfinal[x] = lista_aux
        print(mfinal)
        lista_aux = []
        x += 1
    print('MFINAL')
    print(mfinal)
    #(-_-)#PASO 5 DEL METODO DELPHI#(-_-)#
    #Cálculo del resultado final#

    #Sumatoria del valor de los aspectos#
    sumatoriah = [0] * contar_aspectos
    x = 0
    while x < contar_aspectos:
        y = 0
        z = 0
        while y < 4:
            z = z + mfinal[x][y]
            y += 1
        sumatoriah[x] = z
        x += 1

    #Sumatoria del valor de los criterios#
    sumatoriav = [0] * 4
    x = 0
    while x < 4:
        y = 0
        z = 0
        while y < contar_aspectos:
            z = z + mfinal[y][x]
            y += 1
        sumatoriav[x] = z
        x += 1

    #Promedio del valor de los aspectos#
    promedio = [0] * contar_aspectos
    x = 0
    while x < contar_aspectos:
        z = sumatoriah[x] / 5.0
        promedio[x] = z
        x += 1

    #Cálculo del valor d N#
    n = 0
    x = 0
    z = 0
    while x < contar_aspectos:
        z = z + sumatoriah[x]
        x += 1
    n = z / (5.0 * contar_aspectos)

    #Promedio - N#
    x = 0
    while x < promedio.__len__():
        y = promedio[x]
        promedio[x] = y - n
        x += 1
    print('Promedios')
    print(promedio)

    #Cálculo de los límites#
    limites = [0] * 4
    x = 0
    while x < 4:
        limites[x] = sumatoriav[x] / contar_aspectos
        x += 1
    print('Límites')
    print(limites)

    #Clasificación de los elementos
    x = 0
    id_aspectos_solicitud = []
    for aspect in cant_aspectos:
        id_aspectos_solicitud.append(aspect.id_aspectossolicitud)
    while x < contar_aspectos:
        elemento = promedio[x]
        if elemento >= limites[3]:
            actualiza(4, id_solicitud, id_aspectos_solicitud[x])
        elif elemento >= limites[2]:
            actualiza(3, id_solicitud, id_aspectos_solicitud[x])
        elif elemento >= limites[1]:
            actualiza(2, id_solicitud, id_aspectos_solicitud[x])
        elif elemento >= limites[0]:
            actualiza(1, id_solicitud, id_aspectos_solicitud[x])
        else:
            actualiza(0, id_solicitud, id_aspectos_solicitud[x])
        x += 1
    return

def actualiza(clasificacion, id_solicitud, aspecto):
    rondas = db(db.evaluaciones.id_solicitudes == id_solicitud).select(db.evaluaciones.ronda)
    for ronda in rondas:
        x = ronda.ronda
    if x == '1':
        if clasificacion == 0:
            db((db.evaluaciones.id_solicitudes == id_solicitud) & (
                db.evaluaciones.id_aspectossolicitud == aspecto)).update(delphi='Muy Bien')
        elif clasificacion == 1:
            db((db.evaluaciones.id_solicitudes == id_solicitud) & (
                db.evaluaciones.id_aspectossolicitud == aspecto)).update(delphi='Bien')
        elif clasificacion == 2:
            db((db.evaluaciones.id_solicitudes == id_solicitud) & (
                db.evaluaciones.id_aspectossolicitud == aspecto)).update(delphi='Regular')
        elif clasificacion == 3:
            db((db.evaluaciones.id_solicitudes == id_solicitud) & (
                db.evaluaciones.id_aspectossolicitud == aspecto)).update(delphi='Mal')
        elif clasificacion == 4:
            db((db.evaluaciones.id_solicitudes == id_solicitud) & (
                db.evaluaciones.id_aspectossolicitud == aspecto)).update(delphi='Muy Mal')
    elif x == '2':
        if clasificacion == 0:
            db((db.aspectossolicitud.id_solicitudes == id_solicitud) & (
                db.aspectossolicitud.id == aspecto)).update(evaluacionfinal='Muy Bien')
        elif clasificacion == 1:
            db((db.aspectossolicitud.id_solicitudes == id_solicitud) & (
                db.aspectossolicitud.id == aspecto)).update(evaluacionfinal='Bien')
        elif clasificacion == 2:
            db((db.aspectossolicitud.id_solicitudes == id_solicitud) & (
                db.aspectossolicitud.id == aspecto)).update(evaluacionfinal='Regular')
        elif clasificacion == 3:
            db((db.aspectossolicitud.id_solicitudes == id_solicitud) & (
                db.aspectossolicitud.id == aspecto)).update(evaluacionfinal='Mal')
        elif clasificacion == 4:
            db((db.aspectossolicitud.id_solicitudes == id_solicitud) & (
                db.aspectossolicitud.id == aspecto)).update(evaluacionfinal='Muy Mal')
    return
