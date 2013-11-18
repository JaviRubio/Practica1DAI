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


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from pymongo import MongoClient
from web import form
from web.contrib.template import render_mako
from datetime import date

urls = (
        '/about(.*)', 'about',
        '/archives(.*)', 'archives',
        '/writing(.*)', 'writing',
        '/speaking(.*)', 'speaking',
        '/contact(.*)', 'contact',
        '/logout(.*)','logout',
        '/register(.*)','register',
        '/(.*)', 'index'
        )

app = web.application(urls, globals(), autoreload=True)

render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'user': 'anonymous','pag0' : 'vacio','pag1' : 'vacio','pag2' : 'vacio','pag3' : 'vacio'})
    web.config._session = session
else:
    session = web.config._session

client = MongoClient()
db = client.myDB

#Aunque se llama nuevo usuario,tambien se ha reciclado para actualizar los existentes
def newUser(nombre,apellidos,password,dni,correo,visa,fecha1,fecha2,fecha3,direccion,pago,clausulas):
    nombre=str(nombre)
    user={"nombre":nombre,
        "apellidos":str(apellidos),
        "pass":str(password),
        "correo":str(correo),
        "dni":str(dni),
        "visa":str(visa),
        "dia":str(fecha1),
        "mes":str(fecha2),
        "anyo":str(fecha3),
        "direccion":str(direccion),
        "pago":str(pago),
        "clausulas":str(clausulas)
    }
    if db.users.find_one({"nombre":nombre})==None:
        db.users.insert(user)
    else:
        db.users.update({"nombre":nombre}, {"$set": {"apellidos":str(apellidos),"pass":str(password),"correo":str(correo),"dni":str(dni),"visa":str(visa),"dia":str(fecha1),"mes":str(fecha2),"anyo":str(fecha3),"direccion":str(direccion),"pago":str(pago),"clausulas":str(clausulas)}})

def loadUser(nombre):
    nombre=str(nombre)
    Actualuser=db.users.find_one({"nombre":nombre})
    user=[None]*11
    #Esta conversion de diccionario a lista se hace para mantener la compatibilidad con el resto del codigo
    user[0]=Actualuser["nombre"]
    user[1]=Actualuser["apellidos"]
    user[2]=Actualuser["dni"]
    user[3]=Actualuser["correo"]
    user[4]=Actualuser["visa"]
    user[5]=Actualuser["dia"]
    user[6]=Actualuser["mes"]
    user[7]=Actualuser["anyo"]
    user[8]=Actualuser["direccion"]
    user[9]=Actualuser["pago"]
    user[10]=Actualuser["clausulas"]
    return user


signin_form = form.Form(
    form.Textbox('username',form.notnull,description='Username:'),
    form.Password('password',form.notnull, description='Password:'),
    validators = [form.Validator("Username and password didn't match.",lambda x: str(x.password)==db.users.find_one({"nombre":str(x.username)})["pass"])]
    )

arrayDiasMeses=[None]*31
arrayAnios=[None]*100
d=date.today()
for i in range(31):
    arrayDiasMeses[i]=[i+1,i+1]
for i in range(100):
    arrayAnios[i]=[d.year-i,d.year-i]

registerForm = form.Form( 
    form.Textbox("nombre", form.notnull,description = "Nombre:"),
    form.Textbox("apellidos",form.notnull ,description = "Apellidos:",),
    form.Textbox("dni",form.notnull, description = "DNI:"),
    form.Textbox("correo",form.notnull,form.regexp('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,3})$',"Correo incorrecto"), description = "Correo electronico:"),
    form.Dropdown('dia', arrayDiasMeses),
    form.Dropdown('mes', arrayDiasMeses[0:12]),
    form.Dropdown('anyo', arrayAnios),#Problemas con la codificacion de la Ñ,arreglar si sobre tiempo
    form.Textarea("direccion",form.notnull, description = "Direccion:"),
    form.Password("pass1",form.notnull,form.Validator('El password tiene que tener mas de 7 caracteres',lambda x: int(x)>7), description = "Password:"),
    form.Password("pass2",form.notnull,form.Validator('El password tiene que tener mas de 7 caracteres',lambda x: int(x)>7), description = "Repita su password:"),
    form.Radio("pago", ["Contrareembolso", "Con tarjeta"],description="Forma de pago"),
    form.Checkbox("condiciones",form.Validator('Tiene que aceptar las condiciones',lambda x: x=='acepto'),description="Acepto las condiciones",value='acepto'),
    form.Textbox("visa",form.regexp('([0-9]{4}[\s-]){3}[0-9]{4}',"Visa incorrecta"),description = "Numero de VISA:"),
    validators=[form.Validator("Los password no coinciden",lambda x:x.pass1 == x.pass2),form.Validator("Fecha incorrecta",lambda i:(((int(i.mes) == 2) and ((int(i.dia) <= 28) and ((int(i.anyo) % 4) != 0) or (int(i.dia) <= 29) and ((int(i.anyo) % 4) == 0))) or ((int(i.dia) <= 30) and ((int(i.mes) == 4) or (int(i.mes) == 6) or (int(i.mes) == 9) or (int(i.mes) == 11))) or ((int(i.mes) == 1) or(int(i.mes) == 3) or(int(i.mes) == 5) or(int(i.mes) == 7) or (int(i.mes) == 8) or (int(i.mes) == 10) or (int(i.mes) == 12) )))]
) 

class index:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='index.html'
        return render.index(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

    def POST(self,name):
        form=signin_form()
        if form.validates(): 
            session.user = form['username'].value
        return render.index(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class about:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='about.html'
        return render.about(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)


class archives:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='archives.html'
        return render.archives(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class writing:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='writing.html'
        return render.writing(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)


class speaking:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='speaking.html'
        return render.speaking(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class contact:
    def GET(self,name):
        form=signin_form()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='contact.html'
        return render.contact(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3)

class register:
    def GET(self,name):
        form=signin_form()
        regis=registerForm()
        if session.user!='anonymous':
            session.pag3=session.pag2
            session.pag2=session.pag1
            session.pag1=session.pag0
            session.pag0='register.html'
            data=loadUser(session.user)
            regis['nombre'].value=data[0]
            regis['apellidos'].value=data[1]
            regis['dni'].value=data[2]
            regis['correo'].value=data[3]
            regis['visa'].value=data[4]
            regis['dia'].value=int(data[5])
            regis['mes'].value=int(data[6])
            regis['anyo'].value=int(data[7])
            regis['direccion'].value=data[8]
            regis['pago'].value=data[9]
            regis['condiciones'].value=data[10]
        return render.register(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3,register=regis.render())

    def POST(self,name):
        form=signin_form()
        regis=registerForm()
        if regis.validates(): 
            session.user = regis['nombre'].value
            newUser(regis['nombre'].value,regis['apellidos'].value,regis['pass1'].value,regis['dni'].value,regis['correo'].value,regis['visa'].value,regis['dia'].value,regis['mes'].value,regis['anyo'].value,regis['direccion'].value,regis['pago'].value,regis['condiciones'].value)
        return render.register(formLogin=form.render(),user=session.user,pag1=session.pag1,pag2=session.pag2,pag3=session.pag3,register=regis.render())
       
class logout:
    def GET(self,name):
        session.kill()
        raise web.seeother('/index.html')

if __name__ == "__main__":
    app.run()