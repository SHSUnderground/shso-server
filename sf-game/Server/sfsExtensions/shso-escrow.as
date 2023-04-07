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
var jdbconnection

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
	trace("shso-escrow init() called!")
		
	dbManager = _server.getDatabaseManager()
	jdbconnection = dbManager.getConnection()

	// Create a reference to the Java package
		// This help us building new objects from the nanoxml package.
		// Instead of typing the fully qualified Class name we'll just use:
		//
		// var obj = new nanoxml.SomeObject()
		nanoxml = Packages.net.n3.nanoxml
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


function storeMissionPlayers(userID, missionID) {
	trace("storeMissionPlayers was called.")
	if (userID && missionID) {
		var sqlCommand = "INSERT INTO active_missions VALUES(?, ?) ON DUPLICATE KEY UPDATE MissionID = ?"
		var prePareR = jdbconnection.prepareStatement(sqlCommand)
		prePareR.setInit(1,userID)
		prePareR.setString(2,missionID)
		prePareR.setString(3,missionID)
		
		var success = prePareR.executeUpdate()
				
		if (success != 0)
			trace("Mission record inserted!")
		else
			trace("Ouch, mission record insertion failed")
		
		prePareR.close()
	}
}


function removeMissionPlayers(userID) {
	var removeSqlCommand = "DELETE FROM active_missions WHERE UserID = (SELECT ShsoUserID FROM active_players WHERE SfUserID=?)"
	// trace("Remove from missions sql: " + sql)
	var prePareRqremove = jdbconnection.prepareStatement(removeSqlCommand)
	prePareRqremove.setInit(1,userID)
	
	var success = prePareRqremove.executeUpdate()
				
	if (success != 0)
		trace("Record deleted!")
	else
		trace("Ouch, record deletion failed")
	
	prePareRqremove.close()
}

function handleGetGameRoom(userID, missionID)
{
	storeMissionPlayers(userID, missionID)
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
	//trace("handleRequest cmd=" + cmd + " protocol=" + protocol)
	if (protocol == "xml")
	{
		switch (cmd)
		{
			case "hero_create":
				handleHeroCreate(params, user, fromRoom)
			break
		}
	}
	else
	{
		switch(cmd)
		{
			case "ntO":  // take ownership
				handleNto(params, user, fromRoom)
			break
			
			case "tO":  // take ownership (autotransfer)
				handleTo(params, user, fromRoom)
			break				
		}
	}
}

