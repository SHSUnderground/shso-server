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
sys.path.append('sf-game/Server/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 

def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2

class counters_set(HttpServlet):

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

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

		# Get a reference to database manager
		db = zone.dbManager;

		userID = None
		session_token = None
		counter_name = None
		counter_type = None
		counter_value = None
		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			# if (name == "user"):
				# userID = request.getParameter(name)
			# if (name == "user_id"):
				# userID = request.getParameter(name)
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)
			elif (name == "hero_name"):
				hero_name = request.getParameter(name)
			elif (name == "counter"):
				counter_id = request.getParameter(name)
			elif (name == "amount"):
				difference_amount = request.getParameter(name)
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")

		# # Update/Insert db record for this player
		# error = ""
		# sql = "INSERT INTO shso.equips (UserID, sidekick_id) values (" + userID + ", '" + sidekick_id + "') ON DUPLICATE KEY UPDATE sidekick_id = " + sidekick_id
		# sql = "INSERT INTO shso.counters VALUES(%s, %s, %s, '%s') ON DUPLICATE KEY UPDATE value=;" % (escapeQuotes(userID), escapeQuotes(counter_name), escapeQuotes(counter_type), escapeQuotes(counter_value))
		sql = "UPDATE shso.counters SET value = value + %i WHERE userID = %s AND ID = %s AND hero = '%s';" % (int(difference_amount), counter_id, userID, hero_name)
		success = db.executeCommand(sql)
		success = False
		if (not success):
			error = "db query failed"
		w = response.getWriter()

		w.println("<response>")
		if success:
			w.println("  <status>200</status>")
		else:
			w.println("  <status>404</status>")
		# if userID == '53':
		# 	w.println(sql)
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		# brawler_missions_file = open('sf-game/Server/Server/webserver/webapps/root/rasp/data/json/brawler-missions', 'r')
		# for line in brawler_missions_file.readlines():
		# 	w.println(line)
		# ach_file.close()
		# w.println('{"daily_mission": {"ownable_type_id": 1294}}')
		w.println("</body>")
		w.println("</response>")

		w.close()

	
		#pass
		