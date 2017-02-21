from link import *
from probe import *
from math import *
import scipy.stats
from haversine import haversine

def get_candidates(probe_pt, link_list, r):
	probe_lat, probe_long = probe_pt.getPos()
	min_dist = 1000000000000
	for curr_link in link_list:
		dist, grepLat, grepLong, linkID = curr_link.pointToLink(probe_pt)
		if dist < min_dist:
			min_dist = dist
			min_link = curr_link
		if dist < r:
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
			if count%100==0:
				print count,
			count += 1
			curr_probe = Probe(line)
			get_candidates(curr_probe, all_links, 10)
			if len(curr_probe.grepPoints)<1:
				continue
			if not prev_probe: # the first probe point in the data set
				min_dist = 1000000000000
				for grep in curr_probe.grepPoints:
					dist = grep[0]
					if dist < min_dist:
						min_dist = dist
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.distFromLink = grep[0]
						curr_probe.linkPVID = grep[4]
			else: #prev_probe exists
				prev_probe_grep = prev_probe.bestGrep
				best_result = -1000000000000

				for grep in curr_probe.grepPoints:
					norm_prob = grep[1]
					grep_pos = (grep[2], grep[3])
					delta_d = haversine(curr_probe.getPos(), prev_probe.getPos())*1000
					delta_w = haversine(grep_pos, prev_probe.bestGrep)*1000
					transm_prob = delta_d / (delta_w+0.000000000000001)
					result = norm_prob * transm_prob
					if result > best_result:
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.distFromLink = grep[0]
						curr_probe.linkPVID = grep[4]
						
			for link in all_links:
				if link.linkPVID == curr_probe.linkPVID:
					curr_probe.linkPVID = link.linkPVID
					curr_probe.direction = link.directionOfTravel
					curr_probe.distFromRef = haversine(curr_probe.getPos(), link.RefNode)*1000

			data = curr_probe.sampleID+","+curr_probe.dateTime+","+curr_probe.sourceCode+","+curr_probe.latitude+","
			data += curr_probe.longitude+","+curr_probe.altitude+","+curr_probe.speed+","+curr_probe.heading+","
			data += curr_probe.linkPVID+","+curr_probe.direction+","+str(curr_probe.distFromRef)+","
			data += str(curr_probe.distFromLink)+"\n"
			result_data.write(data)
			
			prev_probe = curr_probe
		result_data.close()



						
	







