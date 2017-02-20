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
		if dist < r:
			# min_dist = dist
			# probe_pt.linkPVID = curr_link.linkPVID
			prob = scipy.stats.norm(0, 20).pdf(dist)
			probe_pt.grepPoints.append([dist, prob, grepLat, grepLong, linkID])
	
	# for curr_link in link_list:
	# 	if curr_link.linkPVID == probe_pt.linkPVID:
	# 		curr_link.candidates.append(probe_pt)
	if len(probe_pt.grepPoints) < 1:
		print "no candidate",
		print min_dist 


		
if __name__ == "__main__":

	all_links = list()
	all_probes = list()
	link_file = "Partition6467LinkData.csv"
	probe_file = "Partition6467ProbePoints.csv"


	with open(link_file) as f:
		for line in f:
			curr_link = Link(line)
			all_links.append(curr_link)

	prev_probe = None
	with open(probe_file) as f:
		count = 0
		for line in f:
			if count>100:
				break
			curr_probe = Probe(line)
			print count,
			get_candidates(curr_probe, all_links, 100)		
			all_probes.append(curr_probe)
			count += 1
			if not prev_probe: # the first probe point in the data set
				min_dist = 1000000000000
				for grep in curr_probe.grepPoints:
					dist = grep[0]
					if dist < min_dist:
						min_dist = dist
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.linkPVID = grep[4]
			else: #prev_probe exists
				prev_probe_grep = prev_probe.bestGrep
				best_result = -1000000000000
				for grep in curr_probe.grepPoints:
					norm_prob = grep[1]
					grep_pos = (grep[2], grep[3])
					delta_d = haversine(curr_probe.getPos(), prev_probe.getPos())*1000
					delta_w = haversine(grep_pos, prev_probe.bestGrep)*1000
					transm_prob = delta_d / delta_w
					result = norm_prob * transm_prob
					print "---",
					print grep[0], 
					print norm_prob, 
					print transm_prob
					if result > best_result:
						curr_probe.bestGrep = (grep[2], grep[3])
						curr_probe.linkPVID = grep[4]
			print curr_probe.linkPVID
			prev_probe = curr_probe


			# if not prev_probe:
			# 	probe.slope = 'X'
			# elif probe.linkPVID != prev_probe.linkPVID:
			# 	probe.slope = 'X'
			# else:
			# 	opposite = float(probe.altitude) - float(prev_probe.altitude)
			# 	start = map(float, [probe.longitude, probe.latitude])
			# 	end = map(float, [prev_probe.longitude, prev_probe.latitude])
			# 	hypotenuse = haversine.haversine(start[0],start[1],end[0],end[1])/1000
			# 	probe.slope = math.atan(opposite/hypotenuse)
			# 	probe.slope = (2*math.pi*probe.slope)/360	


						
	







