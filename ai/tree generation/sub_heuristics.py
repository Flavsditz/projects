#!/usr/bin/python

_REF = "out_h0" # name of ref file
_HEUR = "h2" #name of heuristic file

with open(_REF+".txt", "r") as refFile:
	with open("out_"+_HEUR+".txt", "r") as newFile:
		with open("final_"+_HEUR+".txt", "w") as final:
			for lineNew in newFile:
				# Get the relevant infos
				lineNew = lineNew.split(", ")
				heurNew = lineNew[5]

				# Get the infos from old file
				lineRef = refFile.readline()
				lineRef = lineRef.split(", ")

				lineRef[5] = heurNew

				# Write in new file
				final.write(lineRef[0]+", "+lineRef[1]+", "+lineRef[2]+", "+lineRef[3]+", "+lineRef[4]+", "+lineRef[5])
print "DONE!"