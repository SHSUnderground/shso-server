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
sys.path.append('sf-game/Server/webserver/webapps/root/pylibcsp')
sys.path.append('sf-game/Server/webserver/webapps/root/rasp/users')
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
		userID = None
		session_token = None
		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			# if (name == "user"):
				# userID = request.getParameter(name)
			# if (name == "user_id"):
				# userID = request.getParameter(name)
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)

		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None


			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")

		#200 = Normal Success, 250 means some effect has to be removed
		#responseStatus = "200"

		er = ""
		expiredPotions = ""
		potionDuration = 60 #In Minutes
		shsoID = None
		sfsID = None
		
		# try:
		for name in request.getParameterNames():
			if name == "shsoid":   # AS_SESSION_KEY
				shsoID = int(request.getParameter(name))

		sql = "select ownable_type_id, SfUserId, IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>"+escapeQuotes(str(potionDuration))+",'T','F') FROM active_players, active_potion_effects WHERE ShsoUserId="+escapeQuotes(str(shsoID))+";"
		queryRes = db.executeQuery(sql)
		if ( queryRes == None) or (queryRes.size() == 0):
			pass
		else:
			#sfsID =  int(queryRes[0].getItem("SfUserID"));
			for row in queryRes:
				sfsID = int(row.getItem("SfUserID"))
				if sfsID < 0 :
					pass
				else:
					ownableID = int(row.getItem("ownable_type_id"))
					expiredCheck = str(row.getItem("IF(Timestampdiff(SQL_TSI_MINUTE,start_timestamp,current_timestamp)>60,'T','F')"))
					if expiredCheck == "T":
						#Potion has expired!!!
						expiredPotions = expiredPotions +str(ownableID)+","+str(sfsID) + "|"
						sql = "DELETE FROM active_potion_effects WHERE userid=" + escapeQuotes(str(userID))
						db.executeCommand(sql)
		# except Exception as e:
		# 	pass
			# er = str(e)
			# _server.trace(er)

		

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
		# try:
		if len(expiredPotions) > 0:
			
			
			w.println(expiredPotions)
			

			#Remove that potion from the DB
			#sql = "DELETE FROM active_potion_effects WHERE shsoid = " + str(shsoID) + " AND ownable_type_id = " str(potion[1])
			#success = db.executeCommand(sql)"""
		# except Exception as e:
			# w.println(str(e))

		#w.println("  &lt;/persist&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()