# shso events
#
def init():
	global db
	global jdbconnection 
	global cmdMap
	
	cmdMap = {"ping": handlePing, "keepAlive": handleKeepAlive }
	
	#db = _server.getDatabaseManager()
	jdbconnection = db.getConnection()


def destroy():
	_server.trace( "Python extension dying" )


def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2


def handleRequest(cmd, params, who, roomId, protocol):
	#if protocol == "xml":
		if cmdMap.has_key(cmd):
			cmdMap[cmd](params, who, roomId)
		

def handleInternalEvent(evt):
	chan = evt.getObject("chan")
	#nick = evt.getParam("nick")
	nick = "chumbawumbA"
	passw = evt.getParam("pass")
	#_server.trace("evt = " + ' '.join(map(str, dir(evt))) )
	evtName = evt.getEventName()
	_server.trace( "Received internal event: " + evt.getEventName() )
	if evtName == "loginRequest":
		# to be done: add login verification logic.....for now, just always return logOK.
		_server.trace("Calling loginUser()!")
		obj = _server.loginUser(nick, passw, chan)
				#if obj.success == true:
		_server.trace("Calling getUserByChannel()!")
		user = _server.getUserByChannel(chan)

		response = {}
		response["_cmd"] = "logOK"
		response["name"] = "crabfu"
		response["id"] = "1"; 
		response["playerId"] = "EmpIridWolf"
		
		session_token_sql = "select * from shso.tokens where UserID = ?"
		prePareR = jdbconnection.prepareStatement(session_token_sql)
		prePareR.setInt(1,playerID)
		session_token_res = prePareR.executeQuery(session_token_sql)

		session_token = None
		if session_token_res.next():
			session_token = session_token_res.getString("token")
		response["sessionToken"] = session_token
		_server.trace("Calling sendResponse()!")
		_server.sendResponse(response, -1, None, chan)
		_server.trace("Calling sendRoomList()!")
		_server.sendRoomList(user)
		_server.trace("Called sendRoomList()!")
		zone = _server.getCurrentZone()
		room = zone.getRoomByName("lobby")	
		_server.joinRoom(user,-1,True,room.getId(),"",False,True)
		response = {}
		response["_cmd"] = "notification_ready"
		_server.sendResponse(response, -1, None, [user])

	session_token_res.close()

	prePareR.close()

	jdbconnection.close()

def handlePing(params, who, roomId):
	
	
	response = {}
	response["_cmd"] = "ping"

	_server.sendResponse(response, -1, None, [who])
	
def handleKeepAlive(params, who, roomId):
		
		
		response = {}
		response["_cmd"] = "keepAlive"

		_server.sendResponse(response, -1, None, [who])