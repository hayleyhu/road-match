from haversine import haversine

class Probe(object):
	def __init__(self, line):
		'''
		ProbePoints Record Format:
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
		'''
			grepPoints are the end on the link egde of the line segment that defines shortest distance between a point and the linkPVID
			--------c-----  l
					|
					|
					P
			For example, the distance between P to l is defined by the distance of cP, so c is one grep point
			bestGrep are selected based on both geometric and topological information
		'''
		self.grepPoints = list()
		self.bestGrep = None

	def getPos(self):
		return map(float, (self.latitude, self.longitude))


class Probe2(object):
	'''
	MatchedPoints Record Format:
		sampleID	is a unique identifier for the set of probe points that were collected from a particular phone.
		dateTime	is the date and time that the probe point was collected.
		sourceCode	is a unique identifier for the data supplier (13 = Nokia).
		latitude	is the latitude in decimal degrees.
		longitude	is the longitude in decimal degrees.
		altitude	is the altitude in meters.
		speed		is the speed in KPH.
		heading		is the heading in degrees.
		linkPVID	is the published versioned identifier for the link.
		direction	is the direction the vehicle was travelling on thelink (F = from ref node, T = towards ref node).
		distFromRef	is the distance from the reference node to the map-matched probe point location on the link in decimal meters.
		distFromLink	is the perpendicular distance from the map-matched probe point location on the link to the probe point in decimal meters.
	'''
	def __init__(self, line1, line2):
		self.sampleID    ,\
		self.dateTime    ,\
		self.sourceCode  ,\
		self.latitude    ,\
		self.longitude   ,\
		self.altitude    ,\
		self.speed       ,\
		self.heading     = line1.split(',')
		_, self.linkPVID ,\
		self.direction 	 ,\
		self.distFromRef ,\
		self.distFromLink = line2.split(',')

	def getPos(self):
		return map(float, (self.latitude, self.longitude))

