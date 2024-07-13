#
# friends add request
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
sys.path.append('sf-game/Server/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 

class friendsadd(HttpServlet):

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
		db = zone.dbManager;

		# Get parameters
		value = ""
		pname = ""
		for name in request.getParameterNames():
			value = request.getParameter(name)
			pname = name
			break # to take the first parameter only which should be name of target
			
		# Get potential friend's ID from name
		error = ""
		friendID = 0
		sql = "SELECT user.ID FROM shso.user user WHERE user.Username = '" + value + "'"
		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"			
		if error == "":			
			for row in queryRes:
				friendID = row.getItem("ID")
				

		# get the player ID, which is the immediate parent dir name
		playerID = os.path.basename(os.path.split(os.path.realpath(__file__))[0])  

		# write debug info to log
		#error = ""
		#usersStr = ""
		#sql = "INSERT INTO shso.log (Info) VALUES('" + str(friendID) + "');"

		#success = db.executeCommand(sql)
		#if (success):
		#	error = "no error"
		#else:
		#	error = "db command failed"

		# add new friend to friends table
		error = ""
		usersStr = ""
		sql = "INSERT INTO shso.friends (PlayerID, FriendID) VALUES(" + str(playerID) + "," + str(friendID) +");"

		success = db.executeCommand(sql)
		if (success):
			error = "no error"
		else:
			error = "db command failed"



		w = response.getWriter()

		#w.println("value=" + value)
		#value = ""
		#for name in request.getParameterNames():
		#	value = request.getParameter(name)
			#w.println(value)
		#w.println("end of parameters")


		#w.println(self.htmlHead)
				
		#w.println("<h2>CSP TEST - SmartFoxServer :: Status</h2><hr>")
		#w.println("<table cellpadding='6' cellspacing='0' border='0'>")
		#w.println("<tr bgcolor='#eeeeee'><th align='left'>Key</th><th align='left'>Value</th></tr>")	
		#w.println("</table><hr>")


		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>&lt;relationships&gt;")		
		w.println("  &lt;friends&gt;")

		w.println("  &lt;/friends&gt;")
		w.println("  &lt;ignores&gt;")
  		w.println("  &lt;/ignores&gt;")
		w.println("&lt;/relationships&gt;")
		w.println("  </body>")
		w.println("</response>")		


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))
		#w.println(usersStr)		
		#w.println(error)


		
		#w.println(self.closeHtml)
		w.close()

	
		#pass
		
		