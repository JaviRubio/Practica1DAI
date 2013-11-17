# encoding: utf-8
# File: code.py

# Practicas de Desarrollo de Aplicaciones para Internet (DAI)
# Copyright (C) 2013 - Javier(jvr20@correo.ugr.es)
#    
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#   
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#   
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import web
from web import form

from web.contrib.template import render_mako

urls = (
        '/index(.*)', 'index',
        '/about(.*)', 'about',
        '/archives(.*)', 'archives',
        '/writing(.*)', 'writing',
        '/speaking(.*)', 'speaking',
        '/contact(.*)', 'contact',
        '/logout(.*)','logout',
        )

app = web.application(urls, globals(), autoreload=True)

render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )



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
        #return plantilla.index(session.user, form,session.pag1,session.pag2,session.pag3)
        return render.index(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.index(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.index(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class about:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='about.html'
        return render.about(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.about(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.about(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class archives:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='archives.html'
        return render.archives(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.archives(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.archives(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class writing:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='writing.html'
        return render.writing(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.writing(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.writing(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class speaking:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='speaking.html'
        return render.speaking(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.speaking(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.speaking(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
class contact:
    def GET(self,name):
        form=signin_form()
        if session.user=='usuario':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1='contact.html'
        return render.contact(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if not form.validates(): 
            return render.contact(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)
        else:
            session.user = form['username'].value
            return render.contact(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class logout:
    def GET(self,name):
        session.kill()
        raise web.seeother('/index.html')

if __name__ == "__main__":
    app.run()
