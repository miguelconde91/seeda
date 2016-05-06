# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################


def index():
    mostrarmenu()
    return locals()

def tabla1():
    ft1 = SQLFORM.grid(db.tabla1, paginate=25)
    return dict(ft1=ft1)

def tabla2():
    ft2 = SQLFORM.grid(db.tabla2, paginate=25)
    return dict(ft2=ft2)

def tabla3():
    ft3 = SQLFORM.grid(db.tabla3, paginate=25)
    return dict(ft3=ft3)

def tabla4():
    ft4 = SQLFORM.grid(db.tabla4, paginate=25)
    return dict(ft4=ft4)

def tabla5():
    ft5 = SQLFORM.grid(db.tabla5, paginate=25)
    return dict(ft5=ft5)

def tabla6():
    ft6 = SQLFORM.grid(db.tabla6, paginate=25)
    return dict(ft6=ft6)

def tabla7():
    ft7 = SQLFORM.grid(db.tabla7, paginate=25)
    return dict(ft7=ft7)

def ayuda():
    mostrarmenu2()
    return locals()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection

    rules = {
        '<tablename>': {'GET': {}, 'POST': {}, 'PUT': {}, 'DELETE': {}},
    }
    return Collection(db).process(request, response, rules)
