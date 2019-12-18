#PyMOL surface area batch script
#Frederik Theisen, 2018
#Usage: place file in active folder and execute "run <filename.extension>" #Example: run script.txt
#Ensure the existence of properly formatted database file “path/database.txt”
#Database format example: “1AXC	B”
#Set active folder: cd <folder path>

#Define function to get surface area of structure
def SASA():
	#Set solvent radius
	SolventRadius = 1.4
	#Calculation Quality (0 = very fast, 5 = very slow, higher accuracy. Default = 2) 
	DotDensity = 3
	
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

	#Loop through states and calculate surface area
	for i in range(0,states):
		total += cmd.get_area("all", i+1)
		polar += cmd.get_area("elem N+O", i+1)
		nonpolar += cmd.get_area("elem C+S", i+1)

	#Find average surface areas
	avg_total = total/states
	avg_polar = polar/states
	avg_nopol = nonpolar/states

	return [avg_total , avg_polar ,avg_nopol]


#Load list of PDB codes and ID chain identifiers
database = “path/database.txt”

print("Loading database...")

with open(database) as f:
	lines = f.readlines()
	
print("Database loaded")
print("Starting calculations...")
print("")

for i in range(0,len(lines)):
	cmd.do("delete all")
	line = lines[i].strip()

	#Get PDB code
	pdbid = line[:4].strip()

	#Fetch molecule
	cmd.fetch(pdbid)

	#Get IDP chain identifier
	disorderedchainref = line[5:].strip()

	#Get IDP sequence and remove chain ID string
	sequence = cmd.get_fastastr("chain " + disorderedchainref)[5:].strip().replace("\n","")

	#Skip the complex if the IDP contains modified or non-standard residues
	if '?' in sequence: continue

	#Filters short IDP chains
	if len(sequence) < 5: continue

	#Get complex surface (SASA defined as Script 1, returns array containing total, polar #and nonpolar surface area)
	surface_complex = SASA()

	#Remove IDP
	cmd.do("remove chain " + str(disorderedchainref))

	#Get folded protein surface
	surface_folded = SASA()

	#Converts values to strings and prints in console (copy to text file to save)
	print(pdbid, sequence, str(surface_folded[0]), str(surface_folded[1]), str(surface_folded[2]), str(surface_complex[0]), str(surface_complex[1]), str(surface_complex[2]))

print("")
print("Calculations completed")
print("Script finished")
