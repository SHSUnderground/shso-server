#
# consume item request
# 
#

import sys
import os
import cgi
from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()

# note: smartfox is using python 2.2
sys.path.append('sf-game/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 


def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2

import time

def add_rewards_to_db(xp, fractals, user_id, hero, db):
	print("Add rewards called, ID = " + str(user_id))
	
	check_sql = sql = "SELECT * FROM shso.user WHERE ID = " + escapeQuotes(str(user_id))
	# Assume db is an appropriate database manager object.
	query_res = db.executeQuery(check_sql)

	current_time = time.time()
	curr_timestamp = current_time * 1000
	min_time = 60000
	last_timestamp = None
	
	if "_reskin" in hero:
		hero = hero.split("_reskin")[0]

	# Update fractals
	sql = "UPDATE shso.user SET Fractals = Fractals + " + escapeQuotes(str(fractals)) + " WHERE ID = " + escapeQuotes(str(user_id))
	success = db.executeCommand(sql)
	
	if success:
		print("Added fractals to DB!\nFractals = " + str(fractals))
	else:
		print("Ouch, fractal addition/update failed")
	
	# Update XP
	sql = "UPDATE shso.heroes SET Xp = Xp + " + str(xp) + " WHERE UserID = " + escapeQuotes(str(user_id)) + " AND Name = '" + escapeQuotes(hero) + "'"
	success = db.executeCommand(sql)
	
	if success:
		print("Added XP to DB!\nXP = " + str(xp))
	else:
		print("Ouch, xp addition/update failed")
	
	sql = "SELECT * FROM shso.heroes WHERE UserID = " + escapeQuotes(str(user_id)) + " AND Name = '" + escapeQuotes(hero) + "'"
	
	# Check XP in the database and increase tier if necessary
	query_res = db.executeQuery(sql)
	
	db_xp = None
	db_tier = None
	
	if query_res:
		for temp_row in query_res:
			db_xp = int(temp_row.getItem("Xp"))
			db_tier = int(temp_row.getItem("Tier"))
	else:
		print("DB Query failed")
	
	# You can add more conditions for tier updates if needed
	new_tier = db_tier
	
	if db_xp >= 8100 and db_tier < 1:
		new_tier = 1
	
	if db_xp >= 40000 and db_tier < 2:
		new_tier = 2
	
	if new_tier != db_tier:
		sql = "UPDATE shso.heroes SET Tier = " + escapeQuotes(str(new_tier)) + " WHERE UserID = " + escapeQuotes(str(user_id)) + " AND Name = '" + escapeQuotes(hero) + "'"
		success = db.executeCommand(sql)
		
		if success:
			print("Record inserted!")
		else:
			print("Ouch, record insertion failed")
	return db_xp, db_tier
class turn_in_score(HttpServlet):

	def __init__(self):
		self.htmlHead = "<html><head></head><body style='font-family:Verdana'>"
		self.closeHtml = "</body></html>"
	

	#
	# Handle GET requests  (this gets called from browser)
	#
	def doGet(self, request, response):	

	
		pass

		
	#
	# Handle POST requests (the client app is doing a POST request to anyone.py)
	#
	def doPost(self, request, response):
		if (pylibcsp.ipcheck(False)):   # don't process request if not a valid client
			return

		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to database manager
		db = zone.dbManager;


		# write debug info to log
		#sql = "INSERT INTO shso.log (Info) VALUES('entering friendsremove.py');"
		#success = db.executeCommand(sql)
		

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");


		# # Get parameters
		session_token = None
		userID = None
		hero_id = None
		score = None
		mission_id = None
		medal = None
		squad_count = None
		mission_type = None
		player_kos = None
		# ownable_type_id = None
		# useShards = None
		# potion_id = None
		# request_id = None
		# hero_name = None
		# potion_name = None
		medalMultipliers = [0, 1.25, 2.5, 3.8]
		squadMultipliers = [0, 1.25, 1.5, 2]
		missionTypeRewards = {
			"Easy": 25,
			"Short": 25,
			"Average": 55,
			"Long": 110,
			"Extra Long": 160,
			"mayhem": 10,
			# "crisis": 160
		}
		mission_classes = {
		'be_1001_1_RedSkull001A':'WIP', # Skull and Void! [CRISIS]
		'be_1001_1_RedSkull001': 'Average', # Skull and Void!
		'bo_1001_1_Abomination001':'Average', # Abomination Obliteration!
		'bo_1002_1_Modok001':'WIP', # MODOK Mo' Problems!
		'ca_1001_1_Venom001':'Average', # Symbi-Oh No!
		'ca_1001_1_Venom001A':'Extra Long', # Symbi-Oh No! [CRISIS]
		'fl_1001_1_Bullseye001':'WIP', # Hit the Bullseye! (Please)
		'fl_1002_1_Kingpin001':'Average', # Hail to the Kingpin?!
		'he_1001_1_Loki001':'Average', # The Gods of Thunder?
		'he_1002_1_YmirSurtur001':'Average', # Freezer Burn!
		'he_1003_1_Enchantress001':'Average', # A Thousand Apples a Day
		'li_1002_1_Juggernaut001':'Average', # All For Jugger-Naught
		'm_1001_1_DocOck001':'Average', # Claw and Disorder!
		'm_1002_1_SuperSkrull001':'WIP', # Un-Secret Invasion!
		'm_1005_1_Magneto001':'WIP', # Super-Sized and Magnetized!
		'm_1006_1_DrDoom001':'Easy', # Send In the Clone-Bots!
		'm_1006_1_DrDoom001A':'WIP', # Send In the Clone-Bots! [CRISIS]
		'm_1007_1_FingFangFoom001':'Average', # Flame On! (And On And On And On)
		'm_1008_1_Ultron001':'Easy', # U Turned Out the Lights?!
		'm_1008_1_Ultron001A':'Extra Long', # U Turned Out the Lights?! [CRISIS]
		'm_1009_1_GreenGoblin001':'Average', # Bombs Away!
		'm_100S_1_Skydome001':'Survival', # Time to take A.I.M.!
		'm_100S_1_Skydome001A':'WIP', # Time to Take A.I.M.! [CRISIS]
		'm_100X_1_Sabretooth001':'Easy', # Home Invasion!
		'm_1011_1_GreenGoblin002':'Average', # Breezy Riders!
		'm_1012_1_SuperSkrull002':'WIP', # Unstoppa-Skrull!
		'm_1013_1_Mystique001':'Average', # Seeking Sneaky Mystique!
		'm_1013_1_Mystique001A':'Long', # Seeking Sneaky Mystique! [CRISIS]
		'm_1014_1_Annihilus001':'Average', # Repellent Bugs
		'm_1015_1_SuperSkrull003':'WIP', # We Run in Peace
		'm_1016_1_DocOck002':'Average', # Ock It to Me!
		'm_1017_1_Magneto002':'WIP', # Magneteors!
		'm_1018_1_FinFangFoom002':'Average', # Very Bad Breath!
		'm_101S_1_Skydome002':'Survival', # Strike of the Spider-Foes!
		'm_101S_1_Skydome002A':'WIP', # Strike of the Spider-Foes! [CRISIS]
		'm_1020_1_MoleMan001':'Easy', # Whack-a-Mole Man!
		'm_1022_1_Ultron001':'Average', # Flat Broke and Rusted
		'm_1024_1_Lizard001':'Average', # Lizard-ous to Your Health!
		'm_1025_1_Mysterio001':'Long', # Mysterio's Things Are Afoot!
		'm_1025_1_Mysterio001A':'Extra Long', # Mysterio's Things Are Afoot! [CRISIS]
		'm_1026_1_Magneto003':'WIP', # Attack of the Iron Men!
		'm_1026_1_Magneto003A':'WIP', # Attack of the Iron Men! [CRISIS]
		'm_1027_1_Dracula001':'Easy', # Creatures of the Night!
		'm_1027_1_Dracula001A':'Long', # Creatures of the Night! [CRISIS]
		'm_1028_1_Modok002':'Average', # MODOK Madness!
		'm_1028_1_Modok002A':'Extra Long', # MODOK Madness! [CRISIS]
		'm_1029_1_Wendigo001':'Average', # Wen-Di-Go Away!
		'm_1029_1_Wendigo001A':'Long', # Wen-Di-Go Away! [CRISIS]
		'm_102S_1_Skydome003':'Survival', # Asgardian Gladiators!
		'm_102S_1_Skydome003A':'Survival', # Asgardian Gladiators! [CRISIS]
		'm_1031_1_TitaniumMan001':'Average', # Extremis Measures!
		'm_1031_1_TitaniumMan001A':'WIP', # Extremis Measures! [CRISIS]
		'm_1032_1_Malekith001':'WIP', # The Curse of Malekith!
		'm_1032_1_Malekith001A':'WIP', # The Curse of Malekith! [CRISIS]
		'm_1033_1_ImpossibleMan001':'Long', # The Impossible Holiday!
		'm_1033_1_ImpossibleMan001A':'Extra Long', # The Impossible Holiday! [CRISIS]
		'm_1034_1_Villains001':'WIP', # Bring On The Bad Guys!
		'm_1034_1_Villains001A':'WIP', # Bring on The Bad Guys! [CRISIS]
		'm_1035_1_WinterSoldier001':'Average', # Blast From The Past!
		'm_1035_1_WinterSoldier001A':'Extra Long', # Blast From The Past! [CRISIS]
		'm_1036_1_SpiderMen001':'Average', # Unfriendly Neighborhood Spider-Men!
		'm_1036_1_SpiderMen001A':'Average', # Unfriendly Neighborhood Spider-Men! [CRISIS]
		'm_1037_1_Thanos001':'Average', # The Infinite Thanos!
		'm_1037_1_Thanos001A':'Extra Long', # The Infinite Thanos! [CRISIS]
		'm_1038_1_Deadpool001':'Average', # Deadpool's Scare-Tacular Adventure!
		'm_1038_1_Deadpool001A':'Long', # Deadpool's Scare-Tacular Adventure! [CRISIS]
		'm_1039_1_ImpossibleMan002':'Average', # Ho-Ho-Horrible!
		'm_1039_1_ImpossibleMan002A':'Long', # Ho-Ho-Horrible! [CRISIS]
		'm_103S_1_Skydome004':'Survival', # Monster Smash!
		'm_103S_1_Skydome004A':'Survival', # Monster Smash! [CRISIS]
		'm_1040_1_MegaMission001':'WIP', # The Fight For Fractals!
		'm_1040_1_MegaMission001A':'WIP', # The Fight For Fractals! [CRISIS]
		'm_1041_1_MegaMission002':'WIP', # The Fight For Fractals Continues!
		'm_1041_1_MegaMission002A':'WIP', # The Fight For Fractals Continues! [CRISIS]
		'm_1042_1_MegaMission003':'WIP', # The Final Fight For Fractals!
		'm_1042_1_MegaMission003A':'Extra Long', # The Final Fight For Fractals [CRISIS]
		'm_104S_1_Skydome005':'Survival', # Doomsday in Space!
		'm_104S_1_Skydome005A':'Survival', # Doomsday in Space! [CRISIS]
		'm_105S_1_Skydome006':'Survival', # When Titans Clash!
		'm_105S_1_Skydome006A':'Survival', # When Titans Clash! [CRISIS]
		'm_106S_1_Skydome007':'Survival', # To Battle The Brotherhood!
		'm_106S_1_Skydome007A':'Survival', # To Battle The Brotherhood! [CRISIS]
		'ne_1001_1_Loki002':'Average', # He's Baaack!
		'ni_1001_1_Dormammu001':'Average', # Dormammu Mia!
		'ox_1001_1_Onslaught001':'Average', # Onslaught Onslaught!
		}

		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_token = request.getParameter(name)
			if name == "score":   # AS_SESSION_KEY
				score = request.getParameter(name)
			if name == "hero_id":
				hero_id = request.getParameter(name)
			# if name == "mission_id":
			# 	mission_id = request.getParameter(name)
			if name == "medal":
				medal = request.getParameter(name)
			if name == "hero_id":
				hero_id = request.getParameter(name)
			if name == "squad_count":
				squad_count = request.getParameter(name)
			if name == "player_kos":
				player_kos = request.getParameter(name)
			# if name == "mission_type":
			# 	mission_type = request.getParameter(name)
		# 	if name == "user_id":   # user ID
		# 		user = request.getParameter(name)
		# 	if name == "potion_id":
		# 		ownable_type_id = request.getParameter(name)
		# 	if name == "hero_name":
		# 		hero_name = request.getParameter(name)
		# 	if name == "request_id":
		# 		request_id = request.getParameter(name)
		# #target = 3900009  # temp for testing	
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")
		xp_potion_multiplier = 1
		potionCheckSQL = "select IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>" + "60" + ",'T','F') FROM active_potion_effects WHERE userid=" + userID + " and ownable_type_id = 298429"
		potionCheckQueryRes = db.executeQuery(potionCheckSQL)
		if potionCheckQueryRes and potionCheckQueryRes.size() > 0:
			xp_potion_check = potionCheckQueryRes[0].getItem(0)

			if xp_potion_check == 'F':
				xp_potion_multiplier = 1.25
			else:
				print("XP BONUS EXPIRED! DELETING FROM DB!!")
				deletePotion = "delete from active_potion_effects where ownable_type_id = 298429 and userid = " + userID
				db.executeCommand(deletePotion)
		
		global_multiplierSQL = "SELECT * FROM mission_bonus WHERE MissionID = 'global_multiplier';"
		global_multiplierQueryRes = db.executeQuery(global_multiplierSQL)
		if global_multiplierQueryRes and global_multiplierQueryRes.size() > 0:
			global_multiplier_fractals = float(global_multiplierQueryRes[0].getItem('fractals_multiplier'))
			global_multiplier_xp = float(global_multiplierQueryRes[0].getItem('xp_multiplier'))

		dailySQL = "SELECT mission_name FROM daily_missions WHERE name = 'daily_mission_name'"
		dailyQueryRes = db.executeQuery(dailySQL)
		if dailyQueryRes and dailyQueryRes.size() > 0:
			daily_mission = dailyQueryRes[0].getItem('mission_name')
		

		current_missionSQL = "SELECT MissionID FROM shso.active_missions WHERE shso.active_missions.UserID = " + escapeQuotes(userID)
		current_missionQueryRes = db.executeQuery(current_missionSQL)
		if current_missionQueryRes and current_missionQueryRes.size() > 0:
			mission_id = current_missionQueryRes[0].getItem('MissionID')
		
		mission_multiplierSQL = "SELECT * FROM mission_bonus WHERE MissionID = '" + mission_id + "';"
		mission_multiplierQueryRes = db.executeQuery(mission_multiplierSQL)
		mission_multiplier_fractals = 0
		mission_multiplier_xp = 0
		if mission_multiplierQueryRes and mission_multiplierQueryRes.size() > 0:
			mission_multiplier_fractals = float(mission_multiplierQueryRes[0].getItem('fractals_multiplier'))
			if mission_multiplier_fractals == 1:
				mission_multiplier_fractals = 0
			mission_multiplier_xp = float(mission_multiplierQueryRes[0].getItem('xp_multiplier'))
			if mission_multiplier_xp == 1:
				mission_multiplier_xp = 0

		medal_multiplier = medalMultipliers[int(medal)]

		team_up_multiplier = squadMultipliers[int(squad_count) - 1]

		if mission_id == daily_mission:
			team_up_multiplier = 1.5

		death_penalty = 0.2 * int(player_kos)
		if medal_multiplier == 0 and team_up_multiplier == 0:
			medal_multiplier = 1
		multipliers = medal_multiplier - death_penalty + team_up_multiplier
		if death_penalty > (medal_multiplier + team_up_multiplier):
			multipliers = 1
		w = response.getWriter()

		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		# w.println("  OK")
		# if hero_id.lower() not in testers:
		# 	if mission_id in mission_classes and mission_classes[mission_id] == 'Survival':
		# 		fractals = 10
		# 		xp = 70
		# 	elif mission_id[-1] == 'A':
		# 		fractals = 150
		# 		xp = 300
		# 	elif mission_id.find('100M') > -1:
		# 		fractals = 5
		# 		xp = 35
		# 	else:
		# 		fractals = 50
		# 		xp = 350
		# 	old_multipliers_fractals = global_multiplier_fractals * mission_multiplier_fractals
		# 	old_multipliers_xp = global_multiplier_xp * mission_multiplier_xp
		# 	if mission_id == daily_mission:
		# 		daily_multiplierSQL = "SELECT * FROM mission_bonus WHERE MissionID = 'daily_mission_bonus';"
		# 		daily_multiplierQueryRes = db.executeQuery(daily_multiplierSQL)
		# 		if daily_multiplierQueryRes and daily_multiplierQueryRes.size() > 0:
		# 			daily_multiplier_fractals = float(daily_multiplierQueryRes[0].getItem('fractals_multiplier'))
		# 			daily_multiplier_xp = float(daily_multiplierQueryRes[0].getItem('xp_multiplier'))
		# 		old_multipliers_fractals = old_multipliers_fractals * daily_multiplier_fractals
		# 		old_multipliers_xp = old_multipliers_xp * daily_multiplier_xp
		# 	fractals = old_multipliers_fractals * fractals
		# 	xp = old_multipliers_xp * xp
		# if hero_id.lower() in testers:
		if mission_id not in mission_classes:
			mission_reward = missionTypeRewards['mayhem'] * 1.5
		elif mission_classes[mission_id] != 'Survival':
			mission_reward = missionTypeRewards[mission_classes[mission_id]] * 1.5
			# w.println("mission_ID: " + str(mission_id) + " mission class: " + str(mission_classes[mission_id]) + " missionTypeRewards: " + str(missionTypeRewards[mission_classes[mission_id]]))
		elif mission_classes[mission_id] == 'Survival':
			mission_reward = round((int(score) / 1000) + 0.1)
			# while mission_reward > 10000:
			# 	mission_reward = round((int(score) / 1000) + 0.1)
		# elif mission_reward :
		# 	mission_reward = 0
		if global_multiplier_fractals > 1:
			fractals = mission_reward * (multipliers + global_multiplier_fractals + mission_multiplier_fractals)
		elif mission_id in mission_classes and mission_classes[mission_id] == 'Survival':
			fractals = mission_reward * (multipliers + mission_multiplier_fractals + death_penalty)
		else:
			fractals = mission_reward * (multipliers + mission_multiplier_fractals)
		# w.println("mission_reward: " + str(mission_reward) + "multipliers: " + str(multipliers))
		fractals = round(fractals + 0.1)
		if global_multiplier_xp > 1:
			xp = mission_reward * (multipliers + global_multiplier_xp + mission_multiplier_xp) * 3
		else:
			xp = mission_reward * (multipliers + mission_multiplier_xp) * 3
		if mission_id in mission_classes and mission_classes[mission_id] == 'Survival':
			if fractals > 1000:
				fractals = 1000
				xp = fractals * 3
		if xp_potion_multiplier != 1:
			xp = xp * xp_potion_multiplier
		heroSQL = "SELECT * from equips where UserID = " + escapeQuotes(userID)
		heroQueryRes = db.executeQuery(heroSQL)
		if heroQueryRes and heroQueryRes.size() > 0:
			heroName = heroQueryRes[0].getItem("hero_name")
		if heroName == 'punisher_thunderbolts':
			fractals *= 0.5
			xp *= 0.5
		add_rewards_to_db(xp, fractals, userID, heroName, db)
		leaderboardInsertSQL = "INSERT INTO shso.leaderboard (UserID, MissionID, score, Hero, Multiplayer) VALUES (" + escapeQuotes(userID) + ", '" + escapeQuotes(mission_id) + "', " + escapeQuotes(score) + ", '" + escapeQuotes(heroName) + "', " + str(bool(int(squad_count) > 1)) + ") ON DUPLICATE KEY UPDATE Hero = IF(score < " + escapeQuotes(score) + ", '" + escapeQuotes(heroName) + "', Hero), timestamp = IF(score < " + escapeQuotes(score) + ", CURRENT_TIMESTAMP, timestamp), score = IF(score < " + escapeQuotes(score) + ", " + escapeQuotes(score) + ", score);"
		db.executeCommand(leaderboardInsertSQL)
		# if int(userID) == 53:
		# 	w.println(leaderboardInsertSQL)
		missionTableCleanupSQL = "DELETE FROM active_missions WHERE UserID = " + escapeQuotes(userID) + ";"
		db.executeCommand(missionTableCleanupSQL)
		# w.println("  &lt;potion&gt;")
		# w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		w.println(str(fractals) + ',' + str(xp))
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()