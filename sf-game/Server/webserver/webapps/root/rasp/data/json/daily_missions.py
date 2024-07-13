#
# friends info request
# 
#

import sys
import os
from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()

# note: smartfox is using python 2.2
sys.path.append('sf-game/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 
import datetime
import random
class daily_missions(HttpServlet):

	def __init__(self):
		self.htmlHead = "<html><head></head><body style='font-family:Verdana'>"
		self.closeHtml = "</body></html>"
	

	#
	# Handle GET requests  (this gets called from browser)
	#
	def doPost(self, request, response):	
		


		pass

		
	#
	# Handle POST requests (the client app is doing a POST request to anyone.py)
	#
	def doGet(self, request, response):
		if (pylibcsp.ipcheck(False)):   # don't process request if not a valid client
			return
		
		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

		# Get a reference to database manager
		db = zone.dbManager;

		# userID = None
		# session_token = None
		# #userID = "3870526"   # this line for doPost testing only !!!!!!!!!!!!!!!
		# for name in request.getParameterNames():
		# 	# if (name == "user"):
		# 		# userID = request.getParameter(name)
		# 	# if (name == "user_id"):
		# 		# userID = request.getParameter(name)
		# 	if (name == "AS_SESSION_KEY"):
		# 		session_token = request.getParameter(name)

		# if session_token is not None:
		# 	getUserID = "SELECT * from tokens WHERE token='" + session_token + "'"
		# 	tokenQuery = db.executeQuery(getUserID)
		# 	# userID = None
			
			
		# 	if tokenQuery.size() > 0:
		# 		userID = tokenQuery[0].getItem("userID")

		# # Update/Insert db record for this player
		# error = ""
		# sql = "INSERT INTO shso.equips (UserID, sidekick_id) values (" + userID + ", '" + sidekick_id + "') ON DUPLICATE KEY UPDATE sidekick_id = " + sidekick_id

		# success = db.executeCommand(sql)
		# if (not success):
		# 	error = "db query failed"
		missions = [
			['53013', 'be_1001_1_RedSkull001'], # Skull and Void!
			['70438', 'bo_1001_1_Abomination001'], # Abomination Obliteration!
			['75367', 'ca_1001_1_Venom001'], # Symbi-Oh No!
			['106530', 'fl_1002_1_Kingpin001'], # Hail to the Kingpin?!
			['26554', 'he_1001_1_Loki001'], # The Gods of Thunder?
			['27158', 'he_1002_1_YmirSurtur001'], # Freezer Burn!
			['27157', 'he_1003_1_Enchantress001'], # A Thousand Apples a Day
			['48794', 'li_1002_1_Juggernaut001'], # All For Jugger-Naught
			['1287', 'm_1001_1_DocOck001'], # Claw and Disorder!
			['1293', 'm_1006_1_DrDoom001'], # Send In the Clone-Bots!
			['1294', 'm_1007_1_FingFangFoom001'], # Flame On! (And On And On And On)
			['1289', 'm_1008_1_Ultron001'], # U Turned Out the Lights?!
			['341262', 'm_1008_1_Ultron001A'], # U Turned Out the Lights?! [CRISIS]
			['1290', 'm_1009_1_GreenGoblin001'], # Bombs Away!
			['330875', 'm_100S_1_Skydome001'], # Time to take A.I.M.!
			['60222', 'm_100X_1_Sabretooth001'], # Home Invasion!
			['1291', 'm_1011_1_GreenGoblin002'], # Breezy Riders!
			['1295', 'm_1013_1_Mystique001'], # Seeking Sneaky Mystique!
			['1296', 'm_1014_1_Annihilus001'], # Repellent Bugs
			['12727', 'm_1016_1_DocOck002'], # Ock It to Me!
			['12729', 'm_1018_1_FinFangFoom002'], # Very Bad Breath!
			['350432', 'm_101S_1_Skydome002'], # Strike of the Spider-Foes!
			['20549', 'm_1020_1_MoleMan001'], # Whack-a-Mole Man!
			['20550', 'm_1022_1_Ultron001'], # Flat Broke and Rusted
			['20553', 'm_1024_1_Lizard001'], # Lizard-ous to Your Health!
			['20551', 'm_1025_1_Mysterio001'], # Mysterio's Things Are Afoot!
			['215287', 'm_1027_1_Dracula001'], # Creatures of the Night!
			['367546', 'm_1027_1_Dracula001A'], # Creatures of the Night! [CRISIS]
			['218948', 'm_1028_1_Modok002'], # MODOK Madness!
			['221410', 'm_1028_1_Modok002A'], # MODOK Madness! [CRISIS]
			['229967', 'm_1029_1_Wendigo001'], # Wen-Di-Go Away!
			['229968', 'm_1029_1_Wendigo001A'], # Wen-Di-Go Away! [CRISIS]
			['350434', 'm_102S_1_Skydome003'], # Asgardian Gladiators!
			['350435', 'm_102S_1_Skydome003A'], # Asgardian Gladiators! [CRISIS]
			['313103', 'm_1031_1_TitaniumMan001'], # Extremis Measures!
			['399298', 'm_1033_1_ImpossibleMan001'], # The Impossible Holiday!
			['399299', 'm_1033_1_ImpossibleMan001A'], # The Impossible Holiday! [CRISIS]
			['442726', 'm_1035_1_WinterSoldier001'], # Blast From The Past!
			['442727', 'm_1035_1_WinterSoldier001A'], # Blast From The Past! [CRISIS]
			['488579', 'm_1036_1_SpiderMen001'], # Unfriendly Neighborhood Spider-Men!
			['488580', 'm_1036_1_SpiderMen001A'], # Unfriendly Neighborhood Spider-Men! [CRISIS]
			['506296', 'm_1037_1_Thanos001'], # The Infinite Thanos!
			['510231', 'm_1037_1_Thanos001A'], # The Infinite Thanos! [CRISIS]
			['548122', 'm_1039_1_ImpossibleMan002'], # Ho-Ho-Horrible!
			['548123', 'm_1039_1_ImpossibleMan002A'], # Ho-Ho-Horrible! [CRISIS]
			['355323', 'm_103S_1_Skydome004'], # Monster Smash!
			['355324', 'm_103S_1_Skydome004A'], # Monster Smash! [CRISIS]
			['652287', 'm_1042_1_MegaMission003A'], # The Final Fight For Fractals [CRISIS]
			['424999', 'm_105S_1_Skydome006'], # When Titans Clash!
			['425000', 'm_105S_1_Skydome006A'], # When Titans Clash! [CRISIS]
			['440276', 'm_106S_1_Skydome007'], # To Battle The Brotherhood!
			['440277', 'm_106S_1_Skydome007A'], # To Battle The Brotherhood! [CRISIS]
			['131615', 'ne_1001_1_Loki002'], # He's Baaack!
			['75396', 'ni_1001_1_Dormammu001'], # Dormammu Mia!
			['77216', 'ox_1001_1_Onslaught001'], # Onslaught Onslaught!
			['239136', 'ca_1001_1_Venom001A'], # Symbi-Oh No! [CRISIS]
			['560350', 'm_1025_1_Mysterio001A'], # Mysterio's Things Are Afoot! [CRISIS]
			['529179', 'm_1038_1_Deadpool001'], # Deadpool's Scare-Tacular Adventure!
			['534062', 'm_1038_1_Deadpool001A'], # Deadpool's Scare-Tacular Adventure! [CRISIS]
		]

		
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		# w.println((datetime.datetime.today() - datetime.datetime.utcfromtimestamp(0)).days)
		# w.println(daily_mission_id_index)
		random.seed((datetime.datetime.today() - datetime.datetime.utcfromtimestamp(0)).days)
		daily_mission_id_index = random.randint(0, len(missions) - 1)
		daily_mission_id_index = random.randint(0, len(missions) - 1) # Generate twice to avoid duplicates, maybe Python 2.2's random seed is bugged?
		daily_mission_id = str(missions[daily_mission_id_index][0])
		daily_mission_name_id = missions[daily_mission_id_index][1]
		daily_mission_id_file = open('sf-game/Server/webserver/webapps/root/rasp/data/json/daily_mission_bonus_id.txt', 'w')
		lines = daily_mission_id_file.readlines()
		if lines != [daily_mission_id]:
			sql = 'INSERT INTO daily_missions VALUES ("daily_mission_name", "' + daily_mission_name_id + '") ON DUPLICATE KEY UPDATE mission_name="' + daily_mission_name_id + '";'
			success = db.executeCommand(sql)
			daily_mission_id_file.write(daily_mission_id)
		daily_mission_id_file.close()
		w.println('{"daily_mission": {"ownable_type_id": '+ daily_mission_id +' }}')
		w.println("</body>")
		w.println("</response>")

		w.close()

	
		#pass
		