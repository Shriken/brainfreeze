from cPickle import dumps, loads
from world import World
from flask import session
import interface
import math
import json
import db

def match_username(form):
	results = db.matchUsername(form['username'])
	results = [account['username'] for account in results]
	if session['username'] in results:
		results.remove(session['username'])
	return json.dumps(results)

def submit_code(form):
	game = db.getGame(int(form['game_id']))
	# TODO make sure the player is in the game
	player_id = game['players'].index(session['username'])

	# if the player has already submitted src
	if int(game['turn']) <= len(game['srces'][player_id]):
		return "sonofabitch"

	# submit his src
	game['srces'][player_id].append(form['src'])

	# crash is our debug dummy
	if game['players'][1] == "crash":
		game['srces'][1].append("")

	all_submitted = all_same(map(len, game['srces']))
	if all_submitted:
		simulate_turn(game)
	store(game)
	return "all good"

def simulate_turn(game):
	# get the pickled game object
	world = loads(game['states'][-1].encode('ascii', 'replace'))

	# get all srces from this turn
	last_srces = [l[-1] for l in game['srces']]

	# interpret the srces
	out = interface.interpret(last_srces, 250, 5, world.step,
	                          world.get_callbacks())
	print "Interpreter:", out # interpreter debug message

	# make sure the world ran for the whole turn
	while world.timestamp % 250 != 0:
		world.step()
	
    # check if the game is over
	units = [[u.dead for u in world.units if u.player == p]
	         for p in range(world.num_players)]
	players_lost = map(lambda l: reduce(lambda a,b: a and b, l), units)
	if players_lost[0] and players_lost[1]: # tie
		game["finished"] = 3
	elif players_lost[0]:
		game["finished"] = 1
	elif players_lost[1]:
		game["finished"] = 2
	if game["finished"]:
		world.end_game(game["finished"])

	# save the event history
	for player_id in range(len(game['jsons'])):
		game['jsons'][player_id].append(world.history.get_events(player_id))
	world.history.clear_events()

	# repickle the world and store it as the newest state
	game['states'].append(dumps(world))

	# increment the turncount
	game['turn'] += 1

def store(game):
	db.updateGame(game['game_id'], game)

def get_json(form):
	game = db.getGame(int(form['game_id']))

	# if they're requesting a non-existent turn
	if int(game['turn']) < int(form['turn']):
		return "{'success': false}"

	# get the player's part
	player_id = game['players'].index(session['username'])
	events_list = game['jsons'][player_id]

	json_objs = events_list[:int(form['turn']) + 1]
	objs = map(json.loads, json_objs)

	# merge event dicts into one dict
	events = {k: v for obj in objs
	               for k,v in obj.items()}
	events['success'] = True;
	return json.dumps(events)

def get_turn(form):
	game = db.getGame(int(form['game_id']))
	return str(game['turn'])

def all_same(l):
	def ats(l, v):
		return len(l) == 0 or (v == l[0] and ats(l[1:], v))
	return ats(l[1:], l[0])
