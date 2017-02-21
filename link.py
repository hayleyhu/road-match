from math import sin, cos, atan2, sqrt, degrees, radians, pi
from geopy.point import Point
import sys

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
		self.allNodes = self.getAllNodes()
		self.probePoint = list()
		self.numProbe = 0
		self.closestP = None
		self.closestDist = sys.maxint
		self.farthestP = None
		self.farthestDist = 0

		# Returns lat longs and elevations associated with edges of the link		
	def getAllNodes(self):
		'''
			51.4965800/9.3862299/|51.4966899/9.3867100/|51.4968000/9.3873199/|51.4970100/9.3880399/,,
		'''
		nodes = self.shapeInfo.split("|")   
		all_nodes = []
		for n in nodes:
			lat1, lon1, elev1 = n.split('/')
			all_nodes.append([float(lat1), float(lon1)])
		return all_nodes
	
	def pointToLink(self, point):
		x3, y3 = point.getPos()
		min_dist2edge = 100000000000
		x4, y4 = None, None
		for i in range(len(self.allNodes)-1):
			x1= self.allNodes[i][0]
			y1 = self.allNodes[i][1]
			x2 = self.allNodes[i+1][0]
			y2 = self.allNodes[i+1][1]
			xx = x2-x1
			yy = y2-y1
			denom = ((xx * xx) + (yy * yy)) 
			if denom == 0:
				print self.linkPVID,
				print "error line segment has zero length"
			dist2edge = abs((xx*(x3-x1) + yy*(y3-y1))/denom)*1000
			if dist2edge < min_dist2edge:
				min_dist2edge = dist2edge
				x4 = x1 + xx * dist2edge
				y4 = y1 + yy * dist2edge
		return min_dist2edge, x4, y4, self.linkPVID

	def expSlope(self):
		"""
		Slope Calcuation Formula:
			tan(theta) = height/length
			theta = arctan(height/length)
		"""

			# if probe.direction == "T":
			# 	exp_slope = - exp_slope
		lat1, long1, alt1 = self.closestP
		lat2, long2, alt2 = self.farthestP
		vertical = alt2 - alt1
		horizontal = haversine.haversine(lat1, long1, lat2, long2)*1000
		exp_slope = math.degrees(math.atan(vertical/horizontal))




