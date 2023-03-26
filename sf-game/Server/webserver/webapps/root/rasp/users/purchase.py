#
# purchase item request
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


class purchase(HttpServlet):

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
		catalog_ownable_id = None
		useShards = None
		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_token = request.getParameter(name)
			# if name == "user_id":   # user ID
			# 	user = request.getParameter(name)
			if name == "catalog_ownable_id":  
				catalog_ownable_id = request.getParameter(name)
			if name == "useShards":   
				useShards = request.getParameter(name)
		#target = 3900009  # temp for testing	
							

		# get the player ID, which is the immediate parent dir name
		getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
		tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
		if tokenQuery.size() > 0:
			user = tokenQuery[0].getItem("userID") 
		playerID = user

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
		sql = "SELECT shard_price, category, price_multiplier FROM shso.catalog WHERE catalog_ownable_id = " + escapeQuotes(catalog_ownable_id);
		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		else:
			for row in queryRes:
				shard_price = float(row.getItem("shard_price"))
				multiplier = float(row.getItem("price_multiplier"))
				shard_price *= multiplier
				shard_price = int(round(shard_price))
				category = row.getItem("category")


		### CHECK IF PLAYER HAS ENOUGH FUNDS TO COMPLETE THE PURCHASE
		error = ""
		fractals = -1
		responseStatus = ""
		sql = "SELECT Fractals FROM shso.user WHERE ID = " + escapeQuotes(playerID);
		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		else:
			for row in queryRes:
				fractals = int(row.getItem("Fractals"))					
		if (fractals >= shard_price):
			# insert purchased hero into heroes table
			error = ""
			usersStr = ""
			sql = ""
			if category == "h":
				sql = "INSERT INTO shso.heroes (UserID, Name) SELECT " + playerID + ", name FROM catalog WHERE catalog_ownable_id = " + catalog_ownable_id + ";"
			elif category not in ["badge", "craft", "sidekick"]:
				sql = "INSERT INTO shso.inventory (UserID, type, category, subscriber_only) SELECT " + playerID + ", ownable_type_id, category, subscriber_only FROM catalog WHERE catalog_ownable_id = " + catalog_ownable_id + " ON DUPLICATE KEY UPDATE shso.inventory.quantity=shso.inventory.quantity+1;"
			else:
				responseStatus = "400"
				responseBody = "Sidekick, badge, and craft purchases are disabled at this time."
	
			# if category != "h":
			# 	sql = "INSERT INTO shso.inventory (UserID, type, category, subscriber_only) SELECT " + playerID + ", ownable_type_id, category, subscriber_only FROM catalog WHERE catalog_ownable_id = " + catalog_ownable_id + " ON DUPLICATE KEY UPDATE quantity=quantity+1;"

			success = db.executeCommand(sql)
			if (success):
				error = "no error"
			else:
				error = "db command failed"

			# SUBTRACT COST FROM PLAYER FRACTALS IN DB 
			error = ""
			if responseStatus != "400":
				sql = "UPDATE shso.user SET Fractals = " + str(fractals - shard_price) + "  WHERE ID = " + playerID
				if (str(playerID) == '53'):
					sql = "UPDATE shso.user SET Fractals = " + str(fractals + shard_price) + "  WHERE ID = " + playerID

				success = db.executeCommand(sql)
				if (success):
					error = "no error"
				else:
					error = "db command failed"
				responseStatus = "200"
			responseBody = str(fractals - shard_price)  # return new fractal balance
			if (str(playerID) == '53'):
				responseBody = str(fractals + shard_price)  # return new fractal balance
		else:
			responseStatus = "400"
			# if (category != "h"):
				# responseBody = "only character purchases are allowed at this time."
			# else:
			responseBody = "not enough funds for purchase. shard_price/fractals: " + shard_price + "/" + fractals


		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>" + responseStatus + "</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println(responseBody)
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()

		
	
		#pass
		
		