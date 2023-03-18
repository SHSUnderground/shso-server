from javax.servlet.http import HttpServlet
from it.gotoandplay.smartfoxserver.webserver import WebHelper
from it.gotoandplay.smartfoxserver import SmartFoxServer
from java.lang import Thread, Boolean
from java.io import IOException

import installer

class index(HttpServlet):

	def __init__(self):
		self.sfsVersion = SmartFoxServer.getInstance().getVersion()
		
	def doGet(self, request, response):	
		action = request.getParameter("action")
		
		request.setAttribute("version", self.sfsVersion)	
		
		
		#--- No Actions specied ------------------------------------------------------------
		if action == None:
			request.setAttribute("examplesInstalled", installer.isExamplesReady())			
			dispatcher = request.getRequestDispatcher("_index.jsp")
			dispatcher.forward(request, response)
			
		#--- Install -----------------------------------------------------------------------
		elif action == 'install':
			success = False
			error = None
			
			try:
				installer.performInstallation()
				success = True
				
			except IOException, err:
				error = err.toString()

			request.setAttribute("installationOk", success)
			request.setAttribute("examplesInstalled", installer.isExamplesReady())
			request.setAttribute("error", error)
			
			dispatcher = request.getRequestDispatcher("_index.jsp")
			dispatcher.forward(request, response)
		
		
	def doPost(self, request, response):	
		pass
			
		