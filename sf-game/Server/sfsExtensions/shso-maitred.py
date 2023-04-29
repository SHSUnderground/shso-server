# shso maitred   .
#
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()


def init():
	global db
	global jdbconnection 
	global cmdMap
	
	cmdMap = {"getSeat": handleGetSeat, "closeRoom":handleCloseRoom }
	
	db = _server.getDatabaseManager()
	jdbconnection = db.getConnection()


def destroy():
	_server.trace( "Python extension dying" )
	jdbconnection.close()


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
		
def handleInternalRequest(obj):
	_server.trace("handleInternalRequest() called!")
	_server.trace("type obj= " + type(obj).__name__)
	_server.trace("type obj.get(0) = " + type(obj.get(0)).__name__ )
	_server.trace("obj.get(0)= " + obj.get(0) )
	
	zone = ex.getZone('shs.all')

	# Get a reference to the Extension we want to call 
	targetExtension = zone.getExtension("escrow");

	# Invoke the handleInternalRequest on the target extension and receive the response
	arr = ArrayList()
	arr.add("xml_parse_test")
	arr.add(777)
	retval = targetExtension.handleInternalRequest(arr);


def getNodeData(inStr, nodeStr):
	return (inStr[0].split("<" + nodeStr + ">"))[1].split("</" + nodeStr + ">")[0]

def getPlayerName(shsoUserId):
	error = ""
	username = None
	getUsernameSql = "SELECT Username FROM user WHERE ID = ?"

	prePareR = jdbconnection.prepareStatement(getUsernameSql)
	prePareR.setInt(1,shsoUserId)

	queryRes = prePareR.executeQuery()
	if (queryRes.next()):
		error = "query failed"
	if error == "":
		
		username = queryRes.getString("Username")
	
	queryRes.close()
	prePareR.close()
	

	return username

def getSfUserId(shsoUserId):
	error = ""
	sfUserID = None
	getIdSql = "SELECT SfUserID FROM active_players WHERE ShsoUserID = ?"
	prePareR = jdbconnection.prepareStatement(getIdSql)
	prePareR.setInt(1,shsoUserId)

	queryRes = prePareR.executeQuery()
	if (queryRes.next()):
		error = "query failed"
	if error == "":

		sfUserID = queryRes.getString("SfUserID")

	queryRes.close()
	prePareR.close()
	
	return sfUserID

def handleCloseRoom(params, who, roomId):
	# Create room variable storing invitees list
	room = _server.getCurrentZone().getRoom(roomId)
	if (room):
		# roomVar1 = RoomVariable(name="closed", val=True, priv=False, persistent=True) # by default private and persistent = False
		# roomVar1.setGlobal(True)
		# _server.setRoomVariables(room, None, [roomVar1])
		room.properties.put("closed", True)
		_server.trace("Closed game room: " + str(roomId))
	else:
		print("handleCloseRoom room is NULL.")


