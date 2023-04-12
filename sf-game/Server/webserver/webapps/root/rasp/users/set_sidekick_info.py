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
sys.path.append('sf-game/SFS_PRO_1.6.6/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 


def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2


class set_sidekick_info(HttpServlet):

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
		db = zone.dbManager
		jdbconnection = db.getConnection()

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
			if (name == "sidekick_id"):
				sidekick_id = request.getParameter(name)

		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token= ?"
			prepare = jdbconnection.prepareStatement(getUserID)
			prepare.setString(1,session_token)
			tokenQuery = prepare.executeQuery()
			# userID = None
			
			
			if tokenQuery.next():
				userID = tokenQuery.getInt("userID")
				playerID = userID
 
			tokenQuery.close()
			prepare.close()

		# Update/Insert db record for this player
		error = ""
		sql = "INSERT INTO shso.equips (UserID, sidekick_id) values (?,?) ON DUPLICATE KEY UPDATE sidekick_id = ?"
		prePareR.setInt(1,userID)
		prePareR.setInt(2,sidekick_id)
		prePareR.setInt(3,sidekick_id)

		success = prePareR.executeUpdate()
		if (success == 0):
			error = "db query failed"
		
		prePareR.close()							
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/xml; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("</body>")
		w.println("</response>")

		w.close()

		jdbconnection.close()
		#pass
		