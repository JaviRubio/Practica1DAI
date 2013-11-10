# encoding: utf-8
# File: code.py

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