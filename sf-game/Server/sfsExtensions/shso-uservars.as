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
	trace("shso-uservars init() called!")
		
	dbManager = _server.getDatabaseManager()
}



/*
* This method is called by the server when an extension
* is being removed / destroyed.
* 
* Always make sure to release resources like setInterval(s)
* open files etc in this method.
* 
* In this case we devare the reference to the databaseManager
*/
function destroy()
{
	trace("Bye bye!");
	// Release the reference to the dbase manager
	// devare dbase;
	delete dbase;
}


function getUserIdFromSFS(user) {

	// var sql = "select * from active_players where SfUserID =" + _server.escapeQuotes(sfsID) + ";";
	// queryRes = dbManager.executeQuery(sql);
	// if (queryRes && queryRes.size() > 0) {
	// 	return queryRes.get(0).getItem("ShsoUserID");
	// }
	var userIDSQL = "SELECT ID from user WHERE Username='" + _server.escapeQuotes(user.getName()) + "' OR Nick = '" + _server.escapeQuotes(user.getName()) + "';";
		var queryRes = dbManager.executeQuery(userIDSQL);
		if (queryRes && queryRes.size() > 0) {
			return queryRes.get(0).getItem("ID");
		}

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
			case "user_vars":
				handleUserVars(params, user, fromRoom)
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

function handleUserVars(params, user, room)
{
	trace("handleUserVars() called!")	

	//var hero = params.hero
	//var key = params.key
	//var blob = params.blob
	//var uid = user.getUserId()

	//trace("hero = " + hero)
	//trace("key = " + key)
	//trace("blob = " + blob)

	//var jso = Packages.net.sf.json.JSONObject.fromObject(params);
	//trace(jso);
 

	//var res = []		// The list of params	
	//res[0] = "hero_create"		// at index = 0, we store the command name
	//res[1] = uid	// fromRTCId - CSP not sure what this is supposed to be, guessing that it's user ID
	//res[2] = hero	// hero
	//res[3] = blob	// data

	/*
		_server.sendResponse(response, fromRoom, sender, recipients, type)
		
		response	 An object containing all properties and objects that you want to send to the client(s). On the client side you will obtain the same exact object.
				As a convention there should be always a property called _cmd containing the name of the action being performed.

				If you use the raw/string protocol, you will have to pass an Array of parameters instead of an object. (Check the example below)
		fromRoom	 (optional) The roomId from where this message is coming. If you don't need it, just set it to -1
		sender	 	(optional) The User object that you want to pass as the sender of this message. If you don't need this just use null
		recipients	 an Array containing one ore more User objects
		type	 	(optional) By default it is set to "xml", and the message will be XML formatted. You can also specify "str" if you wish to send a raw, string based message.

	*/

	
	currentZone = _server.getCurrentZone()
	//currentZone = helper.getZone(this.getOwnerZone)
	curRoom = currentZone.getRoom(room)
	//curRoom = _server.getCurrentRoom()
	cnt = curRoom.getUserCount();
	trace("curRoom.getUserCnt() = " + cnt)
	var users = curRoom.getAllUsers()

	///////// write active player info to active_players table in database.  ///////
	//var sql = "INSERT INTO active_players (SfUserID, SfRoomID, Hero, BlobText) VALUES(" + uid.toString() + "," + curRoom.getId().toString() + ",'" + hero + "','" + blob + "')";
	//trace("sql= " + sql);
	//var success = dbManager.executeCommand(sql);
                
        //if (success)
	//	trace("Record inserted!")
	//else
	//	trace("Ouch, record insertion failed")
	/////////////////////////////////////////////////////////////////////


	//for (i=0;i<cnt;i++){
	//	trace(users[i].getName())
	//}

	// CSP - prob need to change next line to send to all clients in the room.
	//_server.sendResponse(res, -1, null, [user], "str")
	//_server.sendResponse(res, -1, null, users, "str")


	///////// now query active_players table, send hero_create response for each active player in room to client.  ///////
	var sql = "SELECT * FROM active_players WHERE SfRoomID = " + _server.escapeQuotes(curRoom.getId().toString());
	var queryRes = dbManager.executeQuery(sql)
	if (queryRes != null)
	{
		for (var i = 0; i < queryRes.size(); i++)
		{
			var tempRow = queryRes.get(i)
		
			//trace("Record n." + i)
			//trace("Name: " + tempRow.getItem("name"))
			//trace("Location: " + tempRow.getItem("location"))
			//trace("Email: " + tempRow.getItem("email"))
			//trace("-------------------------------------------")

			//res = []		// The list of params	
			//res[0] = "hero_create"		// at index = 0, we store the command name
			//res[1] = tempRow.getItem("SfUserID")	// fromRTCId - CSP not sure what this is supposed to be, guessing that it's user ID
			//res[2] = tempRow.getItem("Hero")	// hero
			//res[3] = tempRow.getItem("BlobText")	// data

			//_server.sendResponse(res, -1, null, [user], "str")

			// now send playerVars msg for each active player to all users.  (maybe needs to be done at login, not here).
			trace("SfUserID=" + tempRow.getItem("SfUserID").toString());
			// var pvUser = _server.getUserById(parseInt(tempRow.getItem("SfUserID")));
			var sql = "SELECT * FROM shso.user WHERE id = " + _server.escapeQuotes(tempRow.getItem("ShsoUserID").toString());
			// var queryResName = dbManager.executeQuery(sql);
			// var player_name = queryResName.get(0).getItem("Username").toString();
			var player_name = user.getName();

			res = [];
			res[0] = "playerVars";
			// var sql = 'SELECT heroes.* FROM shso.heroes, shso.user WHERE heroes.UserID = user.ID AND user.ID = ' + _server.escapeQuotes(userID);
			var userID = getUserIdFromSFS(user);
			var player_name = user.getName();
			var squadlvlsql = "select CalculateSquadLevel(" + _server.escapeQuotes(userID) + ") AS `squadlevel`";
			var lvlsql = "select GETLVL((SELECT XP from shso.heroes WHERE UserID = " + _server.escapeQuotes(userID) + " AND name = (SELECT hero_name from shso.equips WHERE UserID = " + _server.escapeQuotes(userID) + "))) AS `hero_level`";
			var squad_level = 0;
			var hero_level = 0;
			var lvlQueryRes = dbManager.executeQuery(lvlsql);
			var squadlvlQueryRes = dbManager.executeQuery(squadlvlsql);
			if (lvlQueryRes && lvlQueryRes.size() > 0) {
				hero_level = lvlQueryRes.get(0).getItem("hero_level");
			}
			if (squadlvlQueryRes && squadlvlQueryRes.size() > 0) {
				squad_level = squadlvlQueryRes.get(0).getItem("squadlevel");
			}
			

			// res[1] = tempRow.getItem("SfUserID").toString() + "|" + tempRow.getItem("ShsoUserID").toString() + "|" + player_name + "|true|" + hero_level.toString() + "|" + squadlevel.toString();
			// res[1] = tempRow.getItem("SfUserID").toString() + "|" + tempRow.getItem("ShsoUserID").toString() + "|" + player_name + "|true|1|1";
			// res[1] = tempRow.getItem("SfUserID").toString() + "|" + tempRow.getItem("ShsoUserID").toString() + "|" + player_name.toString() + "|" + user.isModerator.toString() + "|" + hero_level.toString() + "|" + squadlevel.toString();
			res[1] = tempRow.getItem("SfUserID").toString() + "|" + tempRow.getItem("ShsoUserID").toString() + "|" + player_name + "|" + (user.isModerator == true ? "True" : "False") + "|" + hero_level + "|" + squad_level;
			// trace("USERVARS: " + res[1])
			// res[1] = tempRow.getItem("SfUserID").toString() + "|" + tempRow.getItem("ShsoUserID").toString() + "|" + player_name.toString() + "|" + (user.isModerator | 0).toString() + "|1|1";
			//_server.sendResponse(res, -1, null, [user], "str")
			_server.sendResponse(res, -1, null, users, "str");


		}
	}
	else
		trace("DB Query failed")
	/////////////////////////////////////////////////////////////////////


}



