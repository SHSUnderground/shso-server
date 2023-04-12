#
# friends remove request
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

class friendsremove(HttpServlet):

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
		target = None
		rel = None
		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_key = request.getParameter(name)
			if name == "user":   # user ID
				user = request.getParameter(name)
			if name == "target":  
				target = request.getParameter(name)
			if name == "rel":   
				rel = request.getParameter(name)
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

		# delete friend from friends table
		error = ""
		usersStr = ""
		sql = "DELETE FROM shso.friends WHERE PlayerID = ? AND  FriendID = ?"
		prepare = jdbconnection.prepareStatement(sql)
		prepare.setInt(1,playerID)
		prepare.setInt(2,target)

		success = prepare.executeUpdate()
		if (success != 0):
			error = "no error"
		else:
			error = "db command failed"

		prepare.close()
		jdbconnection.close()

		w = response.getWriter()


		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>text/html; charset=utf-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>")
		w.println("  </body>")
		w.println("</response>")
		
		w.close()

		
	
		#pass
		
		