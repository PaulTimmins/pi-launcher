#!/usr/bin/python3
import time 
import cgi
from daemonize import Daemonize
import asyncio
from aiohttp import web
from gpiozero import LED

form = cgi.FieldStorage()

port = form.getvalue('port')
header = {'content-type': 'text/plain'}

#gpiomap
firepin = LED(1)


def gpiomap(pin=0):
    gpio = 1
    if (pin == 1):
        gpio = 4 
    if (pin == 2):
        gpio = 5
    if (pin == 3):
        gpio = 6
    if (pin == 4):
        gpio = 12
    if (pin == 5):
        gpio = 13
    if (pin == 6):
        gpio = 16
    if (pin == 7):
        gpio = 17
    if (pin == 8):
        gpio = 18
    if (gpio > 1):
        #print("{\"fire\": true; gpio: \""+str(gpio)+"\"}")
        return LED(gpio)
    else:
        #print("{\"fire\": false}")
        return LED(1)

@asyncio.coroutine
def firerequest(request):
    relay = request.match_info.get('relay');
    firepin = gpiomap(int(relay))   
    firepin.on()
    time.sleep(1)
    firepin.off()
    return web.Response(headers=header,body=('fired relay '+relay+' pin '+str(firepin)+"\n").encode('utf-8'))



@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET','/fire/{relay}',firerequest)
    srv = yield from loop.create_server(app.make_handler(),'0.0.0.0', 9001)
    print("Server started at http://0.0.0.0:9001")
    return srv

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

pid = "/tmp/fireproxy.pid"
daemon = Daemonize(app="fire_proxy", pid=pid, action=main)
#daemon.start()

main()
