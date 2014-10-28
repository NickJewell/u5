from app import app
from py2neo.neo4j import GraphDatabaseService, CypherQuery
from py2neo import neo4j
from py2neo.packages.urimagic import URI
from urlparse import urlparse
import re, json
import sys
from flask import Flask, Response, json, jsonify, request, Blueprint, render_template
import csv



# Home routing

@app.route('/')
@app.route('/index')
def index():
	return render_template("./base.html")


# Unity - specific routing for a pass-through ID
# Unity runs triadic closure on the ID to find friends-of-friends to connect to
# Renders via: templates/tri_recommend.html

@app.route('/recommend/<account>')
def connect_user(account):
	intAcc = int(account)
	results = CypherQuery(graph,"MATCH (p1 {id: {account} })-[rel :KNOWS]->(friend)-[rel2 :KNOWS]->(stranger) WHERE p1 <> stranger RETURN friend.first_name, friend.last_name, stranger.first_name, stranger.last_name, collect(distinct rel2.tag) as ConnectOn order by stranger.first_name").execute(account=intAcc)
	return render_template("./tri_recommend.html", triangles=results)	

# Unity - specific display of friends and friends of friends for pass-through ID
# This could be a default URL when you click on an individual?
# Renders via: templates/user.html

@app.route('/unity/<account>')
def unity(account):
	intAcc = int(account)
	results = CypherQuery(graph,"match (p {id: {account} })-[rel :KNOWS]->(f) RETURN p.id, p.first_name, p.last_name, f.id, f.first_name, f.last_name").execute(account=intAcc)
	return render_template("./user.html", network_rels=results)	

	
# Unity - as /unity route but with a basic data viz view
# Renders via: templates/user_viz.html
@app.route('/unity_viz/<account>')
def unity_viz(account):
	return render_template("user_viz.html", user=account)	
	
# unity_viz_edges
# Used to return the edges in JSON format for d3 rendering
# Called indirectly via user_viz.html

@app.route('/unity_viz_edges/<account>')
def unity_viz_edges(account):
	intAcc = int(account)
	results = CypherQuery(graph,"match (p {id: {account} })-[rel :KNOWS]->(f) RETURN p.id, p.first_name, p.last_name, f.id, f.first_name, f.last_name").execute(account=intAcc)
	a = {}
	x = []

	for e in results:
		a['source'] = "{0} {1}".format(e[1], e[2])
		a['target'] = "{0} {1}".format(e[4], e[5])
		#b = "{0},{1}\n".format(e[0], e[1])
		x.append(a.copy())
		
	z = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))
	
	return z	
	
# Unity - as /unity route but with a basic data viz view
# Renders via: templates/user_viz.html
@app.route('/unity_tag_viz/<tag>')
def unity_tag_viz(tag):
	return render_template("tag_viz.html", tag=tag)	
	
# unity_viz_edges
# Used to return the edges in JSON format for d3 rendering
# Called indirectly via user_viz.html

@app.route('/unity_tag_viz_edges/<tag>')
def unity_tag_viz_edges(tag):
	results = CypherQuery(graph,"match (p)-[rel :KNOWS]->(f) WHERE rel.tag = {tag} RETURN p.id, p.first_name, p.last_name, f.id, f.first_name, f.last_name, rel.strength").execute(tag=tag)
	a = {}
	x = []

	for e in results:
		a['source'] = "{0} {1}".format(e[1], e[2])
		a['target'] = "{0} {1}".format(e[4], e[5])
		#b = "{0},{1}\n".format(e[0], e[1])
		x.append(a.copy())
		
	z = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))
	
	return z	