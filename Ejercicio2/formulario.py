# encoding: utf-8
# File: code.py

# Practicas de Desarrollo de Aplicaciones para Internet (DAI)
# Copyright (C) 2013 - Javier (jvr20@correo.ugr.es)
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

from web.contrib.template import render_mako

urls = (
        '/about(.*)', 'about',
        '/archives(.*)', 'archives',
        '/writing(.*)', 'writing',
        '/speaking(.*)', 'speaking',
        '/contact(.*)', 'contact',
        '/(.*)', 'index',
        )

app = web.application(urls, globals(), autoreload=True)

render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

class index:
    def GET(self, name):
        return render.index(name=name)

    def POST(self, name):
        return render.index(name=name)

class about:
    def GET(self, name):
        return render.about(name=name)

    def POST(self, name):
        return render.about(name=name)

class archives:
    def GET(self, name):
        return render.archives(name=name)

    def POST(self, name):
        return render.archives(name=name)

class writing:
    def GET(self, name):
        return render.writing(name=name)

    def POST(self, name):
        return render.writing(name=name)

class speaking:
    def GET(self, name):
        return render.speaking(name=name)

    def POST(self, name):
        return render.speaking(name=name)

class contact:
    def GET(self, name):
        return render.contact(name=name)

    def POST(self, name):
        return render.contact(name=name)

if __name__ == "__main__":
    app.run()
