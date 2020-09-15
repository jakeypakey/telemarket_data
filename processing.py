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

