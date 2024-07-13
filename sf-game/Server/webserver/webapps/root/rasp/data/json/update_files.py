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
import base64

importantFiles = {
	'AssetBundles/Data/general.unity3d': "",
	# 'AssetBundles/SocialSpace/Asgard.unity3d': "",
	# 'AssetBundles/SocialSpace/Asgard_scenario.unity3d': "",
	# 'AssetBundles/SocialSpace/baxter.unity3d': "",
	# 'AssetBundles/SocialSpace/baxter_scenario.unity3d': "",
	# 'AssetBundles/SocialSpace/daily_bugle2.unity3d': "",
	# 'AssetBundles/SocialSpace/daily_bugle2_scenario.unity3d': "",
	# 'AssetBundles/SocialSpace/gameworld_activity_objects.unity3d': "",
	# 'AssetBundles/SocialSpace/gameworld_common_objects.unity3d': "",
	# 'AssetBundles/SocialSpace/Villainville.unity3d': "",
	# 'AssetBundles/SocialSpace/Villainville_scenario.unity3d': "",
}

testers = []

def checkHashes():
	for file in importantFiles.keys():
		if importantFiles[file] == "":
			# Compute md5 hash using OS shell commands
			hash = os.popen('md5sum /srv/ftp/game/Win64/bin/shso_Data/' + file).read().split(' ')[0]
			importantFiles[file] = hash

