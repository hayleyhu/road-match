# road-match
Implement the algorithm to match probe points and links, and calculate the link slope from the assigned probe points.

## Prerequisite 
    link_file = "Partition6467LinkData.csv"
    probe_file = "Partition6467ProbePoints.csv"


## Map-matching:
```
python main.py
```
match_outfile = "MatchedPointsOutput.csv"

## Slope-calculation:
```
python genSlope.py
```
slope_outfile = "slopeAnalysis.csv"