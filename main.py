from link import *
from probe import *
from math import *
import scipy.stats
from haversine import haversine
''' Haversine is used to calculate the distance between two points in the earth.
	Source: https://pypi.python.org/pypi/haversine
'''

def get_candidates(probe_pt, link_list, r):
	'''
	Args: 
		probe_pt (Probe): a probe point
		link_list (listof Link): all links 
		r (int): the threshold distance (in meters) from the point to the link to 
					select qualified link candidates
	
	'''
	probe_lat, probe_long = probe_pt.getPos()
	min_dist = 1000000000000
	for curr_link in link_list:
		dist, grepLat, grepLong, linkID = curr_link.pointToLink(probe_pt)
		if dist < min_dist:
			min_dist = dist
			min_link = curr_link
		if dist < r:
			'''
			Observation Probability is caculated by Normal Distribution probability density function
				with mean = 0 and standard deviation = 2
			'''
			prob = scipy.stats.norm(0, 2).pdf(dist)
			probe_pt.grepPoints.append([dist, prob, grepLat, grepLong, linkID]) 


		
if __name__ == "__main__":

	all_links = list()
	all_probes = list()
	link_file = "Partition6467LinkData.csv"
	probe_file = "Partition6467ProbePoints2.csv"
	match_outfile = "MatchedPointsOutput2.csv"

	with open(link_file) as f:
		for line in f:
			curr_link = Link(line)
			all_links.append(curr_link)
	result_data = open(match_outfile,'w')
	result_data.close()
	prev_probe = None

	with open(probe_file) as f:
		result_data = open(match_outfile,'w+')
		# header = 'sampleID, dateTime, sourceCode, latitude,	longitude, altitude, speed,	heading, linkPVID, direction, distFromRef, distFromLink'
		# result_data.write(header+"\n")
		count = 0
		for line in f:
			# tracking progress while running the program
			if count%100==0: 
				print count, 
			count += 1
			curr_probe = Probe(line)
			get_candidates(curr_probe, all_links, 10)
			if len(curr_probe.grepPoints)<1:
				continue
			'''
			The first probe point is assigned to the link with its shortest distance.
			For later probe points, Transimission Probability is calculated as delta_d/delta_w, 
				where delta_d is the distance between curr_probe and prev_probe, and 
				delta_w is the distance between any curr grep to the previous best grep.
			'''
			if not prev_probe: 
				min_dist = 1000000000000
				for grep in curr_probe.grepPoints:
					dist = grep[0]
					if dist < min_dist:
						min_dist = dist
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.distFromLink = grep[0]
						curr_probe.linkPVID = grep[4]
			else: 
				prev_probe_grep = prev_probe.bestGrep
				best_result = -1000000000000

				for grep in curr_probe.grepPoints:
					norm_prob = grep[1]
					grep_pos = (grep[2], grep[3])
					delta_d = haversine(curr_probe.getPos(), prev_probe.getPos())*1000
					delta_w = haversine(grep_pos, prev_probe.bestGrep)*1000
					transm_prob = delta_d / (delta_w+0.000000000000001)
					''' 
					The grep point with the largest product of norm_prob and transm_prob is selected
					'''
					result = norm_prob * transm_prob
					if result > best_result:
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.distFromLink = grep[0]
						curr_probe.linkPVID = grep[4]
						
			for link in all_links:
				if link.linkPVID == curr_probe.linkPVID:
					curr_probe.linkPVID = link.linkPVID
					curr_probe.direction = link.directionOfTravel
					curr_probe.distFromRef = haversine(curr_probe.getPos(), link.RefNode)
					break

			data = curr_probe.sampleID+","+curr_probe.dateTime+","+curr_probe.sourceCode+","+curr_probe.latitude+","
			data += curr_probe.longitude+","+curr_probe.altitude+","+curr_probe.speed+","+curr_probe.heading+","
			data += curr_probe.linkPVID+","+curr_probe.direction+","+str(curr_probe.distFromRef)+","
			data += str(curr_probe.distFromLink)+"\n"
			result_data.write(data)
			
			prev_probe = curr_probe
		result_data.close()



						
	







