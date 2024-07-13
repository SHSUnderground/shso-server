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

class get_high_scores(HttpServlet):

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
		is_multiplayer_score = None
		mission_id = None
		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_token = request.getParameter(name)
			if name == "hero_id":
				hero_id = request.getParameter(name)
			if name == "mission_id":
				mission_id = request.getParameter(name)
			if name == "is_multiplayer_score":
				is_multiplayer_score = len(request.getParameterValues("is_multiplayer_score")) - 1
				# if is_multiplayer_score is not None: # Because it is duplicated in sent form data.
				# else:
				# 	is_multiplayer_score = request.getParameter(name)
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")
		
		w = response.getWriter()
		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		leaderboardSQL = "SELECT shso.LeaderboardInfo.* FROM shso.LeaderboardInfo where MONTH(shso.LeaderboardInfo.timestamp) = MONTH(CURRENT_TIMESTAMP) AND YEAR(shso.LeaderboardInfo.timestamp) = YEAR(CURRENT_TIMESTAMP) AND shso.LeaderboardInfo.MissionID = " + escapeQuotes(mission_id) + " AND Multiplayer = " + escapeQuotes(is_multiplayer_score)
		if int(hero_id) != 0:
			leaderboardSQL += " AND Hero = " + escapeQuotes(hero_id)
		leaderboardSQL += " ORDER BY avg_group_score_rounded DESC;"
		leaderboardRes = db.executeQuery(leaderboardSQL)
		# if int(userID) == 53:
		# 	w.println("&lt;leadersql&gt;")
		# 	w.println(leaderboardSQL)
		# 	w.println("&lt;/leadersql&gt;")
		w.println("&lt;scores&gt;")
		w.println("&lt;leaders&gt;")
		rank = 1
		if leaderboardRes and leaderboardRes.size() > 0:
			for row in leaderboardRes:
				hero = row.getItem("Hero")
				score = row.getItem("avg_group_score_rounded")
				player = row.getItem("Username")
				w.println("&lt;leader&gt;")
				w.println("&lt;rank&gt;" + str(rank) + "&lt;/rank&gt;")
				w.println("&lt;player&gt;" + str(player) + "&lt;/player&gt;")
				w.println("&lt;hero&gt;" + str(hero) + "&lt;/hero&gt;")
				w.println("&lt;score&gt;" + str(score) + "&lt;/score&gt;")
				w.println("&lt;/leader&gt;")
				rank += 1
		# if mission_classes[mission_id] != 'Survival':
		# 	mission_reward = missionTypeRewards[mission_classes[mission_id]]
			# w.println("mission_ID: " + str(mission_id) + " mission class: " + str(mission_classes[mission_id]) + " missionTypeRewards: " + str(missionTypeRewards[mission_classes[mission_id]]))
		w.println("&lt;/leaders&gt;")
		w.println("&lt;/scores&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()