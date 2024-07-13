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

class decks(HttpServlet):

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

		cardInventorySQL = "SELECT * FROM shso.inventory WHERE category = 'card' AND shso.inventory.UserID = " + escapeQuotes(userID)


		queryRes2 = db.executeQuery(cardInventorySQL)
		if (queryRes2 == None) or (queryRes2.size() == 0):
			error = "db query failed"

		w = response.getWriter()

		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("  &lt;Decks&gt;")
		'''
		DataWarehouse data = dataWarehouse.GetData("Decks/Deck", i);
		DeckProperties deckProperties = new DeckProperties();
		deckProperties.DeckName = data.GetString("Name");
		deckProperties.DeckRecipe = data.GetString("Cards");
		deckProperties.DeckId = data.GetInt("ID");
		deckProperties.ReadOnly = data.GetBool("Readonly");
		deckProperties.Legal = data.GetBool("Legal");
		deckProperties.HeroName = "spider_man";
		'''
		w.println("    &lt;Deck&gt;")
		w.println("      &lt;Name&gt;" + "Starter Deck" + "&lt;/Name&gt;")
		w.println("      &lt;Cards&gt;" + "ST005:1;ST038:1;ST047:2;ST048:4;ST105:1;ST142:4;ST148:2;ST150:4;ST165:4;ST172:4;ST183:4;ST187:4;ST194:1;ST272:1;ST353:3" + "&lt;/Cards&gt;")
		w.println("      &lt;ID&gt;" + "0" + "&lt;/ID&gt;")
		w.println("      &lt;Readonly&gt;" + "true" + "&lt;/Readonly&gt;")
		w.println("      &lt;Legal&gt;" + "true" + "&lt;/Legal&gt;")


		w.println("    &lt;/Deck	&gt;")
		# for row in queryRes2:
		# 	card_id = row.getItem("type")
		# 	card_quantity = row.getItem("quantity")
		# 	w.println("    &lt;card&gt;")
		# 	w.println("      &lt;type&gt;" + card_id + "&lt;/type&gt;")
		# 	w.println("      &lt;count&gt;" + card_quantity + "&lt;/count&gt;")
		# 	w.println("    &lt;/card&gt;")
		# w.println("  &lt;player_id&gt;1&lt;/player_id&gt;")
		# w.println("  &lt;potion&gt;")
		# w.println(responseBody)
		# w.println("  &lt;/potion&gt;")
		w.println("  &lt;/Decks&gt;")
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()
