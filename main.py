from link imoprt *
from probe import *

if __name__ == "__main__":

	all_links = list()
	link_file = "Partition6467LinkData.csv"

	with open(link_file) as f:
		for line in f:
			curr = Link(line)			
			all_links.append(curr)