# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
#request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
    ##db = DAL('postgres://postgres:postgres@localhost/delphi', pool_size=1, check_reserved=['all'], fake_migrate_all=0)
    #sqlite://storage.sqlite   postgres://postgres:postgres@localhost/delphi
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('sqlite://storage.sqlite')
    ## store sessions and tickets there
    ##session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager, Storage
#from gluon.contrib.login_methods.ldap_auth import ldap_auth

auth = Auth(db)
service = Service()
plugins = PluginManager()


#auth.settings.login_methods.append(ldap_auth(mode='ad',server='10.0.0.87',port='389',base_dn='ou=UCI Domain Users,dc=uci,dc=cu'))

# auth.settings.login_methods.append(ldap_auth(mode='ad', server='10.18.1.2', port='389', base_dn='dc=unica,dc=cu'))

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)
auth.settings.expiration = 3000
auth.settings.create_user_groups = None
auth.settings.everybody_group_id = 1
auth.settings.long_expiration = 3600*24*30
auth.settings.remember_me_form = True

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.uci.cu:25'
mail.settings.sender = 'maconde@uci.cu'
mail.settings.login = 'maconde@uci.cu:Mishki*100pre1'



## configure auth policy
#auth.settings.actions_disabled = ['request_reset_password', 'retrieve_username']
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = False
auth.settings.logout_next = URL('index')

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain

use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)

#restricciones para la tabla auth_user
db.auth_user.id.readable = False
#fin de restricciones
