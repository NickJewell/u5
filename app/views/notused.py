@app.route('/')
@app.route('/index')
def index():
	return "Base --hello"

@app.route('/viz')
def viz():
	return render_template("viz2.html")
	
@app.route('/unity')
def unity():

	#results = CypherQuery(graph, 'MATCH (game)-[:USES_MECHANIC]->(mechanic) WHERE mechanic.mechanic = "Trick-taking" RETURN game.bgg_name order by game.bgg_name').execute()
	#return render_template("games.html", games=results)
	
	results = CypherQuery(graph, 'MATCH (p1 {first_name: "Adam"})-[rel :KNOWS]->(friend)-[rel2: KNOWS]->(stranger) WHERE p1 <> stranger RETURN distinct friend.first_name, friend.last_name, stranger.first_name, stranger.last_name, collect(distinct rel2.tag) as Connect_On;').execute()
	return render_template("triangles.html", triangles=results)

@app.route('/unity/<account>')
def get_user(account):
	""" Display details of a particular graph locale
	"""
	
	#results = CypherQuery(graph, "MATCH (m:Movie) "
	#                                 "WHERE m.title = {title} "
	#                                 "RETURN m").execute(title=title)
	
	#results = CypherQuery(graph, 	"MATCH (p1:Person)-[rel:KNOWS {tag:'data analysis'}]-(p2:Person) "
	#								"WHERE p1.id= {account} " 
	#								"RETURN p2, collect(rel.tag) as tags").execute(account=account)
	#								
	#results = CypherQuery(graph,	"MATCH (p1:Person)-[rel:KNOWS {tag:'data analysis'}]-(p2:Person), (p1:Person)-[test:KNOWS]-(p2:Person)"
	#								"WHERE p1.id= {account} "
	#								"RETURN p2.first_name, p2.last_name, rel.tag, collect(test.tag) as other_tags").execute(account=account)
	#								
									
									
	intAcc = int(account)
	results = CypherQuery(graph, 	"MATCH (p1 {id: {account} })-[rel :KNOWS]->(friend)-[rel2 :KNOWS]->(stranger) WHERE p1 <> stranger RETURN friend.first_name, friend.last_name, stranger.first_name, stranger.last_name, collect(distinct rel2.tag) as ConnectOn order by stranger.first_name").execute(account=intAcc)
	return render_template("triangles.html", triangles=results)

@app.route('/nodes')
def nodes():

	a = {}
	x = []
	results = CypherQuery(graph, 	"MATCH (p)-[:KNOWS]->(p2) RETURN distinct p.first_name, p.last_name").execute()
	
	#for n in results:
	#	a.append(n[0])
		
	for r in results:
		#print >> sys.stderr, r[0]
		#print >> sys.stderr, r[1]
		a['name']=r[0]
		#print >> sys.stderr, a
		x.append(a.copy())
		#print >> sys.stderr, x

	#print >> sys.stderr, a
	
	b = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))

	return b

@app.route('/links')
def links():

	a = {}
	x = []
	results = CypherQuery(graph, 	"MATCH (p1)-[rel]->(p2) RETURN distinct p1.id, p2.id").execute()
	
	for r in results:
		#print >> sys.stderr, r[0]
		#print >> sys.stderr, r[1]
		# -1 because of zero indexing
		a['source']=r[0]-1
		a['target']=r[1]-1
		a['value']=1
		#print >> sys.stderr, a
		x.append(a.copy())
	#print >> sys.stderr, x
#	for n in results:
#		a['source']= n[0][0]
#		a['target']= n[1][0] 
#		x.append(a)

	#print >> sys.stderr, a
	
#	b = json.dumps(x)

	z = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))

	return z

@app.route('/d3noob')
def d3noob():
	return render_template("force2.html")

@app.route('/edges')
def edges():
	a = {}
	x = []
	edges = CypherQuery(graph, "match (p)-[rel :KNOWS]->(q) WHERE rel.strength = '2' RETURN distinct p.id, q.id").execute()
	for e in edges:
		a['source'] = e[0]
		a['target'] = e[1]
		#b = "{0},{1}\n".format(e[0], e[1])
		x.append(a.copy())
	z = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))
	return z


@app.route('/all')
def all():

	dataset = {}
	a = {}
	x = []
	nodes = CypherQuery(graph, 	"MATCH (p)-[:KNOWS]->(p2) RETURN distinct p.first_name, p.last_name").execute()
	
	#for n in results:
	#	a.append(n[0])
		
	for n in nodes:
		#print >> sys.stderr, r[0]
		#print >> sys.stderr, r[1]
		a['name']=n[0]
		#print >> sys.stderr, a
		x.append(a.copy())
		#print >> sys.stderr, x

	#print >> sys.stderr, a
	
	b = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))
	
	dataset['nodes'] = b
	
	a = {}
	x = []
	edges = CypherQuery(graph, 	"MATCH (p1)-[rel]->(p2) RETURN distinct p1.id, p2.id").execute()
	
	for e in edges:
			#print >> sys.stderr, r[0]
			#print >> sys.stderr, r[1]
			# -1 because of zero indexing
			a['source']=e[0]-1
			a['target']=e[1]-1
			a['value']=1
			#print >> sys.stderr, a
			x.append(a.copy())
		#print >> sys.stderr, x
	#	for n in results:
	#		a['source']= n[0][0]
	#		a['target']= n[1][0] 
	#		x.append(a)

		#print >> sys.stderr, a
	
	#	b = json.dumps(x)

	z = json.dumps(x, sort_keys=True, indent=4, separators=(',', ': '))
	
	dataset['edges'] = z
	
	result = json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': '))
	
	
	return render_template("newviz.html")