function handleInternalRequest(obj)
{
   // Simply print the name of the event that was received
  // trace("handleInternalRequest called!")   

   message = String(obj.get(0));
   //trace("message = " + message)   
	
   /////////////// xml test ///////////////////// 
   if (message.equals("xml_parse_test"))
   {
	//trace("xml_parse_test conditional entered!") 

	///////////////
	// Setup the xml parser object
		var xmlParser = nanoxml.XMLParserFactory.createDefaultXMLParser()
		
		// This is the XML Reader:
		// You can use a fileReader, to read the XML from a file
		// or the StringReader, to read the XML from a string
		var xmlReader = nanoxml.StdXMLReader.stringReader("<bookList><book title='Head First Design Patterns' author='Freeman, Freeman' year='2004' publisher='OReilly' /> </bookList>")

	 
		// Assign the reader to the parser
		xmlParser.setReader(xmlReader)
		
		// Finally parse the XML
		var xmlDoc = xmlParser.parse()

	var node = xmlDoc.getFirstChildNamed("book")
	var bookTitle = node.getAttribute("title", "")
	//trace("book title=" + bookTitle)
	//////////////
	


	// reference to the java package
	var _util = Packages.java.util
	// Create an ArrayList instance
	var myList = new _util.ArrayList()

	return myList;
   }

   if (message.equals("do_rtc_response"))
   {
	trace("do_rtc_response called!")	

	//var uid = user.getUserId()
	var users = _server.getCurrentZone().getRoomByName("Daily_Bugle").getAllUsers()  // all users

	var res = {}
   	res._cmd="notification"		
	res.message_type = "brawler_invitation"	
	res.inviter_id = "777"
	res.invitation_id = "1103"
	res.inviter_name = "foobar2"
	res.mission = "m_101S_1_Skydome002"

			
	// Send the raw message
	// _server.sendResponse() works just like any other requests
	// you have only to add the "str" argument to use the raw protocol
	_server.sendResponse(res, -1, null, users, "xml")


   }

   if (message.equals("get_game_room_accept"))
   {
	//*AS_SESSION_KEY : aSessionToken
	//*mission : m_1007_1_FingFangFoom001
	//*game : BRAWLER
	//*user : 3870526
	//*invitees : 3900010,3900009,3900011

	var missionID = String(obj.get(2))
	var user = String(obj.get(4))
	//var invitees = String(obj.get(5))
	var invitation_id = String(obj.get(5))
	var accept = String(obj.get(6))
	var inviter_id = String(obj.get(7))

	trace("get_game_room_invite missionID: " + missionID)
	handleGetGameRoom(user, missionID)
	
	  	// reference to the java package
	var _util = Packages.java.util
	// Create an ArrayList instance
	var myList = new _util.ArrayList()
	// Add one or more items to array list
	//myList.add("This is cool!")
	//myList.add((obj.get(1)).toString())

	var myText = "";
		//myText += bldg.S11.Title + "\n";
	myText += "<response>\n"
	myText += "  <status>200</status>\n"
	myText += "  <headers>\n"
	myText += "    <Content-Type>text/html; charset=utf-8</Content-Type>\n"
	myText += "  </headers>\n"
	myText += "  <body>&lt;response&gt;&lt;invitation&gt;\n"
	myText += "	  &lt;invitation_id&gt;1103&lt;/invitation_id&gt;\n"
	myText += "	&lt;/invitation&gt;\n"

	myText += "	&lt;ticket&gt;\n"
	myText += "	  &lt;player_id&gt;" + user + "&lt;/player_id&gt;\n"
	myText += "	  &lt;player_name&gt;RW1wZXJvciBJcmlkZXNjZW50IFdvbGY=&lt;/player_name&gt;\n"
	myText += "	  &lt;subscriber&gt;1&lt;/subscriber&gt;\n"
	myText += "	  &lt;session_key&gt;720f98cb79e59f0e6eb2c758915c53978fb0af09d7e5db86edcfd399168bc07c&lt;/session_key&gt;\n"
	myText += "	  &lt;squad_level&gt;6924&lt;/squad_level&gt;\n"
	myText += "	  &lt;entitlements&gt;\n"
	myText += "	    &lt;ArcadeAllow&gt;1&lt;/ArcadeAllow&gt;\n"
	myText += "	    &lt;CardGameAllow&gt;1&lt;/CardGameAllow&gt;\n"
	myText += "	    &lt;CatalogCountry&gt;US&lt;/CatalogCountry&gt;\n"
	myText += "	    &lt;ClientConsoleAllow&gt;0&lt;/ClientConsoleAllow&gt;\n"
	myText += "	    &lt;DemoLimitsOn&gt;0&lt;/DemoLimitsOn&gt;\n"
	myText += "	    &lt;Expiration&gt;0&lt;/Expiration&gt;\n"
	myText += "	    &lt;IsPayingSubscriber&gt;1&lt;/IsPayingSubscriber&gt;\n"
	myText += "	    &lt;MaxChallengeLevel&gt;65&lt;/MaxChallengeLevel&gt;\n"
	myText += "	    &lt;OpenChatAllow&gt;1&lt;/OpenChatAllow&gt;\n"
	myText += "	    &lt;ParentalCardGameDeny&gt;0&lt;/ParentalCardGameDeny&gt;\n"
	myText += "	    &lt;ParentalFriendingDeny&gt;0&lt;/ParentalFriendingDeny&gt;\n"
	myText += "	    &lt;ParentalHQDeny&gt;0&lt;/ParentalHQDeny&gt;\n"
	myText += "	    &lt;ParentalMissionsDeny&gt;0&lt;/ParentalMissionsDeny&gt;\n"
	myText += "	    &lt;PlayerCountry&gt;US&lt;/PlayerCountry&gt;\n"
	myText += "	    &lt;PlayerLanguage&gt;en&lt;/PlayerLanguage&gt;\n"
	myText += "	    &lt;ShieldHQAllow&gt;1&lt;/ShieldHQAllow&gt;\n"
	myText += "	    &lt;ShieldHeroesAllow&gt;1&lt;/ShieldHeroesAllow&gt;\n"
	myText += "	    &lt;ShieldPlayAllow&gt;1&lt;/ShieldPlayAllow&gt;\n"
	myText += "	    &lt;ShieldPrizeWheelAllow&gt;1&lt;/ShieldPrizeWheelAllow&gt;\n"
	myText += "	    &lt;ShoppingCatalog&gt;1&lt;/ShoppingCatalog&gt;\n"
	myText += "	    &lt;SubscriptionType&gt;1&lt;/SubscriptionType&gt;\n"
	myText += "	    &lt;UnityEditorAllow&gt;0&lt;/UnityEditorAllow&gt;\n"
	myText += "	    &lt;UseExternalShopping&gt;0&lt;/UseExternalShopping&gt;\n"
	myText += "	    &lt;WIPAllow&gt;0&lt;/WIPAllow&gt;\n"
	myText += "	  &lt;/entitlements&gt;\n"
	myText += "	  &lt;created /&gt;\n"
	myText += "	  &lt;cap&gt;1&lt;/cap&gt;\n"
	myText += "	  &lt;mission&gt;" + missionID + "&lt;/mission&gt;\n"
	myText += "	  &lt;server&gt;192.168.235.128:9339&lt;/server&gt;\n"
	myText += "	  &lt;instance&gt;54181934&lt;/instance&gt;\n"
	myText += "	  &lt;game&gt;BRAWLER&lt;/game&gt;\n"
	myText += "	  &lt;allowed_users&gt;" + inviter_id + "," + user + "&lt;/allowed_users&gt;\n"
	myText += "	  &lt;timestamp&gt;2016-05-16T18:14:20.753392&lt;/timestamp&gt;\n"
	myText += "	  &lt;code&gt;3e47d6ee069d21ea6cf183f4b726759c5cbd6df83d43c097be4beb0b2c3eaa13&lt;/code&gt;\n"
	myText += "	&lt;/ticket&gt;&lt;/response&gt;\n"

	myText += "  </body>\n"
	myText += "</response>\n"
	myList.add(myText)
	//myList.add("dummy item");

	  return myList
   }


   if (message.equals("get_game_room_invite"))
   {
	//*AS_SESSION_KEY : aSessionToken
	//*mission : m_1007_1_FingFangFoom001
	//*game : BRAWLER
	//*user : 3870526
	//*invitees : 3900010,3900009,3900011

	var missionID = String(obj.get(2))
	var inviter = String(obj.get(4))
	var invitees = String(obj.get(5))
	trace("get_game_room_invite missionID: " + missionID)
	handleGetGameRoom(inviter, missionID)
	
	  	// reference to the java package
	var _util = Packages.java.util
	// Create an ArrayList instance
	var myList = new _util.ArrayList()
	// Add one or more items to array list
	//myList.add("This is cool!")
	//myList.add((obj.get(1)).toString())

	var myText = "";
		//myText += bldg.S11.Title + "\n";
	myText += "<response>\n"
	myText += "  <status>200</status>\n"
	myText += "  <headers>\n"
	myText += "    <Content-Type>text/html; charset=utf-8</Content-Type>\n"
	myText += "  </headers>\n"
	myText += "  <body>&lt;response&gt;&lt;invitation&gt;\n"
	myText += "	  &lt;invitation_id&gt;1103&lt;/invitation_id&gt;\n"
	myText += "	&lt;/invitation&gt;\n"

	myText += "	&lt;ticket&gt;\n"
	myText += "	  &lt;player_id&gt;" + inviter + "&lt;/player_id&gt;\n"
	myText += "	  &lt;player_name&gt;RW1wZXJvciBJcmlkZXNjZW50IFdvbGY=&lt;/player_name&gt;\n"
	myText += "	  &lt;subscriber&gt;1&lt;/subscriber&gt;\n"
	myText += "	  &lt;session_key&gt;720f98cb79e59f0e6eb2c758915c53978fb0af09d7e5db86edcfd399168bc07c&lt;/session_key&gt;\n"
	myText += "	  &lt;squad_level&gt;6924&lt;/squad_level&gt;\n"
	myText += "	  &lt;entitlements&gt;\n"
	myText += "	    &lt;ArcadeAllow&gt;1&lt;/ArcadeAllow&gt;\n"
	myText += "	    &lt;CardGameAllow&gt;1&lt;/CardGameAllow&gt;\n"
	myText += "	    &lt;CatalogCountry&gt;US&lt;/CatalogCountry&gt;\n"
	myText += "	    &lt;ClientConsoleAllow&gt;0&lt;/ClientConsoleAllow&gt;\n"
	myText += "	    &lt;DemoLimitsOn&gt;0&lt;/DemoLimitsOn&gt;\n"
	myText += "	    &lt;Expiration&gt;0&lt;/Expiration&gt;\n"
	myText += "	    &lt;IsPayingSubscriber&gt;1&lt;/IsPayingSubscriber&gt;\n"
	myText += "	    &lt;MaxChallengeLevel&gt;65&lt;/MaxChallengeLevel&gt;\n"
	myText += "	    &lt;OpenChatAllow&gt;1&lt;/OpenChatAllow&gt;\n"
	myText += "	    &lt;ParentalCardGameDeny&gt;0&lt;/ParentalCardGameDeny&gt;\n"
	myText += "	    &lt;ParentalFriendingDeny&gt;0&lt;/ParentalFriendingDeny&gt;\n"
	myText += "	    &lt;ParentalHQDeny&gt;0&lt;/ParentalHQDeny&gt;\n"
	myText += "	    &lt;ParentalMissionsDeny&gt;0&lt;/ParentalMissionsDeny&gt;\n"
	myText += "	    &lt;PlayerCountry&gt;US&lt;/PlayerCountry&gt;\n"
	myText += "	    &lt;PlayerLanguage&gt;en&lt;/PlayerLanguage&gt;\n"
	myText += "	    &lt;ShieldHQAllow&gt;1&lt;/ShieldHQAllow&gt;\n"
	myText += "	    &lt;ShieldHeroesAllow&gt;1&lt;/ShieldHeroesAllow&gt;\n"
	myText += "	    &lt;ShieldPlayAllow&gt;1&lt;/ShieldPlayAllow&gt;\n"
	myText += "	    &lt;ShieldPrizeWheelAllow&gt;1&lt;/ShieldPrizeWheelAllow&gt;\n"
	myText += "	    &lt;ShoppingCatalog&gt;1&lt;/ShoppingCatalog&gt;\n"
	myText += "	    &lt;SubscriptionType&gt;1&lt;/SubscriptionType&gt;\n"
	myText += "	    &lt;UnityEditorAllow&gt;0&lt;/UnityEditorAllow&gt;\n"
	myText += "	    &lt;UseExternalShopping&gt;0&lt;/UseExternalShopping&gt;\n"
	myText += "	    &lt;WIPAllow&gt;0&lt;/WIPAllow&gt;\n"
	myText += "	  &lt;/entitlements&gt;\n"
	myText += "	  &lt;created /&gt;\n"
	myText += "	  &lt;cap&gt;1&lt;/cap&gt;\n"
	myText += "	  &lt;mission&gt;" + missionID + "&lt;/mission&gt;\n"
	myText += "	  &lt;server&gt;192.168.235.128:9339&lt;/server&gt;\n"
	myText += "	  &lt;instance&gt;54181934&lt;/instance&gt;\n"
	myText += "	  &lt;game&gt;BRAWLER&lt;/game&gt;\n"
	myText += "	  &lt;allowed_users&gt;" + inviter + "," + invitees + "&lt;/allowed_users&gt;\n"
	myText += "	  &lt;timestamp&gt;2016-05-16T18:14:20.753392&lt;/timestamp&gt;\n"
	myText += "	  &lt;code&gt;3e47d6ee069d21ea6cf183f4b726759c5cbd6df83d43c097be4beb0b2c3eaa13&lt;/code&gt;\n"
	myText += "	&lt;/ticket&gt;&lt;/response&gt;\n"

	myText += "  </body>\n"
	myText += "</response>\n"
	myList.add(myText)
	//myList.add("dummy item");

	  return myList
   }


   if (message.equals("get_game_room"))
   {
	var missionID = String(obj.get(1))
	var userID = String(obj.get(2))
	trace("get_game_room missionID: " + missionID)
	handleGetGameRoom(userID, missionID)
	
	  	// reference to the java package
	var _util = Packages.java.util
	// Create an ArrayList instance
	var myList = new _util.ArrayList()
	// Add one or more items to array list
	//myList.add("This is cool!")
	//myList.add((obj.get(1)).toString())

	var myText = "";
		//myText += bldg.S11.Title + "\n";
	myText += "<response>\n"
	myText += "  <status>200</status>\n"
	myText += "  <headers>\n"
	myText += "    <Content-Type>text/html; charset=utf-8</Content-Type>\n"
	myText += "  </headers>\n"
	myText += "  <body>&lt;response&gt;&lt;invitation&gt;\n"
	myText += "	  &lt;invitation_id&gt;1103&lt;/invitation_id&gt;\n"
	myText += "	&lt;/invitation&gt;\n"

	myText += "	&lt;ticket&gt;\n"
	myText += "	  &lt;player_id&gt;" + userID + "&lt;/player_id&gt;\n"
	myText += "	  &lt;player_name&gt;RW1wZXJvciBJcmlkZXNjZW50IFdvbGY=&lt;/player_name&gt;\n"
	myText += "	  &lt;subscriber&gt;1&lt;/subscriber&gt;\n"
	myText += "	  &lt;session_key&gt;720f98cb79e59f0e6eb2c758915c53978fb0af09d7e5db86edcfd399168bc07c&lt;/session_key&gt;\n"
	myText += "	  &lt;squad_level&gt;6924&lt;/squad_level&gt;\n"
	myText += "	  &lt;entitlements&gt;\n"
	myText += "	    &lt;ArcadeAllow&gt;1&lt;/ArcadeAllow&gt;\n"
	myText += "	    &lt;CardGameAllow&gt;1&lt;/CardGameAllow&gt;\n"
	myText += "	    &lt;CatalogCountry&gt;US&lt;/CatalogCountry&gt;\n"
	myText += "	    &lt;ClientConsoleAllow&gt;0&lt;/ClientConsoleAllow&gt;\n"
	myText += "	    &lt;DemoLimitsOn&gt;0&lt;/DemoLimitsOn&gt;\n"
	myText += "	    &lt;Expiration&gt;0&lt;/Expiration&gt;\n"
	myText += "	    &lt;IsPayingSubscriber&gt;1&lt;/IsPayingSubscriber&gt;\n"
	myText += "	    &lt;MaxChallengeLevel&gt;65&lt;/MaxChallengeLevel&gt;\n"
	myText += "	    &lt;OpenChatAllow&gt;1&lt;/OpenChatAllow&gt;\n"
	myText += "	    &lt;ParentalCardGameDeny&gt;0&lt;/ParentalCardGameDeny&gt;\n"
	myText += "	    &lt;ParentalFriendingDeny&gt;0&lt;/ParentalFriendingDeny&gt;\n"
	myText += "	    &lt;ParentalHQDeny&gt;0&lt;/ParentalHQDeny&gt;\n"
	myText += "	    &lt;ParentalMissionsDeny&gt;0&lt;/ParentalMissionsDeny&gt;\n"
	myText += "	    &lt;PlayerCountry&gt;US&lt;/PlayerCountry&gt;\n"
	myText += "	    &lt;PlayerLanguage&gt;en&lt;/PlayerLanguage&gt;\n"
	myText += "	    &lt;ShieldHQAllow&gt;1&lt;/ShieldHQAllow&gt;\n"
	myText += "	    &lt;ShieldHeroesAllow&gt;1&lt;/ShieldHeroesAllow&gt;\n"
	myText += "	    &lt;ShieldPlayAllow&gt;1&lt;/ShieldPlayAllow&gt;\n"
	myText += "	    &lt;ShieldPrizeWheelAllow&gt;1&lt;/ShieldPrizeWheelAllow&gt;\n"
	myText += "	    &lt;ShoppingCatalog&gt;1&lt;/ShoppingCatalog&gt;\n"
	myText += "	    &lt;SubscriptionType&gt;1&lt;/SubscriptionType&gt;\n"
	myText += "	    &lt;UnityEditorAllow&gt;0&lt;/UnityEditorAllow&gt;\n"
	myText += "	    &lt;UseExternalShopping&gt;0&lt;/UseExternalShopping&gt;\n"
	myText += "	    &lt;WIPAllow&gt;0&lt;/WIPAllow&gt;\n"
	myText += "	  &lt;/entitlements&gt;\n"
	myText += "	  &lt;created /&gt;\n"
	myText += "	  &lt;cap&gt;1&lt;/cap&gt;\n"
	myText += "	  &lt;mission&gt;" + missionID + "&lt;/mission&gt;\n"
	myText += "	  &lt;server&gt;192.168.235.128:9339&lt;/server&gt;\n"
	myText += "	  &lt;instance&gt;54181934&lt;/instance&gt;\n"
	myText += "	  &lt;game&gt;BRAWLER&lt;/game&gt;\n"
	myText += "	  &lt;allowed_users&gt;0&lt;/allowed_users&gt;\n"    // allowed_users = 0 means any users allowed
	myText += "	  &lt;timestamp&gt;2016-05-16T18:14:20.753392&lt;/timestamp&gt;\n"
	myText += "	  &lt;code&gt;3e47d6ee069d21ea6cf183f4b726759c5cbd6df83d43c097be4beb0b2c3eaa13&lt;/code&gt;\n"
	myText += "	&lt;/ticket&gt;&lt;/response&gt;\n"

	myText += "  </body>\n"
	myText += "</response>\n"
	myList.add(myText)
	//myList.add("dummy item");

	  return myList
   }

   if (message.equals("get_game_room_solo"))
   {
	var missionID = String(obj.get(1))
	var userID = String(obj.get(2))
	trace("get_game_room missionID: " + missionID)
	handleGetGameRoom(userID, missionID)
	
	  	// reference to the java package
	var _util = Packages.java.util
	// Create an ArrayList instance
	var myList = new _util.ArrayList()
	// Add one or more items to array list
	//myList.add("This is cool!")
	//myList.add((obj.get(1)).toString())

	var myText = "";
		//myText += bldg.S11.Title + "\n";
	myText += "<response>\n"
	myText += "  <status>200</status>\n"
	myText += "  <headers>\n"
	myText += "    <Content-Type>text/html; charset=utf-8</Content-Type>\n"
	myText += "  </headers>\n"
	myText += "  <body>&lt;response&gt;&lt;invitation&gt;\n"
	myText += "	  &lt;invitation_id&gt;1103&lt;/invitation_id&gt;\n"
	myText += "	&lt;/invitation&gt;\n"

	myText += "	&lt;ticket&gt;\n"
	myText += "	  &lt;player_id&gt;" + userID + "&lt;/player_id&gt;\n"
	myText += "	  &lt;player_name&gt;RW1wZXJvciBJcmlkZXNjZW50IFdvbGY=&lt;/player_name&gt;\n"
	myText += "	  &lt;subscriber&gt;1&lt;/subscriber&gt;\n"
	myText += "	  &lt;session_key&gt;720f98cb79e59f0e6eb2c758915c53978fb0af09d7e5db86edcfd399168bc07c&lt;/session_key&gt;\n"
	myText += "	  &lt;squad_level&gt;6924&lt;/squad_level&gt;\n"
	myText += "	  &lt;entitlements&gt;\n"
	myText += "	    &lt;ArcadeAllow&gt;1&lt;/ArcadeAllow&gt;\n"
	myText += "	    &lt;CardGameAllow&gt;1&lt;/CardGameAllow&gt;\n"
	myText += "	    &lt;CatalogCountry&gt;US&lt;/CatalogCountry&gt;\n"
	myText += "	    &lt;ClientConsoleAllow&gt;0&lt;/ClientConsoleAllow&gt;\n"
	myText += "	    &lt;DemoLimitsOn&gt;0&lt;/DemoLimitsOn&gt;\n"
	myText += "	    &lt;Expiration&gt;0&lt;/Expiration&gt;\n"
	myText += "	    &lt;IsPayingSubscriber&gt;1&lt;/IsPayingSubscriber&gt;\n"
	myText += "	    &lt;MaxChallengeLevel&gt;65&lt;/MaxChallengeLevel&gt;\n"
	myText += "	    &lt;OpenChatAllow&gt;1&lt;/OpenChatAllow&gt;\n"
	myText += "	    &lt;ParentalCardGameDeny&gt;0&lt;/ParentalCardGameDeny&gt;\n"
	myText += "	    &lt;ParentalFriendingDeny&gt;0&lt;/ParentalFriendingDeny&gt;\n"
	myText += "	    &lt;ParentalHQDeny&gt;0&lt;/ParentalHQDeny&gt;\n"
	myText += "	    &lt;ParentalMissionsDeny&gt;0&lt;/ParentalMissionsDeny&gt;\n"
	myText += "	    &lt;PlayerCountry&gt;US&lt;/PlayerCountry&gt;\n"
	myText += "	    &lt;PlayerLanguage&gt;en&lt;/PlayerLanguage&gt;\n"
	myText += "	    &lt;ShieldHQAllow&gt;1&lt;/ShieldHQAllow&gt;\n"
	myText += "	    &lt;ShieldHeroesAllow&gt;1&lt;/ShieldHeroesAllow&gt;\n"
	myText += "	    &lt;ShieldPlayAllow&gt;1&lt;/ShieldPlayAllow&gt;\n"
	myText += "	    &lt;ShieldPrizeWheelAllow&gt;1&lt;/ShieldPrizeWheelAllow&gt;\n"
	myText += "	    &lt;ShoppingCatalog&gt;1&lt;/ShoppingCatalog&gt;\n"
	myText += "	    &lt;SubscriptionType&gt;1&lt;/SubscriptionType&gt;\n"
	myText += "	    &lt;UnityEditorAllow&gt;0&lt;/UnityEditorAllow&gt;\n"
	myText += "	    &lt;UseExternalShopping&gt;0&lt;/UseExternalShopping&gt;\n"
	myText += "	    &lt;WIPAllow&gt;0&lt;/WIPAllow&gt;\n"
	myText += "	  &lt;/entitlements&gt;\n"
	myText += "	  &lt;created /&gt;\n"
	myText += "	  &lt;cap&gt;1&lt;/cap&gt;\n"
	myText += "	  &lt;mission&gt;" + missionID + "&lt;/mission&gt;\n"
	myText += "	  &lt;server&gt;192.168.235.128:9339&lt;/server&gt;\n"
	myText += "	  &lt;instance&gt;54181934&lt;/instance&gt;\n"
	myText += "	  &lt;game&gt;BRAWLER&lt;/game&gt;\n"
	myText += "	  &lt;allowed_users&gt;" + userID + "&lt;/allowed_users&gt;\n"    // allowed_users = 0 means any users allowed
	myText += "	  &lt;timestamp&gt;2016-05-16T18:14:20.753392&lt;/timestamp&gt;\n"
	myText += "	  &lt;code&gt;3e47d6ee069d21ea6cf183f4b726759c5cbd6df83d43c097be4beb0b2c3eaa13&lt;/code&gt;\n"
	myText += "	&lt;/ticket&gt;&lt;/response&gt;\n"

	myText += "  </body>\n"
	myText += "</response>\n"
	myList.add(myText)
	//myList.add("dummy item");

	  return myList
   }
   
  
   return "Unrecognized message."
   
   
   //var result = String( + " Received ");
   //return result;
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
	//trace("Event received: " + evt.name)	

	   /////// userExit, userLost, logOut ///////////////////////////
   if ((evt.name == "userExit") || (evt.name == "userLost") || (evt.name == "logOut"))
   {
	var uid = evt.userId
	if (evt.name == "userExit" || evt.name == "userLost") {
		removeMissionPlayers(uid.toString())
	}

	
	//Remove Player from active_players
	var removePlayerSql = "DELETE FROM active_players WHERE SfUserID=?"
	var prePareRemove = jdbconnection.prepareStatement(removePlayerSql)
	prePareRemove.setInit(1,uid)
	trace("sql= " + sql);
	
	var success = prePareRemove.executeUpdate();
				
		if (success != 0)
			trace("Record deleted!")
		else
			trace("Ouch, record deletion failed")
	
	prePareRemov.close()

	return;
   }

}

