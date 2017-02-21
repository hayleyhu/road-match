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
		print "Interating all the points...."
		read_header = True	
		prev_probe = None	 
		while True:
			if read_header:
				header = f.readline()
				read_header = False
				continue
			line1 = f.readline()
			line2 = f.readline()
			if not line2:
				break
			probe = Probe2(line1, line2)
			if not prev_probe or probe.linkPVID != prev_probe.linkPVID:
				continue
			"""
			Slope Calcuation Formula:
				tan(theta) = height/length
				theta = arctan(height/length)
			"""
			print "find continuous slope"
			vertical = float(probe.altitude) - float(prev_probe.altitude)
			horizontal = haversine.haversine(prev_probe.getPose(), probe.getPos())*1000
			exp_slope = math.degrees(math.atan(vertical/horizontal))
			if probe.direction == "T":
				exp_slope = - exp_slope
			for link in all_links:
				if link.linkPVID == probe.linkPVID:
					print "find match"
					link.expSlopeSum += exp_slope
					link.numProbe += 1
					break
	
	slope_outfile = "slopeAnalysis.csv"
	slopef = open(slope_outfile, "w+")
	header = "linkPVID, refSlope, probeSlope, diff\n"
	slopef.write(header)
	print "Interating all the links..."
	for link in all_links:
		if link.numProbe > 0:
			probeSlope = link.expSlopeSum / float(link.numProbe)
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
			
		
				
			
			
