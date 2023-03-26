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
sys.path.append('sf-game/SFS_PRO_1.6.6/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 

def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2

class counters(HttpServlet):

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


		# countersSQL = "SELECT * from shso.counters;"
		# countersRes = db.executeQuery(countersSQL)
		# responseBody = ''
		# if countersRes.size > 0:
		# 	responseBody += "\n&lt;counters&gt;"
		# 	for row in countersRes:
		# 		responseBody += "\n&lt;counter&gt;"
		# 		responseBody += "\n&lt;hero_name&gt;"
		# 		responseBody += row.getItem("name")
		# 		responseBody += "\n&lt;/hero_name&gt;"
		# 		responseBody += "\n&lt;counter_type&gt;"
		# 		responseBody += row.getItem("counter_type")
		# 		responseBody += "\n&lt;/counter_type&gt;"
		# 		responseBody += "\n&lt;value&gt;"
		# 		responseBody += row.getItem("value")
		# 		responseBody += "\n&lt;/value&gt;"
		# 		responseBody += "\n&lt;/counter&gt;"
		# 	responseBody += "\n&lt;/counters&gt;"


		w = response.getWriter()

		w.println("<response>")
		# w.println("  <status>" + responseStatus + "</status>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("	<Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		# w.println(responseBody)
		counters_file = open('sf-game/Server/webserver/webapps/root/rasp/users/counters.xml', 'r')
		for line in counters_file.readlines():
			w.println(line)
		counters_file.close()
		w.println(  "</body>")
		w.println("</response>")
		
		w.close()