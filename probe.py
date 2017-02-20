from haversine import haversine

class Probe(object):
	def __init__(self, line):
		'''
			sampleID	is a unique identifier for the set of probe points that were collected from a particular phone.
			dateTime	is the date and time that the probe point was collected.
			sourceCode	is a unique identifier for the data supplier (13 = COMPANY).
			latitude	is the latitude in decimal degrees.
			longitude	is the longitude in decimal degrees.
			altitude	is the altitude in meters.
			speed		is the speed in KPH.
			heading		is the heading in degrees.
		'''
		self.sampleID    ,\
		self.dateTime    ,\
		self.sourceCode  ,\
		self.latitude    ,\
		self.longitude   ,\
		self.altitude    ,\
		self.speed       ,\
		self.heading     = line.split(',')
		self.linkPVID = None
		self.direction = None
		self.distFromRef = None
		self.distFromLink = None
		self.grepPoints = list()
		self.bestGrep = None

	def getPos(self):
		return map(float, (self.latitude, self.longitude))


	# def distToLink(self, link):
	# 	min_dist = haversine(self.getPos(), link.RefNode)
	# 	for node in link.allNodes[1:]:
	# 		X2, Y2 = node[0], node[1]
	# 		dist = haversine(self.getPos, (X2, Y2))
	# 		if dist < min_dist:
	# 			min_dist = dist

	# 	return min_dist*1000

