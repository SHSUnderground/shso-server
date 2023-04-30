/*
* SmartFoxServer PRO
* Simple Extension Example
* v 1.0.0
* 
*
* Extensions Overview:
* -----------------------------------------------------------------
* Every extension must implement four basic methods:
* 
* init(), destroy(), handleRequest(), handleInternalEvent()
* 
* init()			It's the initialization point of the extension
* 				This method is invoked by the server on the extension as soon as it is loaded
* 				You can put here all your initialization code.
* 
* destroy()			This method is called by the server when the extension is going to be destroyed
* 				You should always put in this method the necessary code to release the resources
* 				you were using like setInterval(s), database connections etc...
* 
* handleRequest()		This method receives the client requests
* 
* handleInternalEvent()		Handles internal server events. Events are:
* 
* 				userJoin	when a user joins the room / zone
* 				userExit	when a user exits a room
* 				userLost	when a user disconnects
* 				newRoom		a new room was created in the zone
* 				roomLost	a room was destroyed in the zone
* 				loginRequest	a custom login request arrived	
*  
*/


var jdbconnection
var dbManager

/* 
* Initializion point:
* 
* this function is called as soon as the extension
* is loaded in the server.
* 
* You can add here all the initialization code
* 
*/

function init()
{

	// Using trace will send data to the server console
	trace("shso-chat init() called!")
		
	dbManager = _server.getDatabaseManager()
	jdbconnection = dbManager.getConnection()
}



/*
* This method is called by the server when an extension
* is being removed / destroyed.
* 
* Always make sure to release resources like setInterval(s)
* open files etc in this method.
* 
* In this case we delete the reference to the databaseManager
*/
function destroy()
{
	trace("Bye bye!")
		// Release the reference to the dbase manager
	delete dbase
	jdbconnection.close()
}

/*
* Handles the client request
* 
* cmd 		contains the request name
* params 	is an object containing data sent by the client
* user 		is the User object of the sender
* fromRoom	the id of the room where the request was sent from
* protocol	"xml" or "raw"
*/


function handleRequest(cmd, params, user, fromRoom, protocol)
{
	trace("handleRequest cmd=" + cmd + " protocol=" + protocol)

	if (protocol == "xml")
	{
		switch (cmd)
		{
			case "send_room_message":
				handleSendRoomMsg(params, user, fromRoom)
			break
		}
	}
	else
	{
		switch(cmd)
		{
						
				
		}
	}


}


/*
* This method handles internal events
* Internal events are dispactched by the Zone or Room where the extension is attached to
* 
* the (evt) object
*/
function handleInternalEvent(evt)
{
	// Simply print the name of the event that was received
	trace("Event received: " + evt.name)	
}

function handleSendRoomMsg(params, user, room)
{
	trace("handleSendRoomMsg() called!");	
	var sender_player_id = params.sender_player_id  //.toString()
	var room_name = params.room_name
	var message= params.message  // this will be base64 encoded
	var uid = user.getUserId()

	trace("sender_player_id = " + sender_player_id)
	trace("room_name = " + room_name)
	trace("message = " + message)

	var currentZone = _server.getCurrentZone()
	var curRoom = currentZone.getRoom(room)
	//var cnt = curRoom.getUserCount();
	//trace("curRoom.getUserCnt() = " + cnt)
	var users = curRoom.getAllUsers()

	var res = {}
	res._cmd = "notification"
	res.message_type = "receive_room_message"
	res.message = message
	res.sender_player_id = parseInt(sender_player_id)
	_server.sendResponse(res, -1, null, users, "xml")

	
	var sqlCommand = "INSERT INTO chat (zone, user, message) VALUES (?, ?, ?)"
	var prePareR = jdbconnection.prepareStatement(sqlCommand)
	prePareR.setString(1,room_name)

	var UserSQLCommand="SELECT Username FROM shso.user WHERE ID=(SELECT ShsoUserID FROM shso.active_players WHERE SfUserID=?)"
	var prePareRuser = jdbconnection.prepareStatement(UserSQLCommand)
	prePareRuser.setInt(1,sender_player_id)
	var resultUser = prePareRuser.executeQuery()


	prePareR.setString(2,resultUser.next().getString("Username"))

	var dcodeMessageSQLCommand = "SELECT CONVERT(FROM_BASE64(?)) using UTF8MB3"
	var prePareRmessge = jdbconnection.prepareStatement(dcodeMessageSQLCommand)
	prePareRmessge.setString(1,message)
	var resultDcodeMessage = prePareRmessge.executeQuery()

	prePareR.setString(3,resultDcodeMessage.next())

	var success = prePareR.executeUpdate()

	if (success != 0)
	{
		trace("Record inserted!")
	}
	else
	{
		trace("Ouch, record insertion failed")
	}

	// logMessage = "[" + room_name + "] " + sender_player_id + ": " + Base64.decode64(message);
	// _server.writeFile("chat.txt", logMessage, True);
	//_server.sendResponse(res, -1, null, [user], "xml")
	
	resultUser.close()
	resultDcodeMessage.close()

	prePareR.close()
	prePareRuser.close()
	prePareRmessge.close()

	

}



