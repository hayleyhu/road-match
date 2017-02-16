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
		self.heading     ,\
		self.linkPVID    ,\
		self.direction   ,\
		self.distFromRef ,\
		self.distFromLink = line.split(',')
