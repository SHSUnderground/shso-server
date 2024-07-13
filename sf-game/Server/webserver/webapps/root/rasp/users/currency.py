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

class currency(HttpServlet):

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
		# ownable_type_id = None
		# useShards = None
		# potion_id = None
		# request_id = None
		# hero_name = None
		# potion_name = None

		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_token = request.getParameter(name)
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

		sql = "SELECT user.Fractals FROM shso.user user WHERE user.ID = " + escapeQuotes(userID)
		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		if (queryRes and queryRes.size() > 0):
			for row in queryRes:
				fractals = row.getItem("Fractals")



		w = response.getWriter()
		
		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		# w.println("  <status>400</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("  &lt;currency&gt;")
		# w.println()
		w.println("    &lt;tokens&gt;2&lt;/tokens&gt;")
		w.println("	&lt;coins&gt;2&lt;/coins&gt;")
		w.println("	&lt;tickets&gt;2&lt;/tickets&gt;")
		w.println("	&lt;shards&gt;" + fractals + "&lt;/shards&gt;")
		# w.println("  &lt;player_id&gt;1&lt;/player_id&gt;")
		# w.println("  &lt;potion&gt;")
		# w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		w.println("  &lt;/currency&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()