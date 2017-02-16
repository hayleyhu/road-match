class Link(object):
	def __init__(self, line):
		'''
			linkPVID		is the published versioned identifier for the link.
			refNodeID		is the internal identifier for the link's reference node.
			nrefNodeID		is the internal identifier for the link's non-reference node.
			length			is the length of the link (in decimal meters).
			functionalClass		is the functional class for the link (1-5).
			directionOfTravel	is the allowed direction of travel for the link (F is from ref node, T is towards ref node, B - both)
			speedCategory		is the speed category for the link (1-8).
			fromRefSpeedLimit	is the speed limit for the link (in kph) in the direction of travel from the reference node.
			toRefSpeedLimit		is the speed limit for the link (in kph) in the direction of travel towards the reference node.
			fromRefNumLanes		is the number of lanes for the link in the direction of travel from the reference node.
			toRefNumLanes		is the number of lanes for the link in the direction of travel towards the reference node.
			multiDigitized		is a flag to indicate whether or not the link is multiply digitized (T is is multiply digitized, F is singly digitized).
			urban			is a flag to indicate whether or not the link is in an urban area (T is in urban area, F is in rural area).
			timeZone		is the time zone offset (in decimal hours) from UTC.
			shapeInfo		contains an array of shape entries consisting of the latitude and longitude (in decimal degrees) and elevation (in decimal meters) for the link's nodes and shape points ordered as reference node, shape points, non-reference node. The array entries are delimited by a vertical bar character and the latitude, longitude, and elevation values for each entry are delimited by a forward slash character (e.g. lat/lon/elev|lat/lon/elev). The elevation values will be null for link's that don't have 3D data.
			curvatureInfo		contains an array of curvature entries consisting of the distance from reference node (in decimal meters) and curvature at that point (expressed as a decimal value of 1/radius in meters). The array entries are delimited by a vertical bar character and the distance from reference node and curvature values for each entry are separated by a forward slash character (dist/curvature|dist/curvature). This entire field will be null if there is no curvature data for the link.
			slopeInfo		contains an array of slope entries consisting of the distance from reference node (in decimal meters) and slope at that point (in decimal degrees). The array entries are delimited by a vertical bar character and the distance from reference node and slope values are separated by a forward slash character (dist/slope|dist/slope). This entire field will be null if there is no slope data for the link.
		'''
		self.linkPVID		  ,\
		self.refNodeID		  ,\
		self.nrefNodeID		  ,\
		self.length			  ,\
		self.functionalClass  ,\
		self.directionOfTravel,\
		self.speedCategory	  ,\
		self.fromRefSpeedLimit,\
		self.toRefSpeedLimit  ,\
		self.fromRefNumLanes  ,\
		self.toRefNumLanes	  ,\
		self.multiDigitized	  ,\
		self.urban			  ,\
		self.timeZone		  ,\
		self.shapeInfo		  ,\
		self.curvatureInfo	  ,\
		self.slopeInfo		  = line.strip().split(',')
		self.RefNodeLat,self.RefNodeLong,_  = self.shapeInfo.split('|')[0].split('/')
		self.RefNode = map(float, (self.RefNodeLat,self.RefNodeLong))
		self.NrefNodeLat,self.NrefNodeLong,_  = self.shapeInfo.split('|')[0].split('/')
		self.NrefNode = map(float, (self.NrefNodeLat,self.NrefNodeLong))
