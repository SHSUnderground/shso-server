#
# Call a SmartFox script with sole purpose of triggering a specific response to Unity SHSO/RTCClient code.
#	Can be used for: 1) moving more logic out of Smartfox scripts into web Python scripts.  2) testing RTCClient response code without having all permanent logic in place. 
#

from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
import java.util.ArrayList as ArrayList
import it.gotoandplay.smartfoxserver.extensions.ExtensionHelper
ex = it.gotoandplay.smartfoxserver.extensions.ExtensionHelper.instance()



class rtcresponse(HttpServlet):

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
		if (pylibcsp.ipcheck(False)):   # don't process request if not a valid client
			return

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
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		targetExtension = zone.getExtension("escrow");

		# Get parameter(s) that was passed in - should be mission ID
		#params = ""
		value = ""
		ndx = 1
		for name in request.getParameterNames():
			if ndx == 2:
				value = request.getParameter(name)
			ndx = ndx + 1
			#params = params + "<br>" + name +" = " + value


		# Invoke the handleInternalRequest on the target extension and receive the response
		arr = ArrayList()
		arr.add("do_rtc_response")
		arr.add(value)  # should be mission ID
		retval = targetExtension.handleInternalRequest(arr);
		arrList = retval.unwrap()
		#trace("Response: " + retval);		


		w = response.getWriter()


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))

		
		#w.println(self.closeHtml)
		w.close()
	
		#pass
		
		