#PyMOL surface area batch script
#Frederik Theisen, 2018
#Usage: place file in active folder and execute "run <filename.extension>" #Example: run script.txt
#Ensure the existence of properly formatted database file “path/database.txt”
#Database format example: “1AXC	B”
#Set active folder: cd <folder path>

#Set variables
cmd.do("set solvent_radius, " + str(SolventRadius)) 
cmd.do("set dot_density, " + str(DotDensity)) 

#Prepare molecule
cmd.do("remove hydro")
cmd.do("remove solvent")
cmd.do("show dots")
cmd.do("set dot_solvent, on") 

#Count models 
states = cmd.count_states("all")

total = 0
polar = 0
nonpolar = 0

#Loop through models and calculate surface area for each state 
for i in range(0,states): 
total += cmd.get_area("all", i+1)		#get total area
polar += cmd.get_area("elem N+O", i+1) 		#get polar area
nonpolar += cmd.get_area("elem C+S", i+1) 	#get nonpolar area

#Calculate average values
avg_total = total/states
avg_polar = polar/states
avg_nopol = nonpolar/states


#Load list of PDB codes and ID chain identifiers
database = “path/database.txt”

with open(database) as f:
	lines = f.readlines()

for i in range(0,len(lines)):
	cmd.do("delete all")
	line = lines[i].strip()

	#Get PDB code
	n = line[:4].strip()

	#Fetch molecule
	cmd.fetch(n)

	#Get IDP chain identifier
	disorderedchainref = line[5:].strip()

	#Get IDP sequence and remove chain ID string
	s = cmd.get_fastastr("chain " + disorderedchainref)[5:].strip().replace("\n","")

	#Skip the complex if the IDP contains modified or non-standard residues
	if '?' in seq: continue

	#Filters short IDP chains
	if len(s) < 5: continue

	#Get complex surface (SASA defined as Script 1, returns array containing total, polar #and nonpolar surface area)
	c = SASA()

	#Remove IDP
	cmd.do("remove chain " + str(disorderedchainref))

	#Get folded protein surface
	f = SASA()

	#Converts values to strings and prints in console (copy to text file to save)
	print(n, s, str(f[0]), str(f[1]), str(f[2]), str(c[0]), str(c[1]), str(c[2]))
