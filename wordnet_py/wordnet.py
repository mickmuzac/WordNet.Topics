from nltk.corpus import wordnet as wn
import re

#Live data from the LR... as it turns out, wordnet can't fix bad keywords
#data = [ "Health", "Physical Education", " Education", "federal resources" ];
#data =  [ "Engineering & Design", "Information Technology", "History-Social Science", "Career & Technical Ed", "federal resources" ];
#data = [ "Visual Arts", "Visual Arts & Performing Arts", "Music", "federal resources" ];
#data = ["3DR","Furniture","office","storage","wood cabinet"]
data = ["3DR","Toyota","Pickup","Truck","Civilian","Hilux","Tacoma","Ford","Chevy","GMC","vehicle"];
#data = [ "3DR", "Building", "Buildings", "Structure", "Structures", "Hanger", "Hangers" ];
#data = [ "pbs", "pbs kids", "Teacher Resource", "Science Experiment", "Cat", "Behavior", "Handedness", "Parent Resource", "Experiment", "Math" ];
#data = ["Higher Education","Middle School","Grade 7","Grade 4","Grade 5","Computational Science","Grade 8","Grade 9","Upper Elementary","High School","Grade 10","Grade 11","Grade 12","English","Grade 6","Elementary School","Physics"]
#data = ["Atmospheric Science","Higher Education","Graduate/Professional","English"]
#data = ["Grade 3","EN","Grade 6","Grade 7","Grade 4","Grade 5","Grade 8","Upper Elementary","Elementary School","Middle School"]
#data = ["research","US Department of Ed"]
#data = ["United States History","Geography","History-Social Science","Immigration and Migration","Science","Early Explorers","Earth & Space Science","federal resources"]
#data = ["United States History","History-Social Science","Early Explorers","federal resources"]
#data = "Lewis and Clark offers maps manuscripts timelines and photos related to the famed expedition.  It includes resources for learning about Meriwether Lewis Sacagawea Congress role in the Louisiana Purchase and Thomas Jeffersons life-long commitment to western exploration".split()

'''data = [ "Botany", "for", "Kids", "offers", "activities", "for", "learning", "how", "leaves", "change", "color", "how", "flowers", "grow", "how", "plant", "fight", 
	"disease", "and", "insects", "why", "plants", "come", "in", "so", "many", "colors", "tips", "for", "growing", "various", "plant", "and", "facts", 
	"about", "fungi", "Learn", "about", "seeds", "composting", "endangered", "plant", "species", "fire", "lichen", "and", "plant", "hunters", 
	"scientists", "who", "collect", "plant", "samples", "from", "around", "the", "world", "to", "trace", "a", "plant", "evolution" ];'''

a = []
allSyns = []

#Replace terms with something more meaningful (ed leads to undesirable results ... trust me)
replaceDict = {"ed" : "education", "en" : "english"}

for x in data:
	x = re.findall(r'[a-zA-Z]+', x)
	for s in x:
		
		#Replace terms with a more correct entry
		if(replaceDict.has_key(s.lower())):
			s = replaceDict[s.lower()]
			
		if s not in a:
			a.append(s)

			
#May need to refactor.. do we want all synsets for a particular word, or just one?
similarScore = 0
ultimateSyn = None

for newVar in a:

	test = wn.synsets(newVar, wn.NOUN)
	if(test and test[0] not in allSyns):
		allSyns.append(test[0])
	#for depth in test:
		#allSyns.append(depth)
	
#Get the synset that has the highest similarity with all of the other words...
hypernymScore = 0
similarScore = 0.1
temp = None
hyperSyn = None
similarSyn = []
ultimateSyn = []
start = 0

for similar in allSyns[:-1]:
	start = start + 1
	for inner in allSyns[start:]:
		#print str(similar) + " -> " + str(inner)
		if(inner != similar):

			#Determine which two synsets has the greatest path_similarity
			if(similarScore <= inner.path_similarity(similar)):
				similarScore = inner.path_similarity(similar)
				similarSyn = []
				similarSyn.append(inner)
				similarSyn.append(similar)
			
			#Determine the best hypernym to use
			temp = inner.lowest_common_hypernyms(similar)
			for common in temp:
				if(common.max_depth() >= hypernymScore):
					hypernymScore = common.max_depth();
					hyperSyn = common;
						
#Get specific synset from similar path..
newScore = 0
for getBest in similarSyn:
	if(getBest.max_depth() > newScore):
		newScore = getBest.max_depth()
		ultimateSyn = []
		ultimateSyn.append(getBest)
	elif(getBest.max_depth() == newScore):
		ultimateSyn.append(getBest)

print "The best synset via hypernyms is: " + str(hyperSyn) + " with a depth of " + str(hypernymScore) 
print "The best synset via path similarity is: " + str(ultimateSyn) + " with a depth of " + str(newScore)  + "\n"
print "Out of these similar synsets: " + str(similarSyn) 

#print inspect.getmembers(hyperSyn, predicate=inspect.ismethod)