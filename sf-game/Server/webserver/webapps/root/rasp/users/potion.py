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

class potion(HttpServlet):

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


		# Get parameters
		session_token = None
		user = None
		ownable_type_id = None
		useShards = None
		potion_id = None
		request_id = None
		hero_name = None
		potion_name = None

		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_token = request.getParameter(name)
			if name == "user_id":   # user ID
				user = request.getParameter(name)
			if name == "potion_id":
				ownable_type_id = request.getParameter(name)
			if name == "hero_name":
				hero_name = request.getParameter(name)
			if name == "request_id":
				request_id = request.getParameter(name)
		#target = 3900009  # temp for testing	
							
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")

		# get the player ID, which is the immediate parent dir name
		playerID = userID
		potion_id = str(ownable_type_id)
		# write debug info to log
		#sql = "INSERT INTO shso.log (Info) VALUES('target:" + str(target) + "');"
		#success = db.executeCommand(sql)

		#sql = "INSERT INTO shso.log (Info) VALUES('user:" + user + "');"
		#success = db.executeCommand(sql)

		
		#if (success):
		#	error = "no error"
		#else:
		#	error = "db command failed"

		# LOOK UP PRICE OF ITEM IN CATALOG
		error = ""
		shard_price = 999999
		category = " "
		sql = "SELECT name FROM shso.catalog WHERE ownable_type_id = " + escapeQuotes(str(ownable_type_id));
		queryRes = db.executeQuery(sql)
		responseBody = ""
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		else:
			for row in queryRes:
				potion_name = row.getItem("name")


		### CHECK IF PLAYER HAS ENOUGH FUNDS TO COMPLETE THE PURCHASE
		error = ""
		fractals = -1
		quantity = 0
		sql = "SELECT quantity FROM shso.inventory WHERE UserID = " + escapeQuotes(str(playerID)) + " AND type = " + escapeQuotes(str(ownable_type_id))
		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		else:
			for row in queryRes:
				quantity = int(row.getItem("quantity"))
		if (quantity > 0):
			# insert purchased hero into heroes table
			error = ""
			usersStr = ""

			sql = "update shso.inventory set quantity=quantity - 1 WHERE UserID = " + playerID + " AND type = " + potion_id
			if (str(playerID) == '53'):
				sql = "update shso.inventory set quantity=quantity + 1 WHERE UserID = " + playerID + " AND type = " + potion_id
			success = db.executeCommand(sql)
			if (success):
				error = "no error"
			else:
				error = "db command failed"

			responseStatus = "200"
			responseBody += '\n<player_id>' + str(user) + '</player_id>'
			responseBody += '\n<_cmd>notification</_cmd>'
			responseBody += '\n<message_type>consume_potion_response</message_type>'
			responseBody += '\n<request_id>' + str(request_id) + '</request_id>'
			# responseBody += '\n<potion_name>' + str(potion_name) + '</potion_name>'
			if potion_name in [
				'#POTION_NAME_1000XPSHIELD', '#POTION_NAME_298424', 
				'#POTION_NAME_5000XPSHIELD', '#POTION_NAME_298425'
				]:
				XPsql = ''
				if potion_name in ['#POTION_NAME_1000XPSHIELD', '#POTION_NAME_298424']:
					xp = '1000'
					XPsql = "UPDATE shso.heroes SET Xp = Xp + " + xp + " WHERE UserID = " + str(playerID) + " AND name = '" + hero_name + "'"
				elif potion_name in ['#POTION_NAME_5000XPSHIELD', '#POTION_NAME_298425']:
					xp = '5000'
					XPsql = "UPDATE shso.heroes SET Xp = Xp + " + xp + " WHERE UserID = " + str(playerID) + " AND name = '" + hero_name + "'"
				success = db.executeCommand(XPsql)
				if (success):
					error = "no error"
				else:
					error = "db command failed"
				responseBody += '\n<xp_added>' + xp + '</xp_added>'
			responseBody += '\n<hero_name>' + hero_name + '</hero_name>'
			responseBody += '\n<ownable_type_id>' + potion_id + '</ownable_type_id>'
			if (str(playerID) == '53'):
				responseBody += '\n<potions_remaining>' + str(quantity+1) + '</potions_remaining>'	
			else:
				responseBody += '\n<potions_remaining>' + str(quantity - 1) + '</potions_remaining>'
				
			responseBody += '\n<success>true</success>'
			responseBody = cgi.escape(responseBody)

		else:
			responseStatus = "400"
			# if (category != "h"):
				# responseBody = "only character purchases are allowed at this time."
			# else:
			responseBody = "Not enough quantity: " + str(quantity) + "\nSQL: " + sql

		if error != "no error":
			responseStatus = "400"
			responseBody = "Error:" + error
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>" + responseStatus + "</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println(f"stop_showing_effect%{user}%{ownable_type_id}%null")
		# w.println("  &lt;potion&gt;")
		w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		


		w.close()
	
		#pass
		
		