/*
 * SmartFoxServer PRO
 * Simple Extension Example
 * v 1.0.0
 *
 * (c) 2005 gotoAndPlay()
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



/*
 * Initializion point:
 *
 * this function is called as soon as the extension
 * is loaded in the server.
 *
 * You can add here all the initialization code
 *
 */
function init() {
	dbManager = _server.getDatabaseManager()
	// Using trace will send data to the server console
	trace("shsoevents init() called.")

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
function destroy() {
	trace("Bye bye!")
}


function applyXPBonus(userID, xp) {
	trace("applyXPBonus called")
	var sql = "SELECT * FROM mission_bonus WHERE MissionID = (SELECT MissionID FROM shso.active_missions WHERE shso.active_missions.UserID = " + _server.escapeQuotes(userID) + ");"
	var queryRes = dbManager.executeQuery(sql)
	var sql_global_multiplier = "SELECT * FROM mission_bonus WHERE MissionID = 'global_multiplier';"
	var queryRes_global = dbManager.executeQuery(sql_global_multiplier)
	var dailyMissionIDSQL = "SELECT CASE WHEN (SELECT mission_name FROM daily_missions WHERE name = 'daily_mission_name') = (SELECT MissionID FROM shso.active_missions WHERE shso.active_missions.UserID = " + _server.escapeQuotes(userID) + ") THEN (SELECT xp_multiplier FROM mission_bonus WHERE MissionID = 'daily_mission_bonus') ELSE '1.0' END AS xp_multiplier;"
	var queryRes_daily = dbManager.executeQuery(dailyMissionIDSQL)
	var multiplier = 1.0
	if (queryRes_global && queryRes_global.size() > 0) {
		multiplier = parseFloat(queryRes_global.get(0).getItem("xp_multiplier"));
	}
	if (queryRes && queryRes.size() > 0) {
		multiplier = parseFloat(queryRes.get(0).getItem("xp_multiplier")) * parseFloat(multiplier);
		//trace("XP Multiplier = " + multiplier.toString())
	}
	if (queryRes_daily && queryRes_daily.size() > 0) {
		multiplier = parseFloat(queryRes_daily.get(0).getItem("xp_multiplier")) * parseFloat(multiplier);
		//trace("XP Multiplier = " + multiplier.toString())
	}
	//trace("New XP Bonus = ")
	//trace((parseInt(xp)*multiplier).toString())
	// trace("multiplier=" + (parseFloat(xp)).toString() + " global=" + (parseFloat(multiplier)).toString())
	return (parseInt(parseFloat(xp) * parseFloat(multiplier))).toString()
}

function applyFractalsBonus(userID, fractals) {

	var sql = "SELECT * FROM mission_bonus WHERE MissionID = (SELECT MissionID FROM shso.active_missions WHERE shso.active_missions.UserID = " + _server.escapeQuotes(userID) + ");"
    // trace(sql)
	var queryRes = dbManager.executeQuery(sql)
	var sql_global_multiplier = "SELECT * FROM mission_bonus WHERE MissionID = 'global_multiplier';"
	var queryRes_global = dbManager.executeQuery(sql_global_multiplier)
	var dailyMissionIDSQL = "SELECT CASE WHEN (SELECT mission_name FROM daily_missions WHERE name = 'daily_mission_name') = (SELECT MissionID FROM shso.active_missions WHERE shso.active_missions.UserID = " + _server.escapeQuotes(userID) + ") THEN (SELECT fractals_multiplier FROM mission_bonus WHERE MissionID = 'daily_mission_bonus') ELSE '1.0' END AS fractals_multiplier;"
	var queryRes_daily = dbManager.executeQuery(dailyMissionIDSQL)
	var multiplier = 1.0
	if (queryRes_global && queryRes_global.size() > 0) {
		multiplier = parseFloat(queryRes_global.get(0).getItem("fractals_multiplier"));
	}
	if (queryRes && queryRes.size() > 0) {
		// var tempRow = queryRes.get(0)
		multiplier = parseFloat(queryRes.get(0).getItem("fractals_multiplier")) * parseFloat(multiplier);
		//trace("Fractals Multiplier = " + multiplier.toString())
        // trace("fractals multiplier=" + (parseFloat(queryRes.get(0).getItem("fractals_multiplier"))).toString() + " global=" + (parseFloat(multiplier)).toString())
	}
	if (queryRes_daily && queryRes_daily.size() > 0) {
		multiplier = parseFloat(queryRes_daily.get(0).getItem("fractals_multiplier")) * parseFloat(multiplier);
		//trace("XP Multiplier = " + multiplier.toString())
	}
	return (parseInt(parseFloat(fractals) * parseFloat(multiplier))).toString()
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
 *
 * Handle Client Requests
 *
 * cmd 		= a string with the client command to execute
 * params 	= list of parameters expected from the client
 * user 		= the User object representing the sender
 * fromRoom 	= the id of the room where the request was generated
 *
 */
function handleRequest(cmd, params, user, fromRoom) {
	if (cmd != "set_counter") {
		trace("events handleRequest() cmd= " + cmd)
	}
	else {
		trace("events handleRequest() cmd= " + cmd)
		var user_id = _server.escapeQuotes(getUserIdFromSFS(user));
		if (user_id) {
			user_id = user_id.toString()
			var counter_hero = _server.escapeQuotes((params.h).toString());
			var counter_id = _server.escapeQuotes((params.id).toString());
			var counter_value = _server.escapeQuotes((params.v).toString());
			if (counter_hero != '<unknown>') {
				counterUpdateSQL = "INSERT INTO counters VALUES(" + counter_id + ", " + user_id + ", '" + counter_hero + "', " + counter_value + ") ON DUPLICATE KEY UPDATE counters.hero = '" + counter_hero + "', counters.value = " + counter_value + ";";
				queryRes = dbManager.executeCommand(counterUpdateSQL)
			}
			else {
				trace('Counter set got unknown: ' + counter_id + ", " + counter_hero + ", " + counter_value)
			}
		}
		// trace("User: " + user_id + " Counter_set: " + counter_hero + ", " + counter_id + ", " + counter_value)
		// if (user_id == "53") {
		// 	// var session_token = params.AS_SESSION_KEY;
		// 	// user.isAdmin = true;
		// 	// var tokenSQL = "SELECT * from tokens WHERE token='" + _server.escapeQuotes(session_token) + "'";
		// 	// var tokenQuery = db.executeQuery(getUserID);
		// 	// var user_id;
		// 	// if (tokenQuery) {
		// 	// 	user_id = tokenQuery[0].getItem("userID");
		// 	// }
		// 	// if (user_id)

		// }
	}
	if (cmd == "send_mission_results") {
		response = {}
		response._cmd = "notification"
		response.message_type = "economy_message" //"achievement_complete"
		response.xp_added = params.xp_added
		response.fractals_added = params.fractals_added
		response.hero_name = params.hero
		response.achievement_id = "0"
		_server.sendResponse(response, -1, null, [user])
		var user_id = _server.escapeQuotes(getUserIdFromSFS(user)).toString();
		if (user_id == "53") {
			// Since the server will take a longer time to update the DB, calculate the new values.
			var xpsql = "select IF(GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(params.hero) + "' and userid=" + user_id + ") + " + _server.escapeQuotes(params.xp_added) + ") > GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(params.hero) + "' and userid=" + user_id + ")), GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(params.hero) + "' and userid=" + user_id + ") + " + _server.escapeQuotes(params.xp_added) + "), 'F') as `leveled_up`, xp + " + _server.escapeQuotes(params.xp_added) + " as `xp` from heroes where name = '" + _server.escapeQuotes(params.hero) + "' and userid=" + user_id + ";";
			var leveled_up_queryRes = dbManager.executeQuery(xpsql);
			if (leveled_up_queryRes && leveled_up_queryRes.size() > 0) {
				var tempRow = leveled_up_queryRes.get(0);
				var leveled_up = tempRow.getItem("leveled_up");
				var current_xp = tempRow.getItem("XP");
				if (leveled_up != "F") {
					response = {};
					response._cmd = "notification";
					response.message_type = "leveled_up";
					response.hero_current_xp = current_xp;
					response.hero_name = params.hero;
					response.new_level = leveled_up;
					response.achievement_id = "0";
					_server.sendResponse(response, -1, null, [user]);
				}
			}
			
		}
	}
	if (cmd == "send_mission_results2") {

		//Check for BonusXP
		//trace("CHECKING BONUS XP")
		var xp_multiplier = 1
		var localsql = "select IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>" + "60" + ",'T','F') FROM  active_potion_effects WHERE userid=" + _server.escapeQuotes(getUserIdFromSFS(user).toString()) + " and ownable_type_id = 298429"
		var queryRes = dbManager.executeQuery(localsql);
		if (queryRes && queryRes.size() > 0) {
			//XP Potion exists for that user
			//trace("BONUS POTION MIGHT EXIST, CHECKING BONUS!")

			var tempRow = queryRes.get(0)
			//dbxP = tempRow.getItem("Xp")
			var xpExist = tempRow.getItem("IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>" + "60" + ",'T','F')")

			if (xpExist == 'F') {
				//trace("XP BONUS EXIST!!!")
				xp_multiplier = 1.25; //Temp Value?
			} else {
				trace("XP BONUS EXPIRED! DELETING FROM DB!!")
				localsql = "delete from active_potion_effects where ownable_type_id = 298429 and userid = " + _server.escapeQuotes(getUserIdFromSFS(user).toString())
				queryRes = dbManager.executeCommand(localsql)
			}
		}

		var xpAward = Math.floor(parseInt(params.xp) * xp_multiplier)
		var coinsAward = params.coins
		var ticketsAward = params.tickets
		var response = {}

		response._cmd = "notification"
		response.message_type = "economy_message" //"achievement_complete"
		//trace("Results, userID = " + params.userID)
		//trace("Results, xpAward = " + xpAward)
		//trace("Results, Coins = " + coinsAward)

		response.xp_added = applyXPBonus(params.userID, xpAward)
		response.fractals_added = applyFractalsBonus(params.userID, coinsAward)
		// response.xp_added = xpAward
		// response.fractals_added = coinsAward
		response.hero_name = params.hero
		response.achievement_id = "0"
		_server.sendResponse(response, -1, null, [user])

		// addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero)
		//trace("BONUS Results, xpAward = " + applyXPBonus(params.userID, xpAward).toString())
		//trace("BONUS Results, Coins = " + applyFractalsBonus(params.userID, coinsAward).toString())
	}

	if (cmd == "consume_potion") {
		var response = {};
		trace("Attempting potion consumption\n");

		//Basic Info
		var userID = getUserIdFromSFS(user);
		var remaining = 0; //Fallback value

		//Get Remaining Potions of that type and set value to remaining
		var localsql = "SELECT quantity FROM shso.inventory WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.ownable_type_id.toString());
		var queryRes = dbManager.executeQuery(localsql);
		if (queryRes && queryRes.size() > 0) {
			remaining = queryRes.get(0).getItem("quantity") - 1;
		}

		if (remaining + 1 > 0) {
			//Apply value to DB
			localsql = "update shso.inventory set quantity=quantity - 1 WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.ownable_type_id.toString());
			if ((userID.toString()) == "53") {
				localsql = "update shso.inventory set quantity=quantity + 1 WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.ownable_type_id.toString());
			}
			var success = dbManager.executeCommand(localsql);

			//AUTHORIZE POTION
			response._cmd = "notification";
			response.message_type = "consume_potion_response";
			response.request_id = params.request_id;
			response.xp_added = "1000";
			response.hero_name = params.hero;
			response.achievement_id = "0";
			response.ownable_type_id = params.ownable_type_id;
			response.potions_remaining = remaining.toString();
			response.success = true;
			response.error_code = "";

			var currentZone = _server.getCurrentZone()
			//currentZone = helper.getZone(this.getOwnerZone)
			var curRoom = currentZone.getRoom(fromRoom)
			//curRoom = _server.getCurrentRoom()
			var cnt = curRoom.getUserCount();
			//trace("curRoom.getUserCnt() = " + cnt)
			var users = curRoom.getAllUsers()

			_server.sendResponse(response, -1, null, [user]);

			//START EFFECT
			//var stringEffect = "start_showing_effect%null%" + params.userID + "%" + params.ownable_type_id + "%" + "null";
			var stringEffect = [];
			stringEffect.push("start_showing_effect")
			stringEffect.push(user.getUserId())
			stringEffect.push(params.ownable_type_id)
			stringEffect.push("null")

			_server.sendResponse(stringEffect, -1, null, users, "str");//Will find all users

			//CHECK IF XP POTION
			var ownID = params.ownable_type_id;
			var xp = 0;

			if (ownID == 643112 || ownID == 298424) {
				xp = 1000;
			}
			if (ownID == 643114 || ownID == 298425) {
				xp = 5000;
			}

			if (xp > 0) {
				var response = {}
				// trace("Fractals BONUS: ")
				// trace(applyFractalsBonus(params.userID, "20"))
				response._cmd = "notification"
				response.message_type = "economy_message" //"achievement_complete"
				response.xp_added = xp.toString();
				response.hero_name = params.hero
				response.achievement_id = "0"
				_server.sendResponse(response, -1, null, [user])
				addRewardsToDb(response.xp_added, response.fractals_added, userID.toString(), params.hero, user)
			}

			//Add to active_potion_effects
			var speedBasedPotions = ["298429", "298427"]
			if (speedBasedPotions.indexOf(ownID.toString()) >= 0) {
				var localsql = "select * FROM  active_potion_effects WHERE userid=" + _server.escapeQuotes(userID.toString()) + " and ownable_type_id = " + _server.escapeQuotes(ownID.toString())
				var queryRes = dbManager.executeQuery(localsql)
				if (queryRes && queryRes.size() > 0) {
					localsql = "DELETE FROM shso.active_potion_effects WHERE userid=" + _server.escapeQuotes(userID.toString()) + " and ownable_type_id = " + _server.escapeQuotes(ownID.toString())
					var success = dbManager.executeCommand(localsql);
				}
				localsql = "INSERT INTO shso.active_potion_effects(userid,request_id,hero_name,ownable_type_id) VALUES(" + _server.escapeQuotes(userID.toString()) + ",1,\"" + "hero" + "\"," + _server.escapeQuotes(ownID.toString()) + ")"
				var success = dbManager.executeCommand(localsql);
				//trace("ADDED POTION TO DATABASE!");
			}


		} else {
			//trace("SHSO EVENT DELETING POTION!");

			var speedBasedPotions = ["298429", "298427"]
			if (speedBasedPotions.indexOf(params.ownable_type_id.toString()) >= 0) {
				var localsql = "INSERT INTO shso.active_potion_effects(userid,request_id,hero_name,ownable_type_id) VALUES(" + _server.escapeQuotes(userID.toString()) + ",1,\"" + _server.escapeQuotes(params.hero.toString()) + "\"," + _server.escapeQuotes(ownID.toString()) + ")"
				var sql = "DELETE FROM shso.inventory WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.ownable_type_id.toString()) + ";";
				var success = dbManager.executeCommand(sql);
				//trace("REMOVED POTION FROM DATABASE!");
			}

		}




		//addXpToDb(response.xp_added, params.userID, params.hero)
		// addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero);
	}

	if (cmd == "potion_cancel") {

		//trace("Attempting potion cancellation\n");
		//AUTHORIZE POTION
		var stringEffect = [];
		stringEffect.push("stop_showing_effect")
		stringEffect.push(user.getUserId())
		stringEffect.push(params.ownable_type_id.toString())
		stringEffect.push("null")

		var currentZone = _server.getCurrentZone()
		//currentZone = helper.getZone(this.getOwnerZone)
		var curRoom = currentZone.getRoom(fromRoom)
		//curRoom = _server.getCurrentRoom()
		var cnt = curRoom.getUserCount();
		//trace("curRoom.getUserCnt() = " + cnt)
		var users = curRoom.getAllUsers()

		_server.sendResponse(stringEffect, -1, null, users, "str");

		//Remove from active effects
		var shsoID = getUserIdFromSFS(user);
		var sql = "DELETE FROM shso.active_potion_effects WHERE userid = " + _server.escapeQuotes(shsoID.toString()) + " and ownable_type_id = " + _server.escapeQuotes(params.ownable_type_id.toString());
		var success = dbManager.executeCommand(sql);
	}

	if (cmd == "achievement_event") {
		trace('Achievement event: ' + params.str1)
		
		// dump object properties
		//trace("param type: " + typeof params)
		// for (var i in params) {
		// 	trace("params." + i+ " = " + params[i]);
		// }
		if (params.str1 == "asgard") {
			var currentZone = _server.getCurrentZone()
			room = currentZone.getRoomByName("Asgard")
			_server.joinRoom(user,-1,true,room.getId(),"",false,true)
			trace('User with hero: ' + params.hero + ' went to lobby: ' + params.str1)
		}
		if (params.str1 == "villain") {
			var currentZone = _server.getCurrentZone()
			room = currentZone.getRoomByName("Villainville")
			_server.joinRoom(user,-1,true,room.getId(),"",false,true)
			trace('User with hero: ' + params.hero + ' went to lobby: ' + params.str1)
		}
		if (params.str1 == "baxter") {
			var currentZone = _server.getCurrentZone()
			room = currentZone.getRoomByName("Baxter_Plaza")
			_server.joinRoom(user,-1,true,room.getId(),"",false,true)
			trace('User with hero: ' + params.hero + ' went to lobby: ' + params.str1)
		}
		if (params.str1 == "bugle") {
			var currentZone = _server.getCurrentZone()
			room = currentZone.getRoomByName("Daily_Bugle")
			_server.joinRoom(user,-1,true,room.getId(),"",false,true)
			trace('User with hero: ' + params.hero + ' went to lobby: ' + params.str1)
		}

		/*
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.event_type = social_pickup_fractal
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.event_sub_type = fractal
		   INFO   | jvm 1	| 2021/04/19 12:45:12 | [shso-events.as]: params.data1 = -10000


		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.event_type = social_pickup_troublebot
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.event_sub_type = troublebot
		   INFO   | jvm 1	| 2021/04/19 12:45:18 | [shso-events.as]: params.data1 = -10000

		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.event_type = social_pickup_token
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.event_sub_type = token
		   INFO   | jvm 1	| 2021/04/19 12:47:49 | [shso-events.as]: params.data1 = -10000

		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.event_type = social_pickup_robber
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.event_sub_type = robber
		   INFO   | jvm 1	| 2021/04/19 12:57:04 | [shso-events.as]: params.data1 = -10000

		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.event_type = generic_event
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.event_sub_type = poke_gumball
		   INFO   | jvm 1	| 2021/04/19 12:56:24 | [shso-events.as]: params.data1 = -10000

		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: param type: object
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.event_type = generic_event
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.event_sub_type = poke_tree
		   INFO   | jvm 1	| 2021/04/19 12:56:31 | [shso-events.as]: params.data1 = -10000


		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.event_type = convert_star_fractal
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.data2 = -10000
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.inc = 1
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.str1 =
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.str2 =
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.hero = iron_man
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.event_sub_type = star_fractal
		   INFO   | jvm 1	| 2021/04/19 12:56:55 | [shso-events.as]: params.data1 = -10000

		 */
		if (params.event_type == "ri") {
			if (params.event_sub_type == "sidekick_spawn_fractal") {
				var response = {}
				response._cmd = "notification"
				response.message_type = "economy_message" //"achievement_complete"
				response.fractals_added = 1
				response.hero_name = params.hero
				response.achievement_id = 0
				_server.sendResponse(response, -1, null, [user])

				//addXpToDb(response.xp_added, params.userID, params.hero)
				addRewardsToDb(0, response.fractals_added, params.userID, params.hero, user)
			}
			else if (params.event_sub_type == "sidekick_spawn_xp") {
				var response = {}
				response._cmd = "notification"
				response.message_type = "economy_message" //"achievement_complete"
				response.xp_added = 5;
				response.hero_name = params.hero
				response.achievement_id = 0
				_server.sendResponse(response, -1, null, [user])
				addRewardsToDb(response.xp_added, 0, params.userID, params.hero, user)
			}
		}
		if ((params.event_type == "social_pickup_troublebot") || (params.event_type == "social_pickup_robber") || (params.event_sub_type == "poke_gumball") || (params.event_sub_type == "poke_tree")) {
			var response = {}
			// trace("Fractals BONUS: ")
			// trace(applyFractalsBonus(params.userID, "20"))

			//Check for BonusXP
			//trace("CHECKING BONUS XP")
			var xp_multiplier = 1
			var localsql = "select IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>" + "60" + ",'T','F') FROM  active_potion_effects WHERE userid=" + _server.escapeQuotes(getUserIdFromSFS(user).toString()) + " and ownable_type_id = 298429"
			var queryRes = dbManager.executeQuery(localsql);
			if (queryRes && queryRes.size() > 0) {
				//XP Potion exists for that user
				//trace("BONUS POTION MIGHT EXIST, CHECKING BONUS!")

				var tempRow = queryRes.get(0)
				//dbxP = tempRow.getItem("Xp")
				var xpExist = tempRow.getItem("IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>" + "60" + ",'T','F')")

				if (xpExist == 'F') {
					trace("XP BONUS EXIST!!!")
					xp_multiplier = 1.25; //Temp Value?
				} else {
					trace("XP BONUS EXPIRED! DELETING FROM DB!!")
					localsql = "delete from active_potion_effects where ownable_type_id = 298429 and userid = " + _server.escapeQuotes(getUserIdFromSFS(user).toString())
					queryRes = dbManager.executeCommand(localsql)
				}
			}

			response._cmd = "notification"
			response.message_type = "economy_message" //"achievement_complete"
			if ((params.event_type == "social_pickup_robber")) {
				response.fractals_added = "15";
				response.xp_added = Math.floor(750 * xp_multiplier).toString();
			}
			else {
				response.fractals_added = "5";
				response.xp_added = Math.floor(300 * xp_multiplier).toString();
			}
			// response.xp_added = Math.floor(20 * xp_multiplier).toString();
			// response.fractals_added = "1"

			response.hero_name = params.hero
			response.achievement_id = "0"
			_server.sendResponse(response, -1, null, [user])

			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero, user)
		}

		if ((params.event_sub_type == "convert_star_fractal")) {
			var response = {}

			response._cmd = "notification"
			response.message_type = "economy_message" //"achievement_complete"
			response.fractals_added = "1"
			response.hero_name = params.hero
			response.achievement_id = "0"
			_server.sendResponse(response, -1, null, [user])
			response.xp_added = "0"
			
			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero, user)
		}


		if (params.event_type == "social_pickup_token") {
			var tokenCheckLastResetSQL = "SELECT DATEDIFF(CURRENT_TIMESTAMP, FROM_UNIXTIME(value)) AS datediff FROM counters WHERE counters.ID=503 AND counters.userID=" + _server.escapeQuotes(params.userID.toString()) + ";";
			var tokenCheckLastResetSQLResult = dbManager.executeQuery(tokenCheckLastResetSQL);
			var tokenCheckSQL = "SELECT BIT_COUNT(value) AS tokenCount FROM counters WHERE counters.ID=501 AND hero='" + _server.escapeQuotes(params.hero) + "' AND counters.userID=" + _server.escapeQuotes(params.userID.toString()) + ";";
			var tokenCheckSQLResult = dbManager.executeQuery(tokenCheckSQL);
			var tokenCount = 0;
			var tokenRewards = [200, 300, 400, 600, 1500];
			if (tokenCheckLastResetSQLResult && tokenCheckSQLResult && tokenCheckLastResetSQLResult.size() == 1 && tokenCheckSQLResult.size() == 1) {
				var datediff = tokenCheckLastResetSQLResult.get(0).getItem("datediff");
				var tokenCountValue = parseInt(tokenCheckSQLResult.get(0).getItem("tokenCount"));
				if (datediff !== "0" && tokenCountValue > 0) {
					tokenCount = tokenCountValue - 1;
				}
			}
			var response = {}

			response._cmd = "notification"
			response.message_type = "economy_message" //"achievement_complete"
			response.xp_added = (tokenRewards[tokenCount]).toString()
			trace(tokenRewards[tokenCount])
			response.hero_name = params.hero
			response.achievement_id = "0"
			_server.sendResponse(response, -1, null, [user])

			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, 0, params.userID, params.hero, user)
		}

		if (params.event_type == "social_pickup_fractal") {
			var response = {}

			response._cmd = "notification"
			response.message_type = "economy_message" //"achievement_complete"
			if (params.event_sub_type == "golden_fractal")
				response.fractals_added = "100"
			else
				response.fractals_added = "10"
			response.hero_name = params.hero
			response.achievement_id = "0"
			_server.sendResponse(response, -1, null, [user])
			response.xp_added = "0"

			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero, user)
		}
		if (params.event_type == "social_pickup_goldenfractal") {
			var response = {}

			response._cmd = "notification"
			response.message_type = "economy_message" //"achievement_complete"
			// if (params.event_sub_type == "golden_fractal")
			// 	response.fractals_added = "100"
			// else
			response.fractals_added = "100"
			response.hero_name = params.hero
			response.achievement_id = "0"
			_server.sendResponse(response, -1, null, [user])
			response.xp_added = "0"

			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero, user)
		}

		if (params.event_type == "consume_potion") {
			var response = {};

			response._cmd = "notification";
			response.message_type = "consume_potion_response";
			response.request_id = "53";
			response.xp_added = "1000"
			response.hero_name = params.hero
			response.achievement_id = "0"
			response.ownable_type_id = "643112";
			response.potions_remaining = "0";
			response.success = "1";
			// response.error_code = "";

			_server.sendResponse(response, -1, null, [user])
			response.fractals_added = 0

			//addXpToDb(response.xp_added, params.userID, params.hero)
			addRewardsToDb(response.xp_added, response.fractals_added, params.userID, params.hero, user)
		}
		if (params.event_type == "open_mystery_box") {
			var userID = getUserIdFromSFS(user);
			//trace("Attempting decoding");
			// trace("Got open mystery box message! from " + userID.toString());
			//var aString = "R28gdG8gaHR0cDovL3d3dy5jbHViem9iYmllcy5jb20=";
			//var d = Packages.it.gotoandplay.extensions.examples.Base64;
			//var dbPass = new java.lang.String(d.decode(aString));

			var response = {};

			response._cmd = "notification";
			response.message_type = "open_mystery_box_response";
			response.request_id = "53";
			response.silver_awarded = "666";
			response.gold_awarded = "6";

			//Was cards_awarded instead of rewards
			var reward = "";

			var potionOwnables = [77219, 77220, 77221, 87588, 265424, 265425, 266041, 266658, 266659, 266660, 275826, 275827, 291734, 291735, 291736, 298427];
			var sidekickOwnables = [291896, 291895, 291892, 291891, 291890, 291887, 291886, 291885, 291884, 291881, 291880, 291879, 291878, 291875, 291874, 291873, 291872, 291871, 291870, 291867, 291865, 291864, 291863, 291862, 291861, 291860, 291859, 291857, 291856, 291855, 291854, 291853, 291852, 291851, 291850, 291849, 291848, 291847, 291846, 291845, 291844, 291840, 291839, 291838, 291837, 291836, 291835, 291833, 291831, 291830, 291822, 291821, 291820, 291819, 291818, 291817, 291816, 291815, 291814, 291813, 291812, 291810, 291809, 291808, 291807, 291806, 291805, 291804, 291803, 291802, 291801, 291800, 291799, 291798, 291797, 291795, 291794, 291793, 291792, 291791, 291790, 291789, 291786, 291785, 291784, 291782, 291781, 291780, 291777, 291776, 291775, 291773, 291772, 291771, 291770];
			//var badgeOwnables = [295246,295253,295264,295269,295275,295280,295286,295287,295291,295302,295324,295328,295330,295344,295349,295351,295353,295241,295250,295252,295255,295265,295283,295289,295303,295304,295310,295314,295327,295338,295359,307610,307611,307612,295356,295358,295334,295333,295313,295279,295281,295307,295317,295311,295258,295242,295290,295296,295335,295347,295348,295355,307609,329039,329040,295315,329042,338211,295306,343703,295346,295336,295308,295251,295256,295345,295337,295316,295266,295312,295271,295273,295243];
			var xpBooster = [298429, 643112, 643114];
			// var heroTierWeak = [1266, 1268, 1269, 1277, 27156, 48793, 52412, 91256, 101637, 214675, 266657, 269101, 277658, 360207, 1246, 1252, 1245, 1278, 1250, 66229, 527338]
			var heroTierWeak = [1266, 1268, 1269, 1277, 27156, 48793, 52412, 91256, 101637, 214675, 266657, 269101, 277658, 360207, 1246, 1252, 1245, 1278, 1250, 66229]
			var heroTierStrong = [1243, 1258, 1273, 1276, 1283, 45791, 77195, 280723, 75417, 366320, 1247, 1256, 1285, 54819, 260524, 343704, 352266, 387700, 442110, 558517]
			//Fixed % Chances
			var sidekickAwarded = 1;
			var badgeAwarded = 1;
			var potionsAwarded = 3;
			var chanceHEROXP = Math.random(); //If less than 0.5 => XPBooster else Hero
			var chancePotionOrXP = Math.random(); //If less than 0.9, then potionownables, else xpbooster
			var chanceHERO = Math.random(); //0:0.35 PotionOwnables 0.35:0.4 xpBooster 0.4:0.7 Sidekick 0.7:0.9 Weak 0.9:0.98 Strong 0.98:1 Mystery/Special
			var toAward = "";
			// var inventoryCheckSQL = "SELECT ownable_type_id FROM catalog WHERE name IN (SELECT value FROM (SELECT 'venom_playable' AS value UNION ALL SELECT 'green_goblin_playable' UNION ALL SELECT 'titanium_man_playable' UNION ALL SELECT 'dr_octopus_playable' UNION ALL SELECT 'thanos_playable' UNION ALL SELECT 'sabretooth_playable' UNION ALL SELECT 'beta_ray_bill' UNION ALL SELECT 'ultron_playable' UNION ALL SELECT 'hulk_mrfixit' UNION ALL SELECT 'winter_soldier_playable' UNION ALL SELECT 'agent_coulson' UNION ALL SELECT 'rocket_raccoon' UNION ALL SELECT 'juggernaut_playable') AS names WHERE value NOT IN (SELECT Name FROM shso.heroes WHERE UserId = " + _server.escapeQuotes(userID.toString()) + "));";
			var inventoryCheckSQL = "SELECT value FROM (SELECT 'venom_playable' AS value UNION ALL SELECT 'green_goblin_playable' UNION ALL SELECT 'titanium_man_playable' UNION ALL SELECT 'dr_octopus_playable' UNION ALL SELECT 'thanos_playable' UNION ALL SELECT 'sabretooth_playable' UNION ALL SELECT 'beta_ray_bill' UNION ALL SELECT 'ultron_playable' UNION ALL SELECT 'hulk_mrfixit' UNION ALL SELECT 'winter_soldier_playable' UNION ALL SELECT 'agent_coulson' UNION ALL SELECT 'rocket_raccoon' UNION ALL SELECT 'juggernaut_playable') AS names WHERE value NOT IN (SELECT Name FROM shso.heroes WHERE UserId = " + _server.escapeQuotes(userID.toString()) + ");";
			var inventoryCheckSQLResult = dbManager.executeQuery(inventoryCheckSQL);
			var inventoryArray = [];

			for (var i = 0; i < inventoryCheckSQLResult.size(); i++) {
				var ownableTypeID = inventoryCheckSQLResult.get(i).getItem("ownable_type_id");
				inventoryArray.push(ownableTypeID);
				// trace(ownableTypeID.toString());
				// trace(userID);
			}
			
			var checkBoxesOpenedSQL = "SELECT SUM(quantity) as totalQuantity FROM boxes_opened WHERE UserID = " + _server.escapeQuotes(userID.toString()) + ";";
			var checkBoxesOpenedResult = dbManager.executeQuery(checkBoxesOpenedSQL);
			var pityFlag = false;
			if (checkBoxesOpenedResult && checkBoxesOpenedResult.size() > 0) {
				var totalQuantity = parseInt(checkBoxesOpenedResult.get(0).getItem("totalQuantity")) + 1;
				if (totalQuantity % 5 == 0) {
					pityFlag = true;
				}
				else{
					var checkPityFlagSQL = "SELECT quantity FROM boxes_opened WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND BoxId = -1;";
					var checkPityFlagResult = dbManager.executeQuery(checkPityFlagSQL);
					if (checkPityFlagResult && checkPityFlagResult.size() > 0) {
						var pityFlagDB = checkPityFlagResult.get(0).getItem("quantity");
						if (pityFlagDB == 1 || pityFlagDB == "1") {
							pityFlag = true;
						}
					}
				}
			}

			var boxID = params.str1.toString();
			if (
				pityFlag
			&& 
			(
				(boxID == "264813" && inventoryArray.indexOf("venom_playable") == -1 )
			|| (boxID == "300257" && inventoryArray.indexOf("green_goblin_playable") == -1)
			|| (boxID == "324767" && inventoryArray.indexOf("titanium_man_playable") == -1)
			|| (boxID == "329041" && inventoryArray.indexOf("dr_octopus_playable") == -1)
			|| (boxID == "345540" && inventoryArray.indexOf("thanos_playable") == -1)
			|| (boxID == "345541" && inventoryArray.indexOf("sabretooth_playable") == -1)
			|| (boxID == "385259" && inventoryArray.indexOf("beta_ray_bill") == -1)
			|| (boxID == "385260" && inventoryArray.indexOf("ultron_playable") == -1)
			|| (boxID == "385261" && inventoryArray.indexOf("hulk_mrfixit") == -1)
			|| (boxID == "454953" && inventoryArray.indexOf("winter_soldier_playable") == -1)
			|| (boxID == "459235" && inventoryArray.indexOf("agent_coulson") == -1)
			|| (boxID == "459236" && inventoryArray.indexOf("rocket_raccoon") == -1)
			|| (boxID == "459237" && inventoryArray.indexOf("juggernaut_playable") == -1)
			)
			) {
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace("DUPLICATE DUPLICATE");
				// trace(pityFlag);
				// trace(boxID);
				// trace(inventoryArray.indexOf('titanium_man_playable'));
				var disableDelayPitySQL = "INSERT INTO boxes_opened VALUES (" + _server.escapeQuotes(userID.toString()) + ",-1,0) ON DUPLICATE KEY UPDATE quantity = 0;";
				var disableDelayPityResult = dbManager.executeCommand(disableDelayPitySQL);
			}
			else if(pityFlag) {
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				// trace("NOT DUPLICATE");
				var delayPitySQL = "INSERT IGNORE INTO boxes_opened VALUES (" + _server.escapeQuotes(userID.toString()) + ",-1,1);";
				var delayPityResult = dbManager.executeCommand(delayPitySQL);
				pityFlag = false;
			}
			
			

			var i = 0;

			var boxIDMain = params.str1.toString();
			//HERO BOX OR NORMAL BOX
			var checkHasBoxSQL = "SELECT * from inventory WHERE quantity > 0 AND UserID =" + _server.escapeQuotes(userID.toString()) + " AND type=" + _server.escapeQuotes(_server.escapeQuotes(params.str1.toString())) + ";"
			var checkQueryRes = dbManager.executeQuery(checkHasBoxSQL);
			if (checkQueryRes && checkQueryRes.size() > 0)
			{
				if (boxIDMain == "385262") {

					/*var HeroBoxChanceVar = Math.random(); // 0:0.6 TierA 0.6:0.90 TierB 0.90:1 Ultra
					if(HeroBoxChanceVar <= 0.6 ){
						var randomID = Math.floor(Math.random() * heroTierWeak.length)
						reward = reward + "{\"ownableTypeID\":"+ heroTierWeak[randomID].toString() + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + heroTierWeak[randomID].toString()+"|hero";
					}else if(HeroBoxChanceVar >0.6 && HeroBoxChanceVar <= 0.9){
						var randomID = Math.floor(Math.random() * heroTierStrong.length)
						reward = reward + "{\"ownableTypeID\":"+ heroTierStrong[randomID].toString() + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + heroTierStrong[randomID].toString()+"|hero";
					}else{
						var UltraHeroes = ["378541:spider_man_iron","373658:destroyer_playable","290513:modok_playable","615323:war_machine_mk2"]
						var randomID = Math.floor(Math.random() * UltraHeroes.length)
						reward = reward + "{\"ownableTypeID\":"+ UltraHeroes[randomID].toString().split(":")[0] + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + UltraHeroes[randomID].toString()+"|hero";
					}*/

					localsql = "select * from mysterybox_loot_hero where heroname in (select name from allheroes where name not in (select name from UserHeroes where UserID=" + userID.toString() + "))"
					queryRes = dbManager.executeQuery(localsql)
					if (queryRes && queryRes.size() > 0) {
						//Can give out a hero
						var randomID = Math.floor(Math.random() * queryRes.size())
						var tempRow = queryRes.get(randomID)
						var ownableID = tempRow.getItem("ownable_type_id").toString()
						var heroName = tempRow.getItem("heroname").toString()
						reward = reward + "{\"ownableTypeID\":" + ownableID + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + ownableID + ":" + heroName + "|hero";

					} else {
						//Cannot give out a hero, giving a fallback hero instead
						reward = reward + "{\"ownableTypeID\":" + "1247" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + "1247" + "|hero";
					}


				} else {
					//POTION
					for (i = 0; i < potionsAwarded; i++) {
						if (chancePotionOrXP > 0.9 && i == 0) {
							var randomID = Math.floor(Math.random() * xpBooster.length)
							reward = reward + "{\"ownableTypeID\":" + xpBooster[randomID].toString() + ",\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";

							reward = reward + "|";
							toAward = toAward + xpBooster[randomID].toString() + "|potion" + ",";

						} else {
							var randomID = Math.floor(Math.random() * potionOwnables.length)
							reward = reward + "{\"ownableTypeID\":" + potionOwnables[randomID].toString() + ",\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";

							reward = reward + "|";
							toAward = toAward + potionOwnables[randomID].toString() + "|potion" + ",";

						}

					}
					//SIDEKICK
					for (i = 0; i < sidekickAwarded; i++) {
						var randomID = Math.floor(Math.random() * sidekickOwnables.length)
						reward = reward + "{\"ownableTypeID\":" + sidekickOwnables[randomID].toString() + ",\"quantity\":1,\"category\":\"sidekick\",\"rarity\":0}";

						reward = reward + "|";
						toAward = toAward + sidekickOwnables[randomID].toString() + "|sidekick" + ",";

					}
					//HERO
					if (chanceHERO <= 0.35 && !pityFlag) {
						var randomID = Math.floor(Math.random() * potionOwnables.length)
						reward = reward + "{\"ownableTypeID\":" + potionOwnables[randomID].toString() + ",\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";
						toAward = toAward + potionOwnables[randomID].toString() + "|potion";

					} else if (chanceHERO > 0.35 && chanceHERO <= 0.4 && !pityFlag) {
						var randomID = Math.floor(Math.random() * xpBooster.length)
						reward = reward + "{\"ownableTypeID\":" + xpBooster[randomID].toString() + ",\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";
						toAward = toAward + xpBooster[randomID].toString() + "|potion";
					} else if (chanceHERO > 0.4 && chanceHERO <= 0.7 && !pityFlag) {
						var randomID = Math.floor(Math.random() * sidekickOwnables.length)
						reward = reward + "{\"ownableTypeID\":" + sidekickOwnables[randomID].toString() + ",\"quantity\":1,\"category\":\"sidekick\",\"rarity\":0}";
						toAward = toAward + sidekickOwnables[randomID].toString() + "|sidekick";
					} else if (chanceHERO > 0.7 && chanceHERO <= 0.9 && !pityFlag) {
						var randomID = Math.floor(Math.random() * heroTierWeak.length)
						reward = reward + "{\"ownableTypeID\":" + heroTierWeak[randomID].toString() + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + heroTierWeak[randomID].toString() + "|hero";
					} else if (chanceHERO > 0.9 && chanceHERO <= 0.98 && !pityFlag) {
						var randomID = Math.floor(Math.random() * heroTierStrong.length)
						reward = reward + "{\"ownableTypeID\":" + heroTierStrong[randomID].toString() + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
						toAward = toAward + heroTierStrong[randomID].toString() + "|hero";
					} else {
						var boxID = params.str1.toString();
						if (boxID == "264813") {
							//Venom
							reward = reward + "{\"ownableTypeID\":" + "277659" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "277659" + "|hero";
						} else if (boxID == "300257") {
							//Goblin
							reward = reward + "{\"ownableTypeID\":" + "295978" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "295978" + "|hero";
						} else if (boxID == "324767") {
							//Titanium
							reward = reward + "{\"ownableTypeID\":" + "321671" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "321671" + "|hero";
						} else if (boxID == "329041") {
							//Ock
							reward = reward + "{\"ownableTypeID\":" + "321672" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "321672" + "|hero";
						} else if (boxID == "345540") {
							//Infinity
							reward = reward + "{\"ownableTypeID\":" + "338209" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "338209" + "|hero";
						} else if (boxID == "345541") {
							//Berserker
							reward = reward + "{\"ownableTypeID\":" + "357156" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "357156" + "|hero";
						} else if (boxID == "385259") {
							//StormBreaker
							reward = reward + "{\"ownableTypeID\":" + "371212" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "371212" + "|hero";
						} else if (boxID == "385260") {
							//Ultron
							reward = reward + "{\"ownableTypeID\":" + "420717" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "420717" + "|hero";
						} else if (boxID == "385261") {
							//Tool
							reward = reward + "{\"ownableTypeID\":" + "438440" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "438440" + "|hero";
						} else if (boxID == "454953") {
							//Winter
							reward = reward + "{\"ownableTypeID\":" + "445781" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "445781" + "|hero";
						} else if (boxID == "459235") {
							//Coulson
							reward = reward + "{\"ownableTypeID\":" + "454955" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "454955" + "|hero";
						} else if (boxID == "459236") {
							//Rocket
							reward = reward + "{\"ownableTypeID\":" + "508134" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "508134" + "|hero";
						} else if (boxID == "459237") {
							//JuggerTest
							reward = reward + "{\"ownableTypeID\":" + "557289" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
							toAward = toAward + "557289" + "|hero";
						}
					}
				}

				/*if(chanceHEROXP < 0.7){
					//XP Booster
					var randomID = Math.floor(Math.random() * xpBooster.length)
					reward = reward + "{\"ownableTypeID\":"+ xpBooster[randomID].toString() + ",\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";
					toAward = toAward + xpBooster[randomID].toString()+"|potion";
				}else{
					//HERO
					//DO SQL STUFF
					reward = reward + "{\"ownableTypeID\":"+ "440278" + ",\"quantity\":1,\"category\":\"h\",\"rarity\":0}";
					toAward = toAward + "440278"+"|hero"; //440278,1249
				}*/

				//response.rewards="{\"ownableTypeID\":510016,\"quantity\":1,\"category\":\"mdln\",\"rarity\":0}|{\"ownableTypeID\":440278,\"quantity\":1,\"category\":\"h\",\"rarity\":0}|{\"ownableTypeID\":1316,\"quantity\":1,\"category\":\"card\",\"rarity\":0}|{\"ownableTypeID\":265424,\"quantity\":1,\"category\":\"potion\",\"rarity\":0}|{\"ownableTypeID\":265425,\"quantity\":1,\"category\":\"potion\",\"rarity\":0}|{\"ownableTypeID\":298424,\"quantity\":1,\"category\":\"potion\",\"rarity\":0}|{\"ownableTypeID\":266660,\"quantity\":1,\"category\":\"potion\",\"rarity\":0}";
				response.rewards = reward;
				//trace(reward)
				_server.sendResponse(response, -1, null, [user], "xml");
				//trace("Should have sent mystery message");
				// response.xp_added = "1000"
				// response.hero_name = params.hero
				// response.achievement_id = "0"
				// response.ownable_type_id = "643112";
				// response.potions_remaining = "0";
				// response.success = "1";
				// response.error_code = "";

				//Update Remaining Boxes left!

				localsql = "update shso.inventory set quantity=quantity - 1 WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.str1.toString());
				if ((userID.toString()) == "53") {
					localsql = "update shso.inventory set quantity=quantity + 1 WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(params.str1.toString());
				}
				var success = dbManager.executeCommand(localsql);
				//Add items to the inventory
				var items = toAward.split(",")
				for each(var awardItem in items) {
					var award = awardItem.split("|");
					var awardOwnable = award[0];
					var heroName = "";
					var awardType = award[1];

					if (awardType == "hero") {
						//Check if hero exists...
						if (awardOwnable.indexOf(":") >= 0) {
							//HeroicBox exclusive hero won
							heroName = awardOwnable.split(":")[1]
							awardOwnable = awardOwnable.split(":")[0]
							//trace(heroName + "!!!!!!!!!" + awardOwnable)

						}
						if (params.str1.toString() == 385262) {
							localsql = "select * from heroes where UserId=" + _server.escapeQuotes(userID.toString()) + " and Name=\"" + _server.escapeQuotes(heroName) + "\"";
						} else {
							localsql = "select * from heroes where UserId=" + _server.escapeQuotes(userID.toString()) + " and Name=(select name from catalog where ownable_type_id = " + _server.escapeQuotes(awardOwnable) + ")";
						}
						//localsql = "select * from heroes where UserId="+userID.toString()+" and Name=(select name from catalog where ownable_type_id = "+awardOwnable+")";
						queryRes = dbManager.executeQuery(localsql);
						if (queryRes && queryRes.size() > 0) {
							//Award fractals incase of duplicate
							var response = {};
							response._cmd = "notification";
							response.message_type = "economy_message"; //"achievement_complete"
							if (params.str1.toString() == 385262) {
								response.fractals_added = "5000";
							} else {
								response.fractals_added = "250";
							}

							response.hero_name = params.hero;
							_server.sendResponse(response, -1, null, [user]);
							addRewardsToDb(0, 250, params.userID, params.hero, user)
						} else {
							//Award Hero
							//total_ownables
							var response = {};
							response._cmd = "notification";
							response.message_type = "economy_message"; //"achievement_complete"
							response.total_ownables = "1";
							response.ownableID1 = awardOwnable;
							response.hero_name = params.hero;
							response.achievement_id = "0";
							_server.sendResponse(response, -1, null, [user]);
							if (params.str1.toString() == 385262 && heroName != "" && heroName != " ") {
								localsql = "INSERT INTO heroes (UserID, Name) SELECT " + _server.escapeQuotes(userID.toString()) + ",  \"" + _server.escapeQuotes(heroName) + "\";";
							} else {
								localsql = "INSERT INTO heroes (UserID, Name) SELECT " + _server.escapeQuotes(userID.toString()) + ", name FROM catalog WHERE ownable_type_id = " + _server.escapeQuotes(awardOwnable) + ";";
							}

							queryRes = dbManager.executeCommand(localsql);
						}
					}
					else if (awardType == "potion") {
						var response = {};
						response._cmd = "notification";
						response.message_type = "economy_message"; //"achievement_complete"
						response.total_ownables = "1";
						response.ownableID1 = awardOwnable;
						response.hero_name = params.hero;
						response.achievement_id = "0";
						_server.sendResponse(response, -1, null, [user]);

						localsql = "select * from inventory where UserId=" + _server.escapeQuotes(userID.toString()) + " and type = " + _server.escapeQuotes(awardOwnable);
						queryRes = dbManager.executeQuery(localsql);
						if (queryRes && queryRes.size() > 0) {
							//Update Quantity
							localsql = "update shso.inventory set quantity=quantity + 1 WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND type = " + _server.escapeQuotes(awardOwnable);
						} else {
							localsql = "insert into shso.inventory(UserID,type,quantity,category,subscriber_only) VALUES(" + _server.escapeQuotes(userID.toString()) + "," + _server.escapeQuotes(awardOwnable) + ",1,\"potion\",0)";
						}
						queryRes = dbManager.executeCommand(localsql);
					}
					else if (awardType == "sidekick") {
						//Check if item exists...
						localsql = "select * from inventory where UserId=" + _server.escapeQuotes(userID.toString()) + " and type = " + _server.escapeQuotes(awardOwnable);
						queryRes = dbManager.executeQuery(localsql);
						if (queryRes && queryRes.size() > 0) {
							//Award fractals incase of duplicate
							var response = {};
							response._cmd = "notification";
							response.message_type = "economy_message"; //"achievement_complete"
							response.fractals_added = "50";
							response.hero_name = params.hero;
							_server.sendResponse(response, -1, null, [user]);
							addRewardsToDb(0, 50, params.userID, params.hero, user)
						} else {
							//Award Item
							//total_ownables
							var response = {};
							response._cmd = "notification";
							response.message_type = "economy_message"; //"achievement_complete"
							response.total_ownables = "1";
							response.ownableID1 = awardOwnable;
							response.hero_name = params.hero;
							response.achievement_id = "0";
							_server.sendResponse(response, -1, null, [user]);

							localsql = "insert into shso.inventory(UserID,type,quantity,category,subscriber_only) VALUES(" + _server.escapeQuotes(userID.toString()) + "," + _server.escapeQuotes(awardOwnable) + ",1,\"" + _server.escapeQuotes(awardType) + "\",0)";
							queryRes = dbManager.executeCommand(localsql);
						}
					}
				}
				var pityUpdateSQL = "INSERT INTO shso.boxes_opened (UserID, BoxId) VALUES(" +  _server.escapeQuotes(userID.toString()) + "," +  _server.escapeQuotes(params.str1.toString()) + ") ON DUPLICATE KEY UPDATE quantity = quantity + 1";
				queryRes = dbManager.executeCommand(pityUpdateSQL);
			}


		}
		if (params.event_type == "open_booster_pack") {

			//trace("Got open booster pack message!");
			var response = {};

			response._cmd = "notification";
			response.message_type = "open_booster_pack_response";
			response.request_id = "53";
			response.silver_awarded = "666";
			response.gold_awarded = "6";
			response.cards_awarded = "{\"ownableTypeID\":1316,\"quantity\":1,\"category\":\"card\",\"rarity\":0}";
			_server.sendResponse(response, -1, null, [user], "xml")
			trace("Should have sent booster pack message");


		}



		/*
		 *
		 * Send response back to client
		 *
		 * sendResponse(response, fromRoom, sender, recipients, type)
		 *
		 * response = an object with the _cmd property specifying the name of the response command
		 * fromRoom = the id of the room where the response comes from (-1 if not needed)
		 * sender   = the user sending the response (null if not needed)
		 * recipients = a list of user that should receive the reponse
		 * type = can be "xml" or "str". It represent the message format
		 *
		 */
		//var response = {}

		//response._cmd = "double"
		//response.values = []

		//_server.sendResponse(response, -1, null, [user])
	}
}

