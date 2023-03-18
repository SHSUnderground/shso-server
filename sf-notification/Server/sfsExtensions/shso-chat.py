#
# SmartFoxServer PRO
# Pyhton Extension template
# version 1.0.0
#

#
# An object called _server is available in the global scope
# The object is used to access the server side framework, just like in Actionscript extensions 
#

# 
# Initializion point:
# 
# this function is called as soon as the extension
# is loaded in the server.
# 
# You can add here all the initialization code
# 
import base64
def init():
	_server.trace("Python extension starting")
	_server.trace('VGhpcyBpcyBhIHRlc3Q='.decode('base64'))


#
# This method is called by the server when an extension
# is being removed / destroyed.
# 
# Always make sure to release resources like setInterval(s)
# open files etc in this method.
# 
# In this case we delete the reference to the databaseManager
#
def destroy():
	_server.trace("Python extension stopping")

	
#
# Handle Client Requests
# 
# cmd 		= a string with the client command to execute 
# params 	= list of parameters expected from the client
# who 		= the User object representing the sender
# roomId 	= the id of the room where the request was generated
# protocol	= the protocol used in the request ("xml", "str", "json"
# 
def handleRequest(cmd, params, who, roomId, protocol):
	pass


#
# This method handles internal events
# Internal events are dispactched by the Zone or Room where the extension is attached to
# 
# the (evt) object
#
def handleInternalEvent(evt):
	_server.trace( "Received internal event: " + evt.getEventName() )