class update_files(HttpServlet):

	def __init__(self):
		self.htmlHead = "<html><head></head><body style='font-family:Verdana'>"
		self.closeHtml = "</body></html>"
	

	#
	# Handle GET requests  (this gets called from browser)
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

		hashCheckComplete = None
		hashesAndFiles = None
		filesToUpdate = [
			importantFiles.keys()[0],
		]
		fileHashes = {}
		session_token = None
		username = None
		for name in request.getParameterNames():
			if (name == "session_token"):
				session_token = request.getParameter(name)
			if (name == "hashCheckComplete"):
				hashCheckComplete = request.getParameter(name)
			if (name == "fileHash"):
				fileHash = request.getParameter(name)
			if (name == "filePath"):
				filePath = request.getParameter(name)
				# for file in hashesAndFiles:
				# 	fileName, fileHash = file.split(",")
				# 	# importantFiles[fileName] = fileHash
		

 		# compare recieved hashes with hash for each file in importantFiles dictionary
		# if hashCheckComplete is not None and hashCheckComplete == '1':
		# 	for file in importantFiles:
		# 		if (file not in fileHashes or importantFiles[file] != fileHashes[file]):
		# 			filesToUpdate.append(file)
  
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + session_token + "'"
			tokenQuery = db.executeQuery(getUserID)
			
			
			if tokenQuery.size() > 0:
				username = tokenQuery[0].getItem("username")
									
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.print("  <body>")
		# w.println("  <>")
		if (hashCheckComplete is not None and hashCheckComplete == '0'):
			# w.print('HASH CHECK COMPLETE: ' + hashCheckComplete)
			w.print(",".join(importantFiles.keys()))
		if ((hashCheckComplete is None or hashCheckComplete == '1') and username.lower() not in testers):
			checkHashes()
			if fileHash.lower() != importantFiles[filePath].lower():
				# w.println(str(importantFiles[filePath]))
				# w.println(fileHash)
				file = open('/srv/ftp/game/Win64/bin/shso_Data/' + filePath, 'rb')
				file_bytes = file.read()
				file.close()
				file_bytes_string = base64.encodestring(file_bytes).replace("\n", "")
				w.print(file_bytes_string + "|" + filePath)
			else:
				w.print(filePath)
			# files = [
			# 	'AssetBundles/Data/general.unity3d',
			# 	# 'AssetBundles/SocialSpace/Asgard.unity3d',
			# 	# 'AssetBundles/SocialSpace/Asgard_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/baxter.unity3d',
			# 	# 'AssetBundles/SocialSpace/baxter_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/daily_bugle2.unity3d',
			# 	# 'AssetBundles/SocialSpace/daily_bugle2_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/gameworld_activity_objects.unity3d',
			# 	# 'AssetBundles/SocialSpace/gameworld_common_objects.unity3d',
			# 	# 'AssetBundles/SocialSpace/Villainville.unity3d',
			# 	# 'AssetBundles/SocialSpace/Villainville_scenario.unity3d',
			# ]
			# filePaths = ""
			# file_bytes_string = ""
			# for filePath in filesToUpdate:
			# 	file = open('/srv/ftp/game/Win64/bin/shso_Data/' + filePath, 'rb')
			# 	file_bytes = file.read()
			# 	file.close()
			# 	file_bytes_string += base64.encodestring(file_bytes).replace("\n", "") + ","
			# 	filePaths += filePath + ","
			# Convert encoded bytes to a string
			# encoded_string = encoded_bytes.decode("utf-8")

			# Now you can send `encoded_string` as a response
			# w.print(file_bytes_string[:-1] + "|" + filePaths[:-1])
		# else:
		# 	# Send list of files as a comma delimited string
		# 	w.print(','.join(filesToUpdate))

		# w.println('{"daily_mission": {"ownable_type_id": 1294}}')
		w.print("</body>")
		w.println("</response>")

		w.close()

		
	#
	# Handle POST requests (the client app is doing a POST request to anyone.py)
	#
	def doGet(self, request, response):
		if (pylibcsp.ipcheck(False)):   # don't process request if not a valid client
			return
		
		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

		# Get a reference to database manager
		db = zone.dbManager;

		hashCheckComplete = None
		hashesAndFiles = None
		filesToUpdate = [
			importantFiles.keys()[0],
		]
		fileHashes = {}
		session_token = None
		username = None
		for name in request.getParameterNames():
			if (name == "session_token"):
				session_token = request.getParameter(name)
			if (name == "hashCheckComplete"):
				hashCheckComplete = request.getParameter(name)
			if (name == "fileHashes"):
				hashesAndFiles = request.getParameter(name).split("|")
				for file in hashesAndFiles:
					fileName, fileHash = file.split(",")
					importantFiles[fileName] = fileHash
		checkHashes()

 		# compare recieved hashes with hash for each file in importantFiles dictionary
		if hashCheckComplete is not None and hashCheckComplete == 1:
			for file in importantFiles:
				if (file not in fileHashes or importantFiles[file] != fileHashes[file]):
					filesToUpdate.append(file)
  
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + session_token + "'"
			tokenQuery = db.executeQuery(getUserID)
			
			
			if tokenQuery.size() > 0:
				username = tokenQuery[0].getItem("username")
									
		w = response.getWriter()

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.print("  <body>")
		# w.println("  <>")
		if (hashCheckComplete is not None and hashCheckComplete == 0):
			w.print(",".join(importantFiles.keys()))
			# w.print(str(importantFiles.keys())))
		if (hashCheckComplete is None or hashCheckComplete == 1 and username.lower() not in testers):
			# files = [
			# 	'AssetBundles/Data/general.unity3d',
			# 	# 'AssetBundles/SocialSpace/Asgard.unity3d',
			# 	# 'AssetBundles/SocialSpace/Asgard_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/baxter.unity3d',
			# 	# 'AssetBundles/SocialSpace/baxter_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/daily_bugle2.unity3d',
			# 	# 'AssetBundles/SocialSpace/daily_bugle2_scenario.unity3d',
			# 	# 'AssetBundles/SocialSpace/gameworld_activity_objects.unity3d',
			# 	# 'AssetBundles/SocialSpace/gameworld_common_objects.unity3d',
			# 	# 'AssetBundles/SocialSpace/Villainville.unity3d',
			# 	# 'AssetBundles/SocialSpace/Villainville_scenario.unity3d',
			# ]
			filePaths = ""
			file_bytes_string = ""
			for filePath in filesToUpdate:
				file = open('/srv/ftp/game/Win64/bin/shso_Data/' + filePath, 'rb')
				file_bytes = file.read()
				file.close()
				file_bytes_string += base64.encodestring(file_bytes).replace("\n", "") + ","
				filePaths += filePath + ","
			# Convert encoded bytes to a string
			# encoded_string = encoded_bytes.decode("utf-8")

			# Now you can send `encoded_string` as a response
			w.print(file_bytes_string[:-1] + "|" + filePaths[:-1])
		else:
			# Send list of files as a comma delimited string
			w.print(','.join(filesToUpdate))

		# w.println('{"daily_mission": {"ownable_type_id": 1294}}')
		w.println("</body>")
		w.println("</response>")

		w.close()

	
		#pass
		