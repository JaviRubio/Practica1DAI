''' Mi repositorio para las practicas de desarrollo de aplicaciones informaticas
    Copyright (C) 2013  JaviRubio

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import web
from web import form
from datetime import date

urls = (
	'/', 'index'
)
plantilla = web.template.render('./templates/')
 
app = web.application(urls, globals())

arrayDiasMeses=[None]*31
arrayAnios=[None]*100
d=date.today()
for i in range(31):
    arrayDiasMeses[i]=[i+1,i+1]
for i in range(100):
    arrayAnios[i]=[d.year-i,d.year-i]
myform = form.Form( 
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
	# Método de Llegada
	def GET(self):
		form = myform()
		return plantilla.formulario_1(form)

	# Método POST
	def POST(self):
		form = myform()
		if not form.validates():
			return plantilla.formulario_1(form)
		else:
			return "Registro completado %s %s" % (form.d.nombre, form.d.apellidos)

if __name__ == "__main__":
	app.run()
