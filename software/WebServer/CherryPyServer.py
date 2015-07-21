__author__ = 'def'

import cherrypy

pronterface_path = '/home/def/Repositories/Printrun'
import sys, time
sys.path.append(pronterface_path)
from printrun.printcore import printcore

class HelloWorld(object):
    def __init__(self, printer):
        self.printer = printer

    def index(self, x, y):
        return "Hello World! " + str(self.printer.online) + ' ' + str(x) + ' ' + str(y)

    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <h1>CoreXY move app</h1>
            Use the form below to control the CoreXY:

            <form method="post" action="move">
              <input type="text" value="0" name="x" />
              <input type="text" value="0" name="y" />
              <button type="submit">Submit</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def move(self, x=0, y=0):
        self.printer.send("G1 F6000 X%s Y%s\n" % (x, y))
        return 'Ok!'

if __name__ == '__main__':
    pc =  printcore()
    time.sleep(2)
    print '[+] Connecting to device...'
    pc.connect('/dev/ttyACM1', 115200)
    time.sleep(2)
    if pc.online:
            print '[!] Connected!'
    else:
            exit()

    pc.send("G28 Y0\nG28 X0\n")

    cherrypy.config.update({'server.socket_host': '172.16.17.241',
                        'server.socket_port': 8080,
                       })
    cherrypy.quickstart(HelloWorld(pc))