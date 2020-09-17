import numpy as np
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import time

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


##WARNING##
##use independent=True to drop a single one-hot col for each catagory
def getOneHot(df,proc,dropFirst=False):
	replaceMap,binaryRep = processDict(proc,dropFirst)

	#handle binary values
	df = df.replace(binaryRep)

	for key in replaceMap.keys():
		#form up catagorical one hots
		temp = df[key].astype(pd.CategoricalDtype(replaceMap[key]))
		#get dummie variables for catagory
		temp =	pd.get_dummies(temp,prefix=key)
		#get the location of the temp category to maintain order
		tempLoc = df.columns.get_loc(key)
		#drop the old string formatted category
		df = df.drop(key,axis='columns')
		#insert colukmns back in
		for col in reversed(temp.columns):
			df.insert(tempLoc,col,temp[col])

	#pdays is usally a null value of (-1 or 999) or a small integer,
	#switch this to binary 
	df.loc[((df['pdays']!=999) & (df['pdays']!=-1)) ,'pdays'] = 1
	df.loc[(df['pdays']!=1),'pdays'] = 0

	return df

def processDict(dictionary,dropFirst=False):
	binaryRep = {}
	replaceMap = {}
	for key,value in dictionary.items():
		if isinstance(value,dict):
			#if dropFirst, and the catagory is not already binary
			if dropFirst and not value=={'Y': 'yes', 'N': 'no'}:
				print('dropped: {}'.format(value.popitem()))
			#if the value is not binary, add catagories
			if not value == {'Y': 'yes', 'N': 'no'}:
				replaceMap[key] = list(value.values())
			#if the value is binary, use single vector
			else: 
				binaryRep[key] = {'yes': 1, 'no': 0}
	return (replaceMap,binaryRep)



#this function verifies that all values in the dictionary/dataframe are taken
#and that no values have not been accounted for
#this function fails if:
#1)there is a key remaining in the dictionary after a pass (value not taken) OR
#2)a unexpected value is encountered (key error will be raised)
def validate(df,dictionary):
	dictionary,binaryRep = processDict(dictionary)
	for category in dictionary.keys():
		if isinstance(dictionary[category],dict):
			dictSet = set(dictionary[category].values())
			inData = set(df[category].unique())
			if not dictSet == inData:
				if len(dictSet) > len(inData):
					print("Value(s): {} occur in DataFrame but NOT IN DATASET.".format(dictSet-inData))
				else:
					print("Value(s): {} occur in dataset but NOT IN DATAFRAME.".format(inData-dictSet))
				return False
	return True

def setupLog():
	if not 'my_logger' in logging.Logger.manager.loggerDict.keys():
		logger = logging.getLogger('my_logger')
		handler = RotatingFileHandler('./logs/info.log', maxBytes=20000, backupCount=20)
		logger.addHandler(handler)
		logger.setLevel(logging.INFO)
		logger.info('Kernel initialized')
		logger.info(time.strftime("%D;%H:%M:%S",time.localtime()))
		logger.info('------------------')
	else:
		logger = logging.getLogger('my_logger')
	return logger

#catMaps - map for organizing catagorical variables
#titles - axis titles
#bunches - bunches returned from sci-kit permutation_importance
def processImportance(catMaps,titles,bunches,dropFirst=False):
	#variables with A append are for the extended dataset
	#unpack variables
	cols = titles[0]
	colsA = titles[1]

	bunch = bunches[0]
	bunchA = bunches[1]

	translator = processDict(catMaps[0],dropFirst)[0]
	translatorA = processDict(catMaps[1],dropFirst)[0]

	features = {title:mean for title,mean in zip(cols,bunch['importances_mean'])}
	featuresA = {title:mean for title,mean in zip(colsA,bunchA['importances_mean'])}

	#group for loop
	translators = (translator,translatorA)
	featuresz = (features,featuresA)

	#mapShort[key] = {val: ke for ke, val in mapShort[key].items()}




	#TODO: IMPLEMENT FOR THE Addiciotnal, also test
	for translator, features in zip(translators,featuresz):
		print(translator)
		for key,value in translator.items{}:
			if isinstance(value,list):
				#now we re-add in the overall catagory
				#and will sum the importances here
				features[key] = 0
				for suffix in value:
					features[key] += features[key+'_'+suffix]
					features.pop(key+'_'+suffix)
				features[key] = np.sqrt(features[key])

				
			
	print(features)

	#get dicts that only include needed variables


	#now, we must group catagorical variables together to figure out their importnance
	#methodology for combining discussed here:https://stats.stackexchange.com/questions/314567/feature-importance-with-dummy-variables



	
	#extract features and their relative importance




	featuresByMean = sorted(features, key=lambda key_value: key_value[1],reverse=True)
	featuresByMeanA = sorted(featuresA, key=lambda key_value: key_value[1],reverse=True)




	means = [info[1] for info in featuresByMean]
	total = sum(means)
	#print(total)
	meanPercentages = [ item/total*100 for item in means ]
	meanLabels = [str(info[0])+" - "+"{:.4f}%".format(perc) for info,perc in zip(featuresByMean,meanPercentages)]

	return None