function addRewardsToDb(xp, fractals, userID, hero, user) {
	trace("Add rewards called, ID = " + userID)
	var checkSql = sql = "SELECT * FROM shso.user WHERE ID = " + _server.escapeQuotes(userID.toString());
	var queryRes = dbManager.executeQuery(checkSql);
	var currTimestamp = new Date().valueOf();
	var minTime = 60000;
	if (hero.indexOf("_reskin") > -1){
		hero = hero.substring(0, hero.indexOf("_reskin"))
	}

	// update fractals
	var sql = "UPDATE shso.user SET Fractals = Fractals + " + _server.escapeQuotes(fractals) + " WHERE ID = " + _server.escapeQuotes(userID.toString())
	var success = dbManager.executeCommand(sql);

	if (success)
		trace("Added fractals to DB!\nFractals = " + fractals)
	else
		trace("Ouch, fractal addition/update failed")

	// update XP
	var sql = "UPDATE shso.heroes SET Xp = Xp + " + xp + " WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND Name = '" + _server.escapeQuotes(hero) + "'"
	var success = dbManager.executeCommand(sql);

	if (success)
		trace("Added XP to DB!\nXP = " + xp)
	else
		trace("Ouch, xp addition/update failed")


	sql = "SELECT * FROM shso.heroes WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND Name = '" + _server.escapeQuotes(hero) + "'"

	// check XP in database and increse tier if necessary...
	var queryRes = dbManager.executeQuery(sql)
	var dbxP
	var dbTier
	if (queryRes != null) {
		for (var i = 0; i < queryRes.size(); i++) {
			var tempRow = queryRes.get(i)
			dbxP = tempRow.getItem("Xp")
			dbTier = tempRow.getItem("Tier")
		}
	} else
		trace("DB Query failed")

	// will prob need to factor in silver or gold badge ownership before increasing tier, at some point.
	var newTier = -1
	if ((dbxP >= 8100) && (dbTier == 0))
		newTier = 1
	if ((dbxP >= 40000) && (dbTier == 1))
		newTier = 2

	if (newTier > 0) {
		var sql = "UPDATE shso.heroes SET Tier = " + _server.escapeQuotes(newTier) + " WHERE UserID = " + _server.escapeQuotes(userID.toString()) + " AND Name = '" + _server.escapeQuotes(hero) + "'"
		var success = dbManager.executeCommand(sql);

		if (success)
			trace("Record inserted!")
		else
			trace("Ouch, record insertion failed")
	}

	var user_id = _server.escapeQuotes(getUserIdFromSFS(user)).toString();
	var xpsql = "select IF(GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(hero) + "' and userid=" + user_id + ")) > GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(hero) + "' and userid=" + user_id + ") - " + _server.escapeQuotes(xp) + "), GETLVL((select xp from heroes where name = '" + _server.escapeQuotes(hero) + "' and userid=" + user_id + ")), 'F') as `leveled_up`, xp from heroes where name = '" + _server.escapeQuotes(hero) + "' and userid=" + user_id + ";";
	// trace(xpsql)
	var leveled_up_queryRes = dbManager.executeQuery(xpsql);
	if (leveled_up_queryRes && leveled_up_queryRes.size() > 0) {
		var tempRow = leveled_up_queryRes.get(0);
		var leveled_up = tempRow.getItem("leveled_up");
		var current_xp = tempRow.getItem("XP");
		if (leveled_up != "F") {
			response = {};
			response._cmd = "notification";
			response.message_type = "leveled_up";
			response.hero_current_xp = current_xp;
			response.hero_name = hero;
			response.new_level = leveled_up;
			response.achievement_id = "0";
			_server.sendResponse(response, -1, null, [user]);
		}
	}

}


/*
 * This method handles internal events
 * Internal events are dispactched by the Zone or Room where the extension is attached to
 *
 * the (evt) object
 */
function handleInternalEvent(evt) {
	// Simply print the name of the event that was received
	//trace("Event received: " + evt.name)
}
