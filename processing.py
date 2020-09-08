import numpy as np
import pandas as pd
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
				dataProcPeopleAdditional.append(peopleAdditionalIndex)
				peopleAdditionalIndex+=1
			else:
				for ke, val in peopleAdditionalMap[key].items():
					subMap[ke] = peopleAdditionalIndex
					peopleAdditionalIndex+=1
				dataProcPeopleAdditional.append(subMap)

	return (dataProcPeople,dataProcPeopleAdditional)

def generateLabels(peopleMap,peopleAdditionalMap):
	labelsPeople = []
	labelsPeopleAdditional = []

	for key in peopleMap.keys():
		if isinstance(peopleMap[key],int) or key=='month':
			labelsPeople.append(key)
		else:
			if len(peopleMap[key].keys()) == 2:
				labelsPeople.append(key)
			else:
				for ke in peopleMap[key].keys():
					labelsPeople.append(key+':'+peopleMap[key][ke])

	for key in peopleAdditionalMap.keys():
		if isinstance(peopleAdditionalMap[key],int) or key=='month' or key=='day_of_week':
			labelsPeopleAdditional.append(key)
		else:
			if len(peopleAdditionalMap[key].keys()) == 2:
				labelsPeopleAdditional.append(key)
			else:
				for ke in peopleAdditionalMap[key].keys():
					labelsPeopleAdditional.append(key+':'+peopleAdditionalMap[key][ke])

	return (labelsPeople,labelsPeopleAdditional)
	

#use processing vectors to translate into final processing form
def translate(proc,raw,size):
	#first remove ID from vector
	data = np.zeros(size)
	for p,r in zip(proc,list(raw)):
		#raw data is numeric or binary
		if isinstance(p,int):
			#data is numeric
			if not isinstance(r,str):
				data[p] = float(r)
			#data is binary (Y/N)
			elif r=='Y':
				data[p] = 1.0
			#else data[p] = 0
		#raw data is catagorical:encode as one-hot
		else:
			data[p[r]] = 1.0
	return data

#translate numeric data to binary
def numericToBinary(data,index,values,binValue,otherBin):
	data[index] = binValue if data[index] in values else otherBin
	return data

def display(labels,data):
	for label,entry in zip(labels,data):
		print('{} : {}'.format(label,entry))

#get list of fields from SQL, translate to verbose df 
def getDataFrame(entries,proc):
	#preprocess map
	replaceMap = {}
	for key,value in proc.items():
		if isinstance(value,dict):
			replaceMap[key] = value

	#figure out what to do here..
	#if this is a tuple, only one entry
	if isinstance(entries,tuple):
		return entries
		
	df = pd.DataFrame(data=entries,columns=proc.keys())
	return df.replace(replaceMap)

def getOneHot(df,proc):
	replaceMap = {}
	for key,value in proc.items():
		if isinstance(value,dict):
			replaceMap[key] = value

	df = pd.get_dummies(df,columns=replaceMap.keys())
	print(df)


