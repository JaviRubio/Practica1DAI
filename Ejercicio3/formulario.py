# encoding: utf-8
# File: code.py

import web
from web import form

urls = (
        '/index(.*)', 'index',
        '/about(.*)', 'about',
        '/archives(.*)', 'archives',
        '/writing(.*)', 'writing',
        '/speaking(.*)', 'speaking',
        '/contact(.*)', 'contact',
        '/logout(.*)','logout',
        )

plantilla = web.template.render('./templates/')

app = web.application(urls, globals())



if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'user': 'anonymous','pag1' : 'vacio','pag2' : 'vacio','pag3' : 'vacio'})
    web.config._session = session
else:
    session = web.config._session

signin_form = form.Form(
    form.Textbox('username',form.Validator('Unknown username.',lambda x: x=='usuario'),description='Username:'),
    form.Password('password',form.notnull, description='Password:'),
    validators = [form.Validator("Username and password didn't match.",lambda x: x.username=='usuario' and x.password=='usuario')]
    )

class index:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='index.html'
        return plantilla.index(session.user, form,session.pag1,session.pag2,session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.index(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.index(session.user, form,session.pag1,session.pag2,session.pag3)

class about:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='about.html'
        return plantilla.about(session.user, form,session.pag1,session.pag2,session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.about(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.about(session.user, form,session.pag1,session.pag2,session.pag3)

class archives:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='archives.html'
        return plantilla.archives(session.user, form,session.pag1,session.pag2,session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.archives(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.archives(session.user, form,session.pag1,session.pag2,session.pag3)

class writing:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='writing.html'
        return plantilla.writing(session.user, form,session.pag1,session.pag2,session.pag2)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.writing(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.writing(session.user, form,session.pag1,session.pag2,session.pag3)

class speaking:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='speaking.html'
        return plantilla.speaking(session.user, form,session.pag1,session.pag2,session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.speaking(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.speaking(session.user, form,session.pag1,session.pag2,session.pag3)

class contact:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='contact.html'
        return plantilla.index(session.user, form,session.pag1,session.pag2,session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return plantilla.index(session.user, form)
        else:
            session.user = form['username'].value
            return plantilla.index(session.user, form,session.pag1,session.pag2,session.pag3)

class logout:
    def GET(self,name):
        session.kill()
        raise web.seeother('/index.html')

if __name__ == "__main__":
    app.run()