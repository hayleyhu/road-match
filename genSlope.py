from haversine import haversine
import math
from link import *
from probe import *



if __name__=="__main__":
	all_links = list()
	matched_outfile = "MatchedPointsOutput.csv"
	link_file = "Partition6467LinkData.csv"
	
	with open(link_file) as f:
		for line in f:
			curr_link = Link(line)
			all_links.append(curr_link)

	with open(matched_outfile) as f:
		print "Iterating all the points...."
		header = f.readline() 
		while True:
			# if read_header:
				
			# 	read_header = False
			# 	continue
			line1 = f.readline()
			line2 = f.readline()
			if not line2:
				break
			probe = Probe2(line1, line2)
			# if (not prev_probe) or (probe.linkPVID != prev_probe.linkPVID):
			# 	continue
			# """
			# Slope Calcuation Formula:
			# 	tan(theta) = height/length
			# 	theta = arctan(height/length)
			# """
			# print "find continuous slope"
			# vertical = float(probe.altitude) - float(prev_probe.altitude)
			# horizontal = haversine.haversine(prev_probe.getPose(), probe.getPos())*1000
			# exp_slope = math.degrees(math.atan(vertical/horizontal))
			# if probe.direction == "T":
			# 	exp_slope = - exp_slope
			for link in all_links:
				if link.linkPVID == probe.linkPVID:
					if probe.distFromRef < link.closestDist:
						link.closestDist = probe.distFromRef
						link.closestP = map(float, (probe.latitude, probe.longitude, probe.altitude))
					if probe.distFromRef > link.farthestDist:
						link.farthestDist = probe.distFromRef
						link.farthestP = map(float, (probe.latitude, probe.longitude, probe.altitude))
					link.numProbe += 1

					break
	
	slope_outfile = "slopeAnalysis.csv"
	slopef = open(slope_outfile, "w+")
	header = "linkPVID, refSlope, probeSlope, diff\n"
	slopef.write(header)
	print "Iterating all the links..."
	for link in all_links:
		if link.numProbe > 1:
			if (not link.closestP) or (not link.farthestP):
				print link.linkPVID,
				print link.numProbe, 
				print link.closestDist,
				print link.farthestDist
				continue
			probeSlope = link.expSlope()
			"""
			Link data contains slopes for several reference nodes. The average of all provided slopes serves as refSlope.
			"""
			slope_info = link.slopeInfo.strip().split('|')
			ref_slope_sum = 0
			for si in slope_info:
				ref_slope_sum += float(si.strip().split('/')[1])
			refSlope = ref_slope_sum/len(slope_info)
			diff = refSlope - probeSlope
			result = "%s, %f, %f, %f\n" %(link.linkPVID, refSlope, probeSlope, diff)
			print result
			slopef.write(result)
	slopef.close()
			
		
				
			
			
