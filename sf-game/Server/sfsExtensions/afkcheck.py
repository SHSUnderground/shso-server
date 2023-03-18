#
# SmartFoxServer PRO
# Pyhton Extension template
# version 1.0.0
#
#Made by sirDoggo
import time
import threading

def init():
	_server.trace("Python AFK_CHECK extension starting")

def destroy():
	_server.trace("Python extension stopping")

def handleRequest(cmd, params, who, roomId, protocol):
	pass

def HandleAfkCheck(user):
    _server.trace("Created new thread!")
    while True:
        time.sleep(15)
	try:
	    _server.trace(user.getLastMessageTime())
            if user.getLastMessageTime() >= 15000:
                #_server.disconnectUser(user)
		_server.trace("SHOULD DISCONNECT!")
		break
	except:
	    break
    return

def handleInternalEvent(evt):
	
	evtName = evt.getEventName()
	if evtName == "userJoin":
	    _server.trace("Adding user to thread!")
	    user = evt.getObject("user")
            x = threading.Thread(target=HandleAfkCheck, args=(user,))
            x.start()
		
		

