import numpy as np
#use information from dictionaries used to process data to
#genereate translation vectors which allow catagorical
#things to be translated into one hot vectors

def generateProcMaps(peopleMap,peopleAdditionalMap):
	peopleIndex = 0
	dataProcPeople = []
	dataProcPeopleAdditional = []
	for key in peopleMap.keys():
		if isinstance(peopleMap[key],int) or key=='month':
			dataProcPeople.append(peopleIndex)
			peopleIndex+=1
		else:
			subMap = {}
			if len(peopleMap[key].keys()) == 2:
				dataProcPeople.append(peopleIndex)
				peopleIndex+=1
			else:
				for ke, val in peopleMap[key].items():
					subMap[ke] = peopleIndex
					peopleIndex+=1
					dataProcPeople.append(subMap)
            
	peopleAdditionalIndex = 0
	for key in peopleAdditionalMap.keys():
		if isinstance(peopleAdditionalMap[key],int) or key=='month' or key=='day_of_week':
			dataProcPeopleAdditional.append(peopleAdditionalIndex)
			peopleAdditionalIndex+=1
		else:
			subMap = {}
			if len(peopleAdditionalMap[key].keys()) == 2:
				dataProcPeopleAdditional.append(peopleIndex)
				peopleAdditionalIndex+=1
			else:
				for ke, val in peopleAdditionalMap[key].items():
					subMap[ke] = peopleAdditionalIndex
					peopleAdditionalIndex+=1
					dataProcPeopleAdditional.append(subMap)
	peopleIndex-=1
	peopleAdditionalIndex-=1
	return (dataProcPeople,dataProcPeopleAdditional,peopleIndex,peopleAdditionalIndex)

#use processing vectors to translate into final processing form
def translate(proc,raw,size):
	vector = np.zeros(size)
	
