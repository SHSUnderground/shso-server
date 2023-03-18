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

class shopping_catalog(HttpServlet):

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

		# userID = None
		# session_token = None
		# #userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
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
									
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		shop_file = open('sf-game/Server/webserver/webapps/root/rasp/data/json/shopping_catalog.json', 'r')
		for line in shop_file.readlines():
			w.println(line.replace('"toggled": 0,',"").replace('"toggled": 1,',""))
		shop_file.close()
		w.println("</body>")
		w.println("</response>")

		w.close()

	
		#pass
		