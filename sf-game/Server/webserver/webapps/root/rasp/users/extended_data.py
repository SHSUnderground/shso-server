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
import datetime

current_time = datetime.datetime.now()
midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
time_until_midnight = midnight - current_time
hours_until_midnight = time_until_midnight.seconds // 3600
minutes_until_midnight = (time_until_midnight.seconds // 60) % 60
seconds_until_midnight = time_until_midnight.seconds % 60
time_until_midnight = str(hours_until_midnight) + ":" + str(minutes_until_midnight) + ":" + str(seconds_until_midnight)

def escapeQuotes(string):
	string2 = str(string).replace( '"', '\"')
	string2 = string2.replace( "'", "\'")
	string2 = string2.replace("\\", "\\\\")
	return string2

class extended_data(HttpServlet):

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
		last_used_hero = 'iron_man'
		last_used_title = ''
		last_used_medallion = ''
		last_used_sidekick = ''
		last_used_deck = ''

		# Get a reference to the Zone where the target extension is running
		#Zone zone = SmartFoxServer.getInstance().getZone("testZone");
		zone = ex.getZone('shs.all')

		# Get a reference to database manager
		db = zone.dbManager;

		#userID = "3870526"   # this line for doGet testing only !!!!!!!!!!!!!!!
		for name in request.getParameterNames():
			if (name == "AS_SESSION_KEY"):
				session_token = request.getParameter(name)
			if (name=="LastCostume"):
				last_used_hero = request.getParameter(name)
			if (name=="LastDeckID"):
				last_used_deck = request.getParameter(name)
			if (name=="FirstCardGame"):
				FirstCardGame = request.getParameter(name)
			if (name=="DemoHack"):
				DemoHack = request.getParameter(name)
			# if (name==""):
			# 	 = request.getParameter(name)
			
			# if (name == "user"):
			# 	userID = request.getParameter(name)
			# if (name == "user_id"):
			# 	userID = request.getParameter(name)
	
		
		if session_token is not None:
			getUserID = "SELECT * from tokens WHERE token='" + escapeQuotes(session_token) + "'"
			tokenQuery = db.executeQuery(getUserID)
			# userID = None
			
			
			if tokenQuery.size() > 0:
				userID = tokenQuery[0].getItem("userID")
			# userID = 
	
		# fileList = ["POST Request Recieved"]
		# outfile = open("/sf-game/Server/webserver/webapps/root/rasp/inventoryresult.txt", "w")
		# outfile.writelines(fileList)

		# Get a reference to the Extension we want to call 
		#targetExtension = zone.getExtension("escrow");

 

		# Get db record for this player
		error = ""
		usersStr = ""
		fractals = -1
		sql = "SELECT user.* FROM shso.user user WHERE user.ID = " + escapeQuotes(userID)

		queryRes = db.executeQuery(sql)
		if (queryRes == None) or (queryRes.size() == 0):
			error = "db query failed"

		username = None
		if (queryRes.size() > 0):
			for row in queryRes:
				username = row.getItem("Username")
				display_name = row.getItem("nick")
				fractals = row.getItem("Fractals")
									

		# Get all owned characters for this player
		error = ""
		usersStr = ""
		sql = "SELECT heroes.* FROM shso.heroes, shso.user WHERE heroes.UserID = user.ID AND user.ID = " + escapeQuotes(userID)


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

		lastUsedHeroSQL = "SELECT * FROM shso.equips WHERE UserID = " + escapeQuotes(userID)
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
		w.println("    <Content-Type>application/xml; charset=UTF-8</Content-Type>")
		w.println("  </headers>")
		w.println("  <body>&lt;profile&gt;")
		w.println("  &lt;id&gt;" + userID + "&lt;/id&gt;")
		if display_name is not None:
			w.println("  &lt;player_name&gt;" + str(display_name) + "&lt;/player_name&gt;")
		else:
			w.println("  &lt;player_name&gt;" + str(username) + "&lt;/player_name&gt;")
		w.println("  &lt;created&gt;2012-09-16 01:17:50&lt;/created&gt;")
		w.println("  &lt;consecutive_days&gt;45&lt;/consecutive_days&gt;")
		w.println("  &lt;logins_today&gt;5&lt;/logins_today&gt;")
		w.println("  &lt;squad_level&gt;" + str(squadlevel) + "&lt;/squad_level&gt;")
		w.println("  &lt;last_celebrated&gt;65&lt;/last_celebrated&gt;")
		w.println("  &lt;current_challenge&gt;66&lt;/current_challenge&gt;")
		w.println("  &lt;tracker_data&gt;0,525043,414418,511843&lt;/tracker_data&gt;")
		w.println("  &lt;medallion_id&gt;" + str(last_used_medallion) + "&lt;/medallion_id&gt;")
		w.println("  &lt;title_id&gt;" + str(last_used_title) + "&lt;/title_id&gt;")
		w.println("  &lt;sidekick_id&gt;" + str(last_used_sidekick) + "&lt;/sidekick_id&gt;")
		w.println("  &lt;sidekick_tier&gt;2&lt;/sidekick_tier&gt;")
		w.println("  &lt;achievement_points&gt;26050&lt;/achievement_points&gt;")
		w.println("  &lt;current_costume&gt;" + str(last_used_hero) + "&lt;/current_costume&gt;")
		w.println("  &lt;tracker_data&gt;0,525043,414418,511843&lt;/tracker_data&gt;")
		w.println("  &lt;time_til_midnight&gt;" + time_until_midnight + "&lt;/time_til_midnight&gt;")
		w.println("  &lt;extended_data&gt;&lt;LastCostume&gt;" + last_used_hero + "&lt;/LastCostume&gt;&lt;LastDeckID&gt;4791457&lt;/LastDeckID&gt;&lt;FirstCardGame&gt;false&lt;/FirstCardGame&gt;&lt;DemoHack&gt;false&lt;/DemoHack&gt;&lt;/extended_data&gt;")
		w.println("  &lt;entitlements&gt;")
		w.println("    &lt;entitlement code=\"6d84fe391a92aa30eef19bf474f6ab6793be25ff2af44cd4935f46bda3365af1\" name=\"PlayerCountry\" value=\"US\" /&gt;")
		w.println("    &lt;entitlement code=\"859f4b70f96ed5d2186174fb10d246d03ce72782d3eca91e7af4ff1c26ab3284\" name=\"PlayerLanguage\" value=\"en\" /&gt;")
		w.println("    &lt;entitlement code=\"8385401e7e67855e326a7880004a49b92fe1c7adca715f39fe96dc533004466a\" name=\"SubscriptionType\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"4a28ecc14ac89cb41023599c85b045130231bf2bae308b35d8680da8cb930f4c\" name=\"ParentalFriendingDeny\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"12653bc181be54d98da281577e4fb44b85990d74b365f241eb760204cd54fcdd\" name=\"UseExternalShopping\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"a3964840914fbbf1e0cf1cfba89d85ebf85ab0c6f7fdb2052fe8e2d80deb547a\" name=\"ShieldPrizeWheelAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"dcb24bd281c189e559d09313043c5b96a58e6cf958177c4886ffadb915657d59\" name=\"ShieldHeroesAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"887652e99a412db55a68e589d2e69414f9dcc857586fdab3bb4c0f1702d0e939\" name=\"ShoppingCatalog\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"9ed45013f9aea458d58523d9eb657360d650803fc9f802ba09a6c5c00be1e60a\" name=\"OpenChatAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"d8c32a846361fa8489af06af6717bc049bdec947540079e908d732c5ac862633\" name=\"ShieldHQAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"e877bb9327ed4d642ef078828d0f084551871a7131f8090d739843b827ca1b3a\" name=\"ParentalHQDeny\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"283e524ed6e7a8ca99f31a861f4abad7543bf3fb5918f42c3b9172590f7983dd\" name=\"IsPayingSubscriber\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"1c3520f25dc5afb53cccf58778da8287ae29233cb1943ddd064c722a6faaefdf\" name=\"WIPAllow\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"0eb50bddecb277d95a3dbfe9b2c1a84ad64b4b57cd8c8c47e448820d8f2df5b9\" name=\"ArcadeAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"682f82aea1ec79f78d588c70b9dfb90a334b06e7e1b8e64f0b3ff7d8b4f77eef\" name=\"ParentalCardGameDeny\" value=\"False\" /&gt;")
		if username.lower() == "titan":
			w.println("    &lt;entitlement code=\"73acbb6669de525c784c99c033f5c1c61cb48cd799c4ea81dcbf351dd44ad9d6\" name=\"ClientConsoleAllow\" value=\"True\" /&gt;")
		else:
			w.println("    &lt;entitlement code=\"73acbb6669de525c784c99c033f5c1c61cb48cd799c4ea81dcbf351dd44ad9d6\" name=\"ClientConsoleAllow\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"6d6862354a6aa60178f17fbefed2f99c7dce13a2ea0af2a921943f4e008f7c9a\" name=\"ShieldPlayAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"b309cf1388fd03e7a66fcb5f77e0ef94ed18e84bbe72d9d903cc2e2bf6ece208\" name=\"ParentalMissionsDeny\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"02cf12485d5d938b4a6a141e995b72dcc61be3c51648a82cc9920c73dead69e2\" name=\"UnityEditorAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"ece2c2637f6b8b719b7726145b776e66a754f100df4187d006cb2d3c1974001c\" name=\"DemoLimitsOn\" value=\"False\" /&gt;")
		w.println("    &lt;entitlement code=\"18f82b9beacc82bfd027cbc29f3bae7a7cc18989153a3ec38f7bb0d5b3cb6924\" name=\"CardGameAllow\" value=\"True\" /&gt;")
		w.println("    &lt;entitlement code=\"8ab981e527edbf8789c6c47c4d81a5248f2030583896bb9bcd7821d9476e31c4\" name=\"CatalogCountry\" value=\"US\" /&gt;")
		w.println("    &lt;entitlement code=\"bf53b06f786703a442f7d0c2f6991460c8a29c154a16f07dc5fa172900e9eaba\" name=\"MaxChallengeLevel\" value=\"65\" /&gt;")
		w.println("    &lt;entitlement code=\"bd62008e49a7f5ada3826e5821aa7d360a5b1d49b063ccb86ad7f28e269743aa\" name=\"Expiration\" value=\"False\" /&gt;")
		w.println("  &lt;/entitlements&gt;")
		w.println("  &lt;prefs&gt;")
		w.println("    &lt;pref&gt;")
		prefSQL = "SELECT * FROM shso.user_prefs WHERE user_id = " + escapeQuotes(userID)
		queryRes_prefs = db.executeQuery(prefSQL)
		if (queryRes_prefs is not None and queryRes_prefs.size() > 0):
			for row in queryRes_prefs:
				pref_id = row.getItem("pref_id")
				value = row.getItem("value")
				w.println("      &lt;pref_id&gt;" + str(pref_id) + "&lt;/pref_id&gt;")
				w.println("      &lt;value&gt;" + str(value) + "&lt;/value&gt;")
		w.println("    &lt;/pref&gt;")
		w.println("  &lt;/prefs&gt;")
		w.println("  &lt;heroes&gt;")


		# loop thru owned characters

		if (queryRes2.size() > 0):
			for row in queryRes2:
				heroname = row.getItem("Name")
				xp = row.getItem("Xp")
				tier = row.getItem("Tier")
				code = row.getItem("Code")

				w.println("        &lt;hero&gt;")
				w.println("          &lt;name&gt;" + heroname + "&lt;/name&gt;")
				w.println("          &lt;xp&gt;" + str(xp) + "&lt;/xp&gt;")
				w.println("          &lt;tier&gt;" + str(tier) + "&lt;/tier&gt;")
				w.println("          &lt;code&gt;" + code + "&lt;/code&gt;")
				w.println("        &lt;/hero&gt;")
		reskins_sql = "select reskin_name, heroes.xp, heroes.tier, heroes.code from reskins, heroes where LOCATE(name, reskin_name) != 0 AND UserID = " + escapeQuotes(userID)
		reskinsRes = db.executeQuery(reskins_sql)
		if reskinsRes is not None and reskinsRes.size() > 0:
			for reskin_row in reskinsRes:
				heroname = reskin_row.getItem("reskin_name")
				xp = reskin_row.getItem("Xp")
				tier = reskin_row.getItem("Tier")
				code = 'Reskin'
				w.println("        &lt;hero&gt;")
				w.println("          &lt;name&gt;" + str(heroname) + "&lt;/name&gt;")
				w.println("          &lt;xp&gt;" + str(xp) + "&lt;/xp&gt;")
				w.println("          &lt;tier&gt;" + str(tier) + "&lt;/tier&gt;")
				w.println("          &lt;code&gt;" + str(code) + "&lt;/code&gt;")
				w.println("        &lt;/hero&gt;")

		w.println("  &lt;/heroes&gt;")
		w.println("  &lt;currency&gt;")
		w.println("    &lt;tokens&gt;0&lt;/tokens&gt;")
		w.println("    &lt;coins&gt;32&lt;/coins&gt;")
		w.println("    &lt;tickets&gt;20&lt;/tickets&gt;")
		w.println("    &lt;shards&gt;" + fractals + "&lt;/shards&gt;")
		w.println("  &lt;/currency&gt;")
		w.println("  &lt;prize_wheel&gt;")
		w.println("    &lt;earned_stops&gt;0&lt;/earned_stops&gt;")
		w.println("  &lt;/prize_wheel&gt;")
		w.println("&lt;/profile&gt;")
		w.println("</body>")
		w.println("</response>")
		


		#w.println(arrList.get(0))
		#w.println(arrList.get(1))
		#w.println(usersStr)		
		#w.println(scriptPath)


		
		#w.println(self.closeHtml)
		w.close()

	
		#pass
		