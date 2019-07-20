#!/usr/bin/python3
import time 
import cgi
from daemonize import Daemonize
import asyncio
from aiohttp import web
from gpiozero import LED, Button

form = cgi.FieldStorage()

port = form.getvalue('port')
header = {'Content-Type': 'text/plain','Access-Control-Allow-Origin': '*'}
headerjson = {'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'}

#gpiomap
firepin = LED(1)
armrelay = LED(19)
armswitch = Button(20)
continuitysense = Button(21)
armed = 0


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

def arm():
    global armed
   #check continuity sense pin when we have that wired up :D
   #if armswitch.is_pressed:
    for n in (1,2,3,4,5,6,7,8):
     firepin = gpiomap(n)
     firepin.off()
    armrelay.on()
    armed=1
    print("armed\n")

def disarm():
    global armed
    for n in (1,2,3,4,5,6,7,8):
     firepin = gpiomap(n)
     firepin.off()
    armrelay.off()
    armed=0
    print("disarmed\n")

@asyncio.coroutine
def firerequest(request):
   global armed
   if armed == 1:
    relay = request.match_info.get('relay')
    firepin = gpiomap(int(relay))   
    firepin.on()
    time.sleep(1)
    firepin.off()
    return web.Response(headers=header,body=('fired relay '+relay+' pin '+str(firepin)+"\n").encode('utf-8'))
   else:
    return web.Response(headers=header,body=("cannot fire - system disarmed\n").encode('utf-8'))

@asyncio.coroutine
def armrequest(request):
   global armed
   arm()
   if armed == 1:
    return web.Response(headers=headerjson,body=('{"armed": "on"}').encode('utf-8'))
   else:
    return web.Response(headers=headerjson,body=('{"armed": "off"}').encode('utf-8'))

@asyncio.coroutine
def disarmrequest(request):
   global armed
   disarm()
   if armed == 1:
    return web.Response(headers=header,body=('{"armed": "on"}').encode('utf-8'))
   else:
    return web.Response(headers=header,body=('{"armed": "off"}').encode('utf-8'))


@asyncio.coroutine
def armquery(request):
   global armed
   if armed == 1:
    return web.Response(headers=header,body=('{"armed": "on"}').encode('utf-8'))
   else:
    return web.Response(headers=header,body=('{"armed": "off"}').encode('utf-8'))

@asyncio.coroutine
def testrequest(request):
    global armed
    if armed == 1:
      return web.Response(headers=headerjson,body=('{"message": "cannot continuity test, system is armed"}').encode('utf-8'))
    else:
      armrelay.off() #paranoid!
      results = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0 }
      for n in (1,2,3,4,5,6,7,8):
        firepin = gpiomap(n)
        firepin.on()
        time.sleep(.25)
        if continuitysense.is_pressed:
           results[str(n)]='1'
           #print("continuity detected\n")
        #else:
           #print("no continuity\n")
        firepin.off()
      return web.Response(headers=headerjson,body=('{ "x1": '+str(results['1'])+', "x2": '+str(results['2'])+', "x3": '+str(results['3'])+', "x4": '+str(results['4'])+', "x5": '+str(results['5'])+', "x6": '+str(results['6'])+', "x7": '+str(results['7'])+', "x8": '+str(results['8'])+' }').encode('utf-8'))

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET','/fire/{relay}',firerequest)
    app.router.add_route('GET','/test',testrequest)
    app.router.add_route('GET','/isarmed',armquery)
    app.router.add_route('GET','/arm',armrequest)
    app.router.add_route('GET','/disarm',disarmrequest)
    srv = yield from loop.create_server(app.make_handler(),'0.0.0.0', 9001)
    print("Server started at http://0.0.0.0:9001")
    return srv

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

pid = "/tmp/fireproxy.pid"
daemon = Daemonize(app="fire_proxy", pid=pid, action=main)
daemon.start()

main()
