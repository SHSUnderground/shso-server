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


class set_pref(HttpServlet):

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
		userID = None
		pref_id = None
		value = None
		session_token = None
		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)
			if (name == "pref_id"):
				pref_id = request.getParameter(name)
			if (name == "value"):
				value = request.getParameter(name)
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")


		sql = "INSERT INTO user_prefs VALUES(" + escapeQuotes(userID) + ", " + escapeQuotes(pref_id) + ", '" + escapeQuotes(value) + "') ON DUPLICATE KEY UPDATE pref_id=" + escapeQuotes(pref_id) + ", value='" + escapeQuotes(value) + "';"
		success = db.executeCommand(sql)
		w = response.getWriter()

		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")\
		if success:
			w.println("  <status>200</status>")
		else:
			w.println("  <status>500</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("  &lt;bank&gt;")
		w.println("  &lt;player_id&gt;" + escapeQuotes(userID) + "&lt;/player_id&gt;")
		# w.println("  &lt;potion&gt;")
		# w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()