function handleNto(params, user, room)  // transfer ownership
{
	// var started = RoomVariable("started",1, 1)
	// _server.setRoomVariables(started, None,room)
	// trace("Room var: " + room.GetVariable("started"))
	//trace("handleNto() called!")	

	var uid = user.getUserId()

	var res = []		// The list of params	
	res[0] = "own"		// at index = 0, we store the command name
	res[1] = uid.toString() + "=|" + params[0]  // not sure if uid is right thing to send back (it's ownerId in client).
		
	// Send the raw message
	// _server.sendResponse() works just like any other requests
	// you have only to add the "str" argument to use the raw protocol
	_server.sendResponse(res, -1, null, [user], "str")

}

function handleTo(params, user, room)  // transfer ownership (autotransfer)
{
	 //trace("handleTo() called!")	

	 //var uid = user.getUserId()

	 //var res = []		// The list of params	
	 //res[0] = "own"		// at index = 0, we store the command name
	 //res[1] = uid.toString() + "=|" + params[0]  // not sure if uid is right thing to send back (it's ownerId in client).
		
	// Send the raw message
	// _server.sendResponse() works just like any other requests
	// you have only to add the "str" argument to use the raw protocol
	 //_server.sendResponse(res, -1, null, [user], "str")

}


function handleHeroCreate(params, user, room)
{
	//trace("handleHeroCreate() called!")	

	var hero = params.hero
	var key = params.key
	var blob = params.blob
	var shsoID = params.shsoID
	var uid = user.getUserId()

	//trace("hero = " + hero)
	//trace("key = " + key)
	//trace("blob = " + blob)

	//var jso = Packages.net.sf.json.JSONObject.fromObject(params);
	//trace(jso);
 

	var res = []		// The list of params	
	res[0] = "hero_create"		// at index = 0, we store the command name
	res[1] = uid	// fromRTCId - CSP not sure what this is supposed to be, guessing that it's user ID
	res[2] = hero	// hero
	res[3] = blob	// data

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

	// var updateLastUsedSQL = "UPDATE shso.heroes SET last_used = CURRENT_TIMESTAMP WHERE name = '" + hero + "' AND UserID = " + shsoID.toString();
	// var updatesuccess = dbManager.executeCommand(updateLastUsedSQL);
	// if (updatesuccess)
	// 	trace("Updated last used hero!");
	// else
	// 	trace("Ouch, update last used hero failed");

	currentZone = _server.getCurrentZone()
	//currentZone = helper.getZone(this.getOwnerZone)
	curRoom = currentZone.getRoom(room)
	//curRoom = _server.getCurrentRoom()
	cnt = curRoom.getUserCount();
	trace("curRoom.getUserCnt() = " + cnt)
	var users = curRoom.getAllUsers()

	///////// write active player info to active_players table in database.  ///////
	var insertSql = "INSERT INTO active_players (SfUserID, ShsoUserID, SfRoomID, Hero, BlobText) VALUES(?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE Hero = ? , BlobText = ?"
	var prePareRin = jdbconnection.prepareStatement(insertSql)
	prePareRin.setInit(1,uid)
	prePareRin.setInit(2,shsoID)
	prePareRin.setInit(3,curRoom.getId())
	prePareRin.setString(4,hero)
	prePareRin.setString(5,blob)
	prePareRin.setString(6,hero)
	prePareRin.setString(7,blob)

	trace("sql= " + sql);
	var success = prePareRin.executeUpdate()

		if (success != 0)
		trace("Record inserted!")
	else
		trace("Ouch, record insertion failed")
	prePareRin.close()
	/////////////////////////////////////////////////////////////////////


	for (i=0;i<cnt;i++){
		trace(users[i].getName())
	}

	// CSP - prob need to change next line to send to all clients in the room.
	//_server.sendResponse(res, -1, null, [user], "str")
	_server.sendResponse(res, -1, null, users, "str")


	///////// now query active_players table, send hero_create response for each active player in room to client.  ///////
	var getallUserSql = "SELECT * FROM active_players WHERE SfRoomID = ?" 
	var prePareRUser = jdbconnection.prepareStatement(getallUserSql)
	prePareRUser.setInit(1,curRoom.getId())

	var queryRes = prePareRUser.executeQuery()
	if (queryRes.next() != null)
	{
		
		do
		{

			res = []		// The list of params	
			res[0] = "hero_create"		// at index = 0, we store the command name
			res[1] = queryRes.getInt("SfUserID")	// fromRTCId - CSP not sure what this is supposed to be, guessing that it's user ID
			res[2] = queryRes.getString("Hero")	// hero
			res[3] = queryRes.getString("BlobText")	// data

			_server.sendResponse(res, -1, null, [user], "str")

			// now send playerVars msg for each active player to all users.  (maybe needs to be done at login, not here).
			//trace("SfUserID=" + tempRow.getItem("SfUserID").toString())
			// var pvUser = _server.getUserById(parseInt(tempRow.getItem("SfUserID")))
			var ResNsql = "SELECT * FROM shso.user WHERE id = ?"
			var prePareRrn = jdbconnection.prepareStatement(ResNsql)
			prePareRrn.setInit(1,queryRes.getInt("ShsoUserID"))
			
			var queryResName = prePareRrn.executeQuery();

			var player_name = queryResName.next().getString("Username");

			res = []
			res[0] = "playerVars"
			res[1] = queryRes.getInt("SfUserID").toString() + "|" + queryRes.getInt("ShsoUserID").toString() + "|" + player_name + "|true|1|1"
			//trace("Res[1]: " + res[1]);
			//_server.sendResponse(res, -1, null, [user], "str")
			_server.sendResponse(res, -1, null, users, "str")
			// i++;
			
			queryResName.close()

			prePareRrn.close()

		} while (queryRes.next())
	}
	else
		trace("DB Query failed")
	/////////////////////////////////////////////////////////////////////
	
	queryRes.close()

	
	prePareRUser.close()

}



