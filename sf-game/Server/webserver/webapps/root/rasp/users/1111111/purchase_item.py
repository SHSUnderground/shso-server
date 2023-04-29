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

class purchase_item(HttpServlet):

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
		db = zone.dbManager
		jdbconnection = db.getConnection()


		# write debug info to log
		#sql = "INSERT INTO shso.log (Info) VALUES('entering friendsremove.py');"
		#success = db.executeCommand(sql)
		

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");


		# Get parameters
		session_key = None
		user = None
		catalog_ownable_id = None
		useShards = None
		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_key = request.getParameter(name)
			if name == "user":   # user ID
				user = request.getParameter(name)
			if name == "catalog_ownable_id":  
				catalog_ownable_id = request.getParameter(name)
			if name == "useShards":   
				useShards = request.getParameter(name)
		#target = 3900009  # temp for testing	
							

		# get the player ID, which is the immediate parent dir name
		playerID = os.path.basename(os.path.split(os.path.realpath(__file__))[0])  

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
		sql = "SELECT shard_price, category, price_multiplier FROM shso.catalog WHERE catalog_ownable_id = ?"
		prepare = jdbconnection.prepareStatement(sql)
		prepare.setInt(1,catalog_ownable_id)

		queryRes = prepare.executeQuery()
		if (queryRes.next()):
			shard_price = float(queryRes.getInt("shard_price"))
			multiplier = queryRes.getFloat("price_multiplier")
			shard_price *= multiplier
			shard_price = int(round(shard_price))
			category = queryRes.getString("category")
		else:
			error = "db query failed"
		
		queryRes.close()
		prepare.close()


		### CHECK IF PLAYER HAS ENOUGH FUNDS TO COMPLETE THE PURCHASE
		error = ""
		fractals = -1
		sql = "SELECT Fractals FROM shso.user WHERE Paid = 1 AND ID = " + playerID
		queryRes = db.executeQuery(sql)


		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"
		else:
			for row in queryRes:
				fractals = int(row.getItem("Fractals"))					
		if (fractals >= shard_price) and (category == "h"):
			# insert purchased hero into heroes table
			error = ""
			usersStr = ""
			sql = "INSERT INTO shso.heroes (UserID, Name) SELECT ?, name FROM catalog WHERE catalog_ownable_id = ?"
			prePareR = jdbconnection.prepareStatement(sql)
			prePareR.setInt(1,playerID)
			prePareR.setInt(2,catalog_ownable_id)

			success = prePareR.executeUpdate()
			if (success != 0):
				error = "no error"
			else:
				error = "db command failed"
			prePareR.close()
			# SUBTRACT COST FROM PLAYER FRACTALS IN DB 
			error = ""
			sql = "UPDATE shso.user SET Fractals = ? WHERE ID = ?"
			prePareR = jdbconnection.prepareStatement(sql)
			prePareR.setInt(1,fractals - shard_price)
			prePareR.setInt(2,playerID)

			success = prePareR.executeUpdate()
			if (success != 0):
				error = "no error"
			else:
				error = "db command failed"
			
			prePareR.close()


			responseStatus = "200"
			responseBody = str(fractals - shard_price)  # return new fractal balance
		else:
			responseStatus = "400"
			if (category != "h"):
				responseBody = "only character purchases are allowed at this time."
			else:
				responseBody = "not enough funds for purchase. shard_price/fractals: " + shard_price + "/" + fractals


		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>" + responseStatus + "</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println(responseBody)
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()

		jdbconnection.close()
	
		#pass
		
		