def handleGetSeat(params, who, roomId):
	_server.trace("getSeat params[0]=" + params[0])	

	user = who
	zone = _server.getCurrentZone()
	

	### TEMPORARY KLUDGE INSTEAD OF PARSING XML  ###### 
	if  "<game>BRAWLER</game>" in params[0]:
		_server.trace("Calling sendRoomList() brawler!")

		#mission = (params[0].split("<mission>"))[1].split("</mission>")[0]
		mission = getNodeData(params, "mission")
		_server.trace("mission =" + mission)

		# mayhem missions always get their own room, with max users set to 1
		# MAKE SURE TO MODIFY MULTIPLAYER MISSIONS SECTION TO CHECK MAX USERS ALLOWED IN ROOM
		if  "MAYHEM" in params[0]:   # this is processing for mayhem missions
			#create new room. use lobby roomCounter custom property to name room uniquely.
			lobby = zone.getRoomByName("lobby")

			# if roomCounter property doesn't exist, add it. Doing it here because it didn't seem to work in init() method.
			if "roomCounter" not in lobby.properties:
				lobby.properties.put("roomCounter", 1)

			roomCnt = lobby.properties.get("roomCounter")
			rName = "game-" + str(roomCnt)
			roomCnt = roomCnt + 1
			lobby.properties.put("roomCounter", roomCnt)

			roomObj = {}      	
			roomObj["name"] = rName
			roomObj["maxU"] = 1
			roomObj["isGame"] = True
			roomObj["closed"] = False
			#If something goes wrong an exception will be raised, so you should put your join code in a try/except block
			roomToUse = _server.createRoom(roomObj, who)

			# Create room variable storing mission name
			roomVar1 = RoomVariable("mission", mission) # by default private and persistent = False
			_server.setRoomVariables(roomToUse, None, [roomVar1])
			#_server.joinRoom( who, roomId, True, roomToUse.getId()) 

		else:   # this is processing for multiplayer missions
			
			shsoID = getNodeData(params, "player_id")
			allowedUsers = getNodeData(params, "allowed_users")
			_server.trace("shsoID: " + shsoID)
			_server.trace("allowedUsers: " + allowedUsers)

			if allowedUsers == "0":  # 0 means allow anyone, so this is request for daily mission
				# loop thru existing game rooms (that are hosting the same mission name) and see if any are not full....
				allRooms = zone.getRooms()
				allRoomsFull = True
				for room in allRooms:
					if room.isGame():
						roomMission = room.getVariable("mission").getValue()
						_server.trace("roomMission =" + roomMission)
					else:
						roomMission = ""
						_server.trace("roomMission = <not game room>")
	
					if (room.getUserCount() < room.getMaxUsers()) and (room.isGame()) and (roomMission == mission):
						try:
							if (room.properties.get("closed") is None):
								_server.trace("Room: " + str(room.getId()) + "Closed = None")
								roomVar = room.getVariable("invitees")
								if (roomVar is None): # ignore for rooms that have invitees, daily mission players not allowed there
									allRoomsFull = False
									roomToUse = room
									break
							elif (not room.properties.get("closed")):
								_server.trace("Room: " + str(room.getId()) + "Closed = False")
								roomVar = room.getVariable("invitees")
								if (roomVar is None): # ignore for rooms that have invitees, daily mission players not allowed there
									allRoomsFull = False
									roomToUse = room
									break
							else:
								_server.trace("Room: " + str(room.getId()) + "Closed = True")
						except:
							_server.trace("Joined without checking if room is closed, room: " + str(room.getId()))
							roomVar = room.getVariable("invitees")
							if (roomVar is None): # ignore for rooms that have invitees, daily mission players not allowed there
								allRoomsFull = False
								roomToUse = room
								break
						# _server.trace("Joined without checking if room is closed, room: " + str(room.getId()))
						# roomVar = room.getVariable("invitees")
						# if (roomVar is None): # ignore for rooms that have invitees, daily mission players not allowed there
						# 	allRoomsFull = False
						# 	roomToUse = room
						# 	break
				if not allRoomsFull:
					#use found room that is not full
					_server.trace("found game room that is not full.")
				else:
					#create new room. use lobby roomCounter custom property to name room uniquely.
					lobby = zone.getRoomByName("lobby")
				#"""
					# if roomCounter property doesn't exist, add it. Doing it here because it didn't seem to work in init() method.
					if "roomCounter" not in lobby.properties:
						lobby.properties.put("roomCounter", 1)
	
					roomCnt = lobby.properties.get("roomCounter")
					rName = "game-" + str(roomCnt)
					roomCnt = roomCnt + 1
					lobby.properties.put("roomCounter", roomCnt)
					roomObj = {}      	
					roomObj["name"] = rName
					roomObj["maxU"] = 4
					roomObj["isGame"] = True
					# roomObj["closed"] = False
					#If something goes wrong an exception will be raised, so you should put your join code in a try/except block
					roomToUse = _server.createRoom(roomObj, who)
	
					# Create room variable storing mission name
					roomVar1 = RoomVariable("mission", mission) # by default private and persistent = False
					_server.setRoomVariables(roomToUse, None, [roomVar1])
				#"""
			else:  # allowed_users != 0 means must be request for invite mission
				# if this is the inviter, create room, add inviter to room, store invitees in room variable and send invites to invitees...
				# otherwise, find room where player is invitee, then add invitee to that room.  
				userList = allowedUsers.split(',')
				if (userList[0] == shsoID):	# index 0 is the inviter's ID 
					#create new room. use lobby roomCounter custom property to name room uniquely.
					lobby = zone.getRoomByName("lobby")
					
					# if roomCounter property doesn't exist, add it. Doing it here because it didn't seem to work in init() method.
					if "roomCounter" not in lobby.properties:
						lobby.properties.put("roomCounter", 1)

					roomCnt = lobby.properties.get("roomCounter")
					rName = "game-" + str(roomCnt)
					roomCnt = roomCnt + 1
					lobby.properties.put("roomCounter", roomCnt)
					roomObj = {}      	
					roomObj["name"] = rName
					roomObj["maxU"] = 4
					roomObj["isGame"] = True
					# roomObj["closed"] = False
					#If something goes wrong an exception will be raised, so you should put your join code in a try/except block
					_server.trace("who.getUserId()=" + str(who.getUserId()))
					roomToUse = _server.createRoom(roomObj, who)
	
					# Create room variable storing invitees list
					roomVar1 = RoomVariable("invitees", allowedUsers) # by default private and persistent = False
					_server.setRoomVariables(roomToUse, None, [roomVar1])

					# Create room variable storing mission name
					roomVar2 = RoomVariable("mission", mission) # by default private and persistent = False
					_server.setRoomVariables(roomToUse, None, [roomVar2])


					# send invites to invitees (but not inviter)
					for i in userList:
						if (i != shsoID):
							_server.trace("need to invite " + i)
							sfUserId = getSfUserId(i)
							if (sfUserId is None):
								continue
							_server.trace("sfUserId = " + sfUserId)
							invuser =  _server.getUserById(int(sfUserId))

							response = {}
							response["_cmd"] = "notification"
							response["message_type"] = "brawler_invitation"
							response["inviter_id"] = shsoID
							response["invitation_id"] = "1103"
							response["inviter_name"] = getPlayerName(shsoID)
							response["mission"] = mission
	
							_server.sendResponse(response, -1, None, [invuser], _server.PROTOCOL_XML)
							# !!!! TBD !!!!!
				else:
					# loop thru existing game rooms, looking for a room where player is an invitee...
					allRooms = zone.getRooms()
					roomToUse = None
					for room in allRooms:
						roomVar = room.getVariable("invitees")
						invitees = None
						if (roomVar is not None):
							invitees = roomVar.getValue()
							_server.trace("roomVar invitees= " + invitees)
							if shsoID in invitees: # player has been invited to this room
								roomToUse = room
								break
					# no room was found for this invitee, so just return...
					if (roomToUse == None):
						_server.trace("no room was found for this invitee, player not added to any room.")
						return

		

        	#join user
			_server.joinRoom( who, roomId, True, roomToUse.getId())
		return
	###################################################

	_server.trace("Calling sendRoomList()!")
	_server.sendRoomList(user)
	_server.trace("Called sendRoomList()!")
	
	room = zone.getRoomByName("Daily_Bugle")
	lobby = zone.getRoomByName("lobby")
	_server.joinRoom(user,lobby.getId(),True,room.getId(),"",False,True)
	#_server.joinRoom(user,-1,True,room.getId(),"",False,True)
	
