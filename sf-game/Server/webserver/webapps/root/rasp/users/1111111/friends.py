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
sys.path.append('sf-game/Server/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 

class friends(HttpServlet):

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

		# get the player ID, which is the immediate parent dir name
		scriptPath = os.path.basename(os.path.split(os.path.realpath(__file__))[0])  

		# Get all online friends for this player
		error = ""
		usersStr = ""
		#sql = "SELECT user.* FROM shso.user user WHERE user.ID in (SELECT FriendID from friends where PlayerID = " + scriptPath + ")"
		sql =	"""SELECT user.Username, user.ID from user where user.ID in (
				SELECT friends.FriendID
				FROM shso.active_players active_players
		 			CROSS JOIN shso.friends friends
		 			INNER JOIN shso.user usertab ON (friends.PlayerID = usertab.ID)
				WHERE  usertab.ID = friends.PlayerID
		  			AND usertab.ID = """ + scriptPath + """ 
		  			AND friends.FriendID = active_players.ShsoUserID
			);
			"""

		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"

		# Get all offline friends for this player
		error = ""
		usersStr = ""
		#sql = "SELECT user.* FROM shso.user user WHERE user.ID in (SELECT FriendID from friends where PlayerID = " + scriptPath + ")"
		sql =	"""SELECT user.Username, user.ID from user where user.ID in (
	SELECT friends.FriendID
	FROM shso.friends friends
		 INNER JOIN shso.user usertab ON (friends.PlayerID = usertab.ID)
	WHERE  usertab.ID = friends.PlayerID
		  AND usertab.ID = """ + scriptPath + """ 
          AND friends.FriendID NOT IN (SELECT active_players.ShsoUserID as FriendID FROM active_players)
);
			"""

		queryRes2 = db.executeQuery(sql)
		if (queryRes2 == None) or (queryRes2.size() == 0):
			error = "db query failed"


		w = response.getWriter()

		#w.println("value=" + value)
		#for name in request.getParameterNames():
		#	value = request.getParameter(name)
		#	w.println(value)
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

		# do two loops, first for online friends (in active_players table), second for offline friends


		if (queryRes.size() > 0):
			for row in queryRes:
				username = row.getItem("Username")					
				playerID = row.getItem("ID")

    				w.println("    &lt;friend&gt;")
      				w.println("      &lt;id&gt;" + playerID + "&lt;/id&gt;")
      				w.println("      &lt;name&gt;" + username + "&lt;/name&gt;")
      				w.println("      &lt;status&gt;online&lt;/status&gt;")
				w.println("      &lt;location&gt;GameWorld:TBD&lt;/location&gt;")   #location should only be added for online players.
    				w.println("    &lt;/friend&gt;")

		if (queryRes2.size() > 0):
			for row in queryRes2:
				username = row.getItem("Username")
				playerID = row.getItem("ID")

    				w.println("    &lt;friend&gt;")
      				w.println("      &lt;id&gt;" + playerID + "&lt;/id&gt;")
      				w.println("      &lt;name&gt;" + username + "&lt;/name&gt;")
      				w.println("      &lt;status&gt;offline&lt;/status&gt;")
				w.println("      &lt;location&gt;GameWorld:TBD&lt;/location&gt;")   #location should only be added for online players.
    				w.println("    &lt;/friend&gt;")


		w.println("  &lt;/friends&gt;")
		w.println("  &lt;ignores&gt;")
  		w.println("  &lt;/ignores&gt;")
		w.println("&lt;/relationships&gt;")
		w.println("  </body>")
		w.println("</response>")		


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))
		#w.println(usersStr)		
		#w.println(scriptPath)


		
		#w.println(self.closeHtml)
		w.close()
	
		#pass
		
		