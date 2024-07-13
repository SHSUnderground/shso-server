#
# Simple servlet example
# Display basic SmartFoxServer status infos
#

from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()



class solo(HttpServlet):

	def __init__(self):
		self.htmlHead = "<html><head></head><body style='font-family:Verdana'>"
		self.closeHtml = "</body></html>"
	

	#
	# Handle GET requests
	#
	def doGet(self, request, response):	
		pass
		
	#
	# Handle POST requests (the client app is doing a POST request to anyone.py)
	#
	def doPost(self, request, response):

		################### test code for XML parsing, remove when done testing!!! ###############################
		#zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("maitred");

		# Invoke the handleInternalRequest on the target extension and receive the response
		#arr = ArrayList()
		#arr.add("a test")
		#arr.add(777)
		#retval = targetExtension.handleInternalRequest(arr);
		#arrList = retval.unwrap()	
		############################################################################################################

		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		targetExtension = zone.getExtension("escrow");

		# Get parameter(s) that was passed in - should be mission ID
		#params = ""
		value = None
		user = None
		for name in request.getParameterNames():
			if name == "mission":   # mission ID
				value = request.getParameter(name)
			if name == "user":   # user ID
				user = request.getParameter(name)



		# Invoke the handleInternalRequest on the target extension and receive the response
		arr = ArrayList()
		arr.add("get_game_room_solo")
		arr.add(value)  # should be mission ID
		arr.add(user) # SHSO user ID
		retval = targetExtension.handleInternalRequest(arr);
		arrList = retval.unwrap()
		#trace("Response: " + retval);		


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


		#w.println("<response>")
		#w.println("  <status>200</status>")
		#w.println("  <headers>")
		#w.println("    <Content-Type>text/html; charset=utf-8</Content-Type>")
		#w.println("  </headers>")
		#w.println("  <body>&lt;invitation&gt;")
		#w.println("	  &lt;invitation_id&gt;1103&lt;/invitation_id&gt;")
		#w.println("	&lt;/invitation&gt;")
		#w.println("  </body>")
		#w.println("</response>")		


		w.println(arrList.get(0))
		#w.println(arrList.get(1))

		
		#w.println(self.closeHtml)
		w.close()
	
		#pass
		
		