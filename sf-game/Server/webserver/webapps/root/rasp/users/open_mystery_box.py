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

def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2

class open_mystery_box(HttpServlet):

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
		sidekick_id = None
		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			# if (name == "user"):
				# userID = request.getParameter(name)
			# if (name == "user_id"):
				# userID = request.getParameter(name)
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)
		# getUserID = "SELECT * from tokens WHERE token='" + session_token + "'"
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")

		# # Update/Insert db record for this player
		# error = ""
		# sql = "INSERT INTO shso.equips (UserID, sidekick_id) values (" + userID + ", '" + sidekick_id + "') ON DUPLICATE KEY UPDATE sidekick_id = " + sidekick_id

		# success = db.executeCommand(sql)
		# if (not success):
		# 	error = "db query failed"
									
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/xml; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("  &lt;document&gt;")
		w.println("&lt;player_id&gt;" + str(userID) + "&lt;/player_id&gt;")
		w.println("""

  &lt;_cmd&gt;notification&lt;/_cmd&gt;
  &lt;message_type&gt;open_mystery_box_response&lt;/message_type&gt;
	&lt;request_id&gt;9588428&lt;/request_id&gt;
  &lt;silver_awarded&gt;0&lt;/silver_awarded&gt;
  &lt;gold_awarded&gt;0&lt;/gold_awarded&gt;
  &lt;includes_super_rare&gt;true&lt;/includes_super_rare&gt;
&lt;rewards&gt;
{"ownableTypeID":15237,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15238,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15239,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15240,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15241,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15242,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15249,"quantity":1,"category":"potion","rarity"=0}|
    {"ownableTypeID":15250,"quantity":1,"category":"potion","rarity"=0}
&lt;/rewards&gt;
&lt;/document&gt;
""")
		w.println("</body>")
		w.println("</response>")

		w.close()