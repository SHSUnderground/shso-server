#
# handle invite friends to mission
# NOTE: smartfox pro is using python 2.2
# 192.168.235.1 -  -  [31/Mar/2021:03:08:16 +0000] "POST /rasp/mm/brawler/friends HTTP/1.1" 404 1388 +9*+-

from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()


class friends(HttpServlet):

	def __init__(self):
		self.htmlHead = "<html><head></head><body style='font-family:Verdana'>"
		self.closeHtml = "</body></html>"
	

	#
	# Handle GET requests
	#
	def doGet(self, request, response):		
		#w = response.getWriter()
		#w.println("doGet() called!")
		#w.close()

		pass
		
	#
	# Handle POST requests (the client app is doing a POST request to anyone.py)
	#
	def doPost(self, request, response):

		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		targetExtension = zone.getExtension("escrow");

		# Get parameter(s) that was passed in - should be mission ID
		#*AS_SESSION_KEY : aSessionToken
		#*mission : m_1007_1_FingFangFoom001
		#*game : BRAWLER
		#*user : 3870526
		#*invitees : 3900010,3900009,3900011

		session_key = None
		mission = None
		game = None
		user = None
		invitees = None
		for name in request.getParameterNames():
			if name == "AS_SESSION_KEY":   # AS_SESSION_KEY
				session_key = request.getParameter(name)	
			if name == "mission":   # mission ID
				mission = request.getParameter(name)
			if name == "game":   # invite type (brawler, card, etc)
				game = request.getParameter(name)
			if name == "user":   # user ID
				user = request.getParameter(name)
			if name == "invitees":   # invitees list
				invitees = request.getParameter(name)

		######  debug logging ###################
		#f = open("/tmp/csp-python-log.txt", "a")
		#f.write("log opened...")		
		#for name in request.getParameterNames():
		#	val = request.getParameter(name)
 		#	if val.isdigit():
		#		f.write("*" + name + " : " + str(val))
		#	else:
		#		f.write("*" + name + " : " + val)
		#f.close()
		####### end debug logging #############################


		# Invoke the handleInternalRequest on the target extension and receive the response
		arr = ArrayList()
		arr.add("get_game_room_invite")  # handler to call in target extension
		arr.add(session_key)
		arr.add(mission)  # should be mission ID
		arr.add(game)
		arr.add(user)
		arr.add(invitees)
		retval = targetExtension.handleInternalRequest(arr);
		arrList = retval.unwrap()
		#trace("Response: " + retval);		


		w = response.getWriter()		

		w.println(arrList.get(0))

		w.close()
	
		#pass
		
		