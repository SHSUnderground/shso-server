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

class inventory(HttpServlet):

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
		# fileList = ["POST Request Recieved"]
		# outfile = open("/sf-game/Server/webserver/webapps/root/rasp/inventoryresult.txt", "w")
		# outfile.writelines(fileList)
		# outfile.close()
		# userID = None
		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

		# Get a reference to database manager
		db = zone.dbManager;

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
 

		# Get db record for this player
		error = ""
		usersStr = ""
		sql = "SELECT user.* FROM shso.user user WHERE user.ID = " + escapeQuotes(userID)

		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"

		# Get all owned characters for this player
		error = ""
		usersStr = ""
		inventorysql = "SELECT shso.inventory.* FROM shso.inventory, shso.user WHERE category != 'card' AND shso.inventory.UserID = shso.user.ID AND shso.user.ID = " + escapeQuotes(userID)


		queryRes2 = db.executeQuery(inventorysql)
		if (queryRes2 == None) or (queryRes2.size() == 0):
			error = "db query failed"


		# if (queryRes2.size() > 0):
		# 	for row in queryRes2:
		# 		xp = int(row.getItem("Xp"))
		# 		XPlist.append(xp+0.5)
		# 		XPlist.sort()
		# 		heroName = row.getItem("Name")
		# 		# #testvar = heroName + ''
		# 		# testvar2 = heroScores[0]['angel']
		# 		# _server.trace("Hero name: ")
		# 		if heroName in heroNames:
		# 			squadlevel += XPlist.index(xp+0.5) + heroScores[str(heroName)]	
		# 		else:
		# 			squadlevel += XPlist.index(xp+0.5) #+ heroScores[0][str(heroName)]
		# 		# squadlevel += heroScores[0][str(heroName)]
		# 		XPlist.pop(XPlist.index(xp+0.5))

		w = response.getWriter()


		w.println("\n<response>")
		w.println("\n  <status>200</status>")
		w.println("\n  <headers>")
		w.println("\n	<Content-Type>application/xml; charset=UTF-8</Content-Type>")
		w.println("\n  </headers>")
		w.println("\n  <body>&lt;masterinventory&gt;")
		w.println("\n  &lt;inventory&gt;")
		temp_inven = []
		inventory_file = open('sf-game/Server/webserver/webapps/root/rasp/users/inventory.xml', 'r')
		for line in inventory_file.readlines():
			w.println(line)
			temp_inven.append(line)

		inventory_file.close()
		
		# loop through inventory in db

		if (queryRes2.size() > 0):
			for row in queryRes2:
				itemType = row.getItem("type")
				itemQuantity = row.getItem("quantity")
				itemCategory = row.getItem("category")
				itemSubOnly = row.getItem("subscriber_only")
				item = "&lt;type&gt;" + str(itemType) + "&lt;/type&gt;\n"
				if item not in temp_inven:

					w.println("\n	    &lt;item&gt;")
					w.println("\n	      &lt;type&gt;" + str(itemType) + "&lt;/type&gt;")
					w.println("\n	      &lt;quantity&gt;" + str(itemQuantity) + "&lt;/quantity&gt;")
					w.println("\n	      &lt;category&gt;" + str(itemCategory) + "&lt;/category&gt;")
					if itemSubOnly == 1:
						w.println("\n	      &lt;subscriber_only&gt;" + str(itemSubOnly) + "&lt;/subscriber_only&gt;")
					w.println("\n	    &lt;/item&gt;")

		w.println("\n  &lt;/inventory&gt;")
		w.println("\n  &lt;gear&gt;")
		w.println("\n  &lt;/gear&gt;")
		w.println("\n  &lt;/masterinventory&gt;")
		w.println("\n</body>")
		w.println("\n</response>")
		# outfile = open("/sf-game/Server/webserver/webapps/root/rasp/inventoryresult.txt", "w")
		# outfile.writelines(fileList)
		# outfile.close()


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))
		#w.println(usersStr)		
		#w.println(scriptPath)


		
		#w.println(self.closeHtml)
		w.close()

	
		#pass
		