#
# potion persist request
# 
#

import sys
import os
import cgi
import time
import datetime
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


class potion_persist(HttpServlet):

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
		jdbconnection = db.getConnection()

		# write debug info to log
		#sql = "INSERT INTO shso.log (Info) VALUES('entering friendsremove.py');"
		#success = db.executeCommand(sql)
		

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");


		# # Get parameters
		# session_key = None
		# user = None
		# ownable_type_id = None
		# useShards = None
		# potion_id = None
		# request_id = None
		# hero_name = None
		# potion_name = None

		# for name in request.getParameterNames():
		# 	if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
		# 		session_key = request.getParameter(name)
		# 	if name == "user_id":   # user ID
		# 		user = request.getParameter(name)
		# 	if name == "potion_id":
		# 		ownable_type_id = request.getParameter(name)
		# 	if name == "hero_name":
		# 		hero_name = request.getParameter(name)
		# 	if name == "request_id":
		# 		request_id = request.getParameter(name)
		# #target = 3900009  # temp for testing	

		#200 = Normal Success, 250 means some effect has to be removed
		#responseStatus = "200"

		er = ""
		expiredPotions = ""
		potionDuration = 60 #In Minutes
		shsoID = None
		sfsID = None
		
		try:
			for name in request.getParameterNames():
				if name == "shsoid":   # AS_SESSION_KEY
					shsoID = int(request.getParameter(name))

			sql = "select ownable_type_id, SfUserId, IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)> ?,'T','F') FROM active_players, active_potion_effects WHERE ShsoUserId=?"
			prepare = jdbconnection.prepareStatement(sql)
			prepare.setInt(1,potionDuration)
			prepare.setInt(2,shsoID)
			queryRes = prepare.executeQuery()
			if (queryRes.next()):
				queryRes.beforeFirst()
				while queryRes.next():
					sfsID = queryRes.getInt("SfUserID")
					if sfsID < 0 :
						pass
					else:
						ownableID = queryRes.getInt("ownable_type_id")
						expiredCheck = queryRes.getString("IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>60,'T','F')")
						if expiredCheck == "T":
							#Potion has expired!!!
							expiredPotions = expiredPotions +str(ownableID)+","+str(sfsID) + "|"
							sql = "DELETE FROM active_potion_effects WHERE userid=" + escapeQuotes(str(playerID))
							db.executeCommand(sql)
			else:
				pass

			queryRes.close()				
			prepare.close()
			jdbconnection.close()
		except Exception as e:
			er = str(e)
			_server.trace(er)

		

		w = response.getWriter()
		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")

		
				

		#w.println("  &lt;persist&gt;")
		# w.println("  &lt;player_id&gt;1&lt;/player_id&gt;")
		# w.println("  &lt;potion&gt;")
		# w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		try:
			if len(expiredPotions) > 0:
				
				
				w.println(expiredPotions)
				

				#Remove that potion from the DB
				#sql = "DELETE FROM active_potion_effects WHERE shsoid = " + str(shsoID) + " AND ownable_type_id = " str(potion[1])
				#success = db.executeCommand(sql)"""
		except Exception as e:
			w.println(str(e))

		#w.println("  &lt;/persist&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()