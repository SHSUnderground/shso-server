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
sys.path.append('sf-game/SFS_PRO_1.6.6/Server/webserver/webapps/root/pylibcsp')
import pylibcsp 

class squad(HttpServlet):

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
		userID = None
		session_token = None

		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to database manager
		db = zone.dbManager
		jdbconnection = db.getConnection()

		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)
			# if (name == "user"):
			# 	userID = request.getParameter(name)
			# if (name == "user_id"):
			# 	userID = request.getParameter(name)
	
		
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token= ?"
			prepare = jdbconnection.prepareStatement(getUserID)
			prepare.setString(1,session_token)
			tokenQuery = prepare.executeQuery()
			# userID = None
			
			
			if tokenQuery.next():
				userID = tokenQuery.getInt("userID")
				playerID = userID
 
			tokenQuery.close()
			prepare.close() 
	
		# fileList = ["POST Request Recieved"]
        # outfile = open("sf-game/SFS_PRO_1.6.6/Server/webserver/webapps/root/rasp/inventoryresult.txt", "w")
        # outfile.writelines(fileList)

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

 

		# Get db record for this player
		error = ""
		usersStr = ""
		fractals = -1
		sql = "SELECT user.* FROM shso.user user WHERE user.ID = " + userID

		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"

		username = None
		if (queryRes.size() > 0):
			for row in queryRes:
				username = row.getItem("Username")
				fractals = row.getItem("Fractals")
									

		# Get all owned characters for this player
		error = ""
		usersStr = ""
		sql = "SELECT heroes.* FROM shso.heroes, shso.user WHERE heroes.UserID = user.ID AND user.ID = " + userID


		queryRes2 = db.executeQuery(sql)
		if (queryRes2 == None) or (queryRes2.size() == 0):
			error = "db query failed"

		XPlist = [0, 100, 400, 900, 1600, 2500, 3600, 4900, 6400, 8100, 10000, 12000, 14500, 17000, 20000, 23000, 27000, 31000, 35000, 40000, 45000, 50000, 55000, 60000, 66000, 72000, 79000, 86000, 93000, 100000, 108000, 116000, 125000, 134000, 144000, 154000, 165000, 176000, 188000, 200000]	
		heroScores = { 'abomination_playable': 1, 'agent_coulson': 2, 'agent_venom': 1, 'american_dream': 2, 'angel': 1, 'annihilus_playable': 3, 'anti_venom': 1, 'ant_man': 0, 'arachne': 1, 'archangel': 1, 'archangel_x_force': 1, 'beast': 3, 'beta_ray_bill': 1, 'black_cat': 1, 'black_panther': 2, 'black_widow': 2, 'black_widow_avengers': 2, 'blade': 0, 'cable': 1, 'captain_america': 3, 'captain_america_avengers': 3, 'captain_america_bucky': 2, 'captain_america_stealth': 3, 'captain_america_wwii': 3, 'captain_marvel': 2, 'carnage_playable': 0, 'colossus': 1, 'cyclops': 3, 'cyclops_astonishing': 3, 'cyclops_first': 3, 'daredevil': 1, 'daredevil_armored': 1, 'daredevil_classic': 1, 'daredevil_shadowland': 1, 'deadpool': 0, 'deadpool_pirate': 1, 'deadpool_x_force': 1, 'destroyer_playable': 0, 'dracula_playable': 2, 'drax': 1, 'dr_doom_future_foundation': 2, 'dr_doom_playable': 2, 'dr_octopus_playable': 1, 'dr_strange': 2, 'electro_playable': 1, 'elektra': 0, 'elektra_pure': 1, 'emma_frost': 1, 'enchantress_playable': 1, 'falcon': 1, 'falcon_exo7': 1, 'firestar': 0, 'frankenstein': 0, 'gambit': 1, 'gamora': 2, 'ghost_rider': 0, 'ghost_rider_classic': 1, 'giant_man': 2, 'goliath': 1, 'green_goblin_playable': 1, 'groot': 1, 'guardian': 2, 'havok': 2, 'hawkeye': 0, 'hawkeye_avengers': 1, 'hope_summers': 1, 'hulk': 0, 'hulk_avengers': 3, 'hulk_gladiator': 0, 'hulk_indestructible': 1, 'hulk_mrfixit': 1, 'hulk_red': 0, 'human_torch': 1, 'iceman': 1, 'impossible_man_playable': 1, 'invisible_woman': 2, 'invisible_woman_future': 3, 'iron_fist': 1, 'iron_man': 3, 'iron_man_2020': 2, 'iron_man_arctic': 3, 'iron_man_avengers': 3, 'iron_man_hulkbuster': 3, 'iron_man_midas': 2, 'iron_man_mk1': 2, 'iron_man_mk2': 2, 'iron_man_mk42': 2, 'iron_man_silvercenturion': 2, 'iron_man_stealth': 3, 'iron_monger': 2, 'iron_patriot': 1, 'jean_grey': 1, 'jean_grey_dark_phoenix': 1, 'jean_grey_phoenix': 1, 'jean_grey_phoenix_white': 1, 'juggernaut_playable': 1, 'lizard_playable': 1, 'loki_avengers_playable': 2, 'loki_thor2_playable': 1, 'luke_cage': 0, 'magneto_playable': 2, 'modok_playable': 1, 'monkey_king': 0, 'moon_knight': 1, 'morbius': 0, 'mr_fantastic': 3, 'mr_fantastic_future': 3, 'ms_marvel': 3, 'mysterio_playable': 1, 'mystique_playable': 2, 'nick_fury': 2, 'nick_fury_avengers': 2, 'nightcrawler': 2, 'nightcrawler_swashbuckler': 2, 'nighthawk': 2, 'nova': 2, 'nova_modern': 1, 'onslaught_playable': 0, 'psylocke': 1, 'psylocke_x_force': 2, 'punisher': 0, 'punisher_thunderbolts': 2, 'quicksilver': 1, 'reptil': 1, 'rescue': 1, 'rocket_raccoon': 1, 'rogue': 1, 'rogue_avenging': 1, 'ronan': 2, 'sabretooth_playable': 0, 'sandman_playable': 1, 'sasquatch': 1, 'scarlet_witch': 1, 'sentry': 1, 'shadowcat': 2, 'she_hulk': 1, 'she_hulk_red': 0, 'silver_surfer': 1, 'silver_surfer_dark': 0, 'spiderham': 2, 'spider_girl': 1, 'spider_girl_black': 2, 'spider_gwen': 1, 'spider_man': 3, 'spider_man_2099': 1, 'spider_man_armored': 3, 'spider_man_assassin': 2, 'spider_man_bagman': 1, 'spider_man_ben': 2, 'spider_man_bigtime': 2, 'spider_man_black': 2, 'spider_man_eote': 2, 'spider_man_first': 2, 'spider_man_future': 3, 'spider_man_iron': 2, 'spider_man_noir': 1, 'spider_man_scarlet': 1, 'spider_man_spdr': 2, 'spider_man_superior': 1, 'spider_man_ultimate': 1, 'spider_woman': 1, 'squirrel_girl': 1, 'star_lord': 3, 'storm': 2, 'storm_mohawk': 0, 'super_skrull_playable': 2, 'taskmaster_playable': 1, 'thanos_playable': 2, 'thing': 1, 'thing_future': 2, 'thing_tuxedo': 1, 'thor': 1, 'thor_battle_armor': 1, 'thor_classic': 1, 'thor_movie': 3, 'thor_ultimate': 1, 'tigra': 1, 'titanium_man_playable': 1, 'ultron_playable': 0, 'ultron_playable_gold': 0, 'valkyrie': 1, 'venom_playable': 0, 'vision': 1, 'war_machine': 2, 'war_machine_iron_patriot': 2, 'war_machine_mk2': 2, 'wasp': 2, 'werewolf': 1, 'winter_soldier_playable': 1, 'wolverine': 2, 'wolverine_avenging': 2, 'wolverine_classic': 1, 'wolverine_jeans': 1, 'wolverine_samurai': 2, 'wolverine_x_force': 3, 'wonder_man': 1 }
		heroNames = ['abomination_playable', 'agent_coulson', 'agent_venom', 'american_dream', 'angel', 'annihilus_playable', 'anti_venom', 'ant_man', 'arachne', 'archangel', 'archangel_x_force', 'beast', 'beta_ray_bill', 'black_cat', 'black_panther', 'black_widow', 'black_widow_avengers', 'blade', 'cable', 'captain_america', 'captain_america_avengers', 'captain_america_bucky', 'captain_america_stealth', 'captain_america_wwii', 'captain_marvel', 'carnage_playable', 'colossus', 'cyclops', 'cyclops_astonishing', 'cyclops_first', 'daredevil', 'daredevil_armored', 'daredevil_classic', 'daredevil_shadowland', 'deadpool', 'deadpool_pirate', 'deadpool_x_force', 'destroyer_playable', 'dracula_playable', 'drax', 'dr_doom_future_foundation', 'dr_doom_playable', 'dr_octopus_playable', 'dr_strange', 'electro_playable', 'elektra', 'elektra_pure', 'emma_frost', 'enchantress_playable', 'falcon', 'falcon_exo7', 'firestar', 'frankenstein', 'gambit', 'gamora', 'ghost_rider', 'ghost_rider_classic', 'giant_man', 'goliath', 'green_goblin_playable', 'groot', 'guardian', 'havok', 'hawkeye', 'hawkeye_avengers', 'hope_summers', 'hulk', 'hulk_avengers', 'hulk_gladiator', 'hulk_indestructible', 'hulk_mrfixit', 'hulk_red', 'human_torch', 'iceman', 'impossible_man_playable', 'invisible_woman', 'invisible_woman_future', 'iron_fist', 'iron_man', 'iron_man_2020', 'iron_man_arctic', 'iron_man_avengers', 'iron_man_hulkbuster', 'iron_man_midas', 'iron_man_mk1', 'iron_man_mk2', 'iron_man_mk42', 'iron_man_silvercenturion', 'iron_man_stealth', 'iron_monger', 'iron_patriot', 'jean_grey', 'jean_grey_dark_phoenix', 'jean_grey_phoenix', 'jean_grey_phoenix_white', 'juggernaut_playable', 'lizard_playable', 'loki_avengers_playable', 'loki_thor2_playable', 'luke_cage', 'magneto_playable', 'modok_playable', 'monkey_king', 'moon_knight', 'morbius', 'mr_fantastic', 'mr_fantastic_future', 'ms_marvel', 'mysterio_playable', 'mystique_playable', 'nick_fury', 'nick_fury_avengers', 'nightcrawler', 'nightcrawler_swashbuckler', 'nighthawk', 'nova', 'nova_modern', 'onslaught_playable', 'psylocke', 'psylocke_x_force', 'punisher', 'punisher_thunderbolts', 'quicksilver', 'reptil', 'rescue', 'rocket_raccoon', 'rogue', 'rogue_avenging', 'ronan', 'sabretooth_playable', 'sandman_playable', 'sasquatch', 'scarlet_witch', 'sentry', 'shadowcat', 'she_hulk', 'she_hulk_red', 'silver_surfer', 'silver_surfer_dark', 'spiderham', 'spider_girl', 'spider_girl_black', 'spider_gwen', 'spider_man', 'spider_man_2099', 'spider_man_armored', 'spider_man_assassin', 'spider_man_bagman', 'spider_man_ben', 'spider_man_bigtime', 'spider_man_black', 'spider_man_eote', 'spider_man_first', 'spider_man_future', 'spider_man_iron', 'spider_man_noir', 'spider_man_scarlet', 'spider_man_spdr', 'spider_man_superior', 'spider_man_ultimate', 'spider_woman', 'squirrel_girl', 'star_lord', 'storm', 'storm_mohawk', 'super_skrull_playable', 'taskmaster_playable', 'thanos_playable', 'thing', 'thing_future', 'thing_tuxedo', 'thor', 'thor_battle_armor', 'thor_classic', 'thor_movie', 'thor_ultimate', 'tigra', 'titanium_man_playable', 'ultron_playable', 'ultron_playable_gold', 'valkyrie', 'venom_playable', 'vision', 'war_machine', 'war_machine_iron_patriot', 'war_machine_mk2', 'wasp', 'werewolf', 'winter_soldier_playable', 'wolverine', 'wolverine_avenging', 'wolverine_classic', 'wolverine_jeans', 'wolverine_samurai', 'wolverine_x_force', 'wonder_man']
		squadlevel = 0
		
		if (queryRes2.size() > 0):
			for row in queryRes2:
				xp = int(row.getItem("Xp"))
				XPlist.append(xp+0.5)
				XPlist.sort()
				heroName = row.getItem("Name")
				# #testvar = heroName + ''
				# testvar2 = heroScores[0]['angel']
				# _server.trace("Hero name: ")
				if heroName in heroNames:
					squadlevel += XPlist.index(xp+0.5) + heroScores[str(heroName)]	
				else:
					squadlevel += XPlist.index(xp+0.5) #+ heroScores[0][str(heroName)]
				# squadlevel += heroScores[0][str(heroName)]
				XPlist.pop(XPlist.index(xp+0.5))


		w = response.getWriter()

		lastUsedHeroSQL = "SELECT * FROM shso.equips WHERE UserID = " + userID
		# lastUsedHeroSQL = "SELECT hero FROM shso.equips WHERE userid = " + userID
		lastUsedQueryRes = db.executeQuery(lastUsedHeroSQL)
		last_used_hero = 'iron_man'
		last_used_title = ''
		last_used_medallion = ''
		last_used_sidekick = ''
		if(lastUsedQueryRes.size() > 0):
			if(lastUsedQueryRes[0].getItem("hero_name") is not None):
				last_used_hero = str(lastUsedQueryRes[0].getItem("hero_name"))
			if (lastUsedQueryRes[0].getItem("title_id") is not None):
				last_used_title = str(lastUsedQueryRes[0].getItem("title_id"))
			if (lastUsedQueryRes[0].getItem("medallion_id") is not None):
				last_used_medallion = str(lastUsedQueryRes[0].getItem("medallion_id"))
			if(lastUsedQueryRes[0].getItem("sidekick_id") is not None):
				last_used_sidekick = str(lastUsedQueryRes[0].getItem("sidekick_id"))

		w.println("<response>")
		w.println("  <status>200</status>")
		w.println("  <headers>")
		w.println("    <Content-Type>application/json; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>{")
		w.println('"id:"' + userID + ",")
		w.println('"player_name"' + username + ",")
		# w.println("  created:2012-09-16 01:17:50:)
		# w.println("  consecutive_days:45:)
		# w.println("  logins_today:5:)
		# w.println("  squad_level:" + str(squadlevel) :)
		w.println('"last_celebrated:"' + "65" + ",")
		w.println('"current_challenge:"' + "66" + ",")
		w.println('"tracker_data:"' + "0,525043,414418,511843" + ",")
		w.println('"medallion_id:"' + str(last_used_medallion) + ",")
		w.println('"title_id:"' + str(last_used_title) + ",")
		w.println('"sidekick_id:"' + str(last_used_sidekick) + ",")
		w.println('"sidekick_tier:"' + "2" + ",")
		w.println('"achievement_points:"' + "26050" + ",")
		w.println('"current_costume:"' + str(last_used_hero) + ",")
		# w.println("extended_data:LastCostume:" + last_used_hero + "/LastCostume:LastDeckID:4791457/LastDeckID:FirstCardGame:false/FirstCardGame:DemoHack:false/DemoHack::)
		
		
		# w.println("      value:424999,414586,376099,350432:)
		w.println('"heroes:"{')


		# loop thru owned characters

		if (queryRes2.size() > 0):
			for row in queryRes2:
				heroname = row.getItem("Name")
				xp = row.getItem("Xp")
				tier = row.getItem("Tier")
				code = row.getItem("Code")

				w.println("{")
				w.println('"name:"' + heroname + ",")
				w.println('"xp:"' + str(xp) + ",")
				w.println('"tier:"' + str(tier) + ",")
				w.println('"code:"' + code + ",")
				w.println("}")


		w.println("}")
		# w.println("  currency:")
		# w.println("    tokens:0:)
		# w.println("    coins:32:)
		# w.println("    tickets:20:)
		# w.println("    shards:" + fractals :)
		# w.println("  :)
		# w.println("  prize_wheel:")
		# w.println("    earned_stops:0:)
		# w.println("  :)
		# w.println(":)
		w.println("}</body>")
		w.println("</response>")
		


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))
		#w.println(usersStr)		
		#w.println(scriptPath)


		
		#w.println(self.closeHtml)
		w.close()

		jdbconnection.close()
		#pass
		