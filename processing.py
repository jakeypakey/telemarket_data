import numpy as np
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
import time
import matplotlib.pyplot as plt
import matplotlib

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
def processImportance(catMap,cols,bunch,dropFirst=False):
	translator = processDict(catMap,dropFirst)[0]
	features = {title:mean for title,mean in zip(cols,bunch['importances_mean'])}

	#now, we must group catagorical variables together to figure out their importnance
	#methodology for combining discussed here:https://stats.stackexchange.com/questions/314567/feature-importance-with-dummy-variables
	for key,value in translator.items():
		if isinstance(value,list):
			#now we re-add in the overall catagory
			#and will sum the importances here
			features[key] = 0
			for suffix in value:
				features[key] += features[key+'_'+suffix]
				features.pop(key+'_'+suffix)
			#take the sqrt of the sum of dummy variables importance's
			features[key] = np.sqrt(features[key])

				
	#back to list for sorting	
	features = [(feature,importance) for feature,importance in features.items()]

	#now list sorted by importance
	featuresByMean = sorted(features, key=lambda key_value: key_value[1],reverse=True)

	#final processing into strings to label visualiztions
	means = [info[1] for info in featuresByMean]

	total = sum(means)

	meanPercentages = [item/total*100 for item in means]

	#get index where cumaltive sum of feature importance is greater/eq to 90%
	cutoff = next(idx for idx, value in enumerate(np.cumsum(meanPercentages)) if (value >= 90))
	
	#get features of minor importance
	rest = meanPercentages[cutoff+1:]

	#reform vectors, combining bottom 10% into 'other'
	meanPercentages = meanPercentages[:(cutoff+1)]
	meanPercentages.append(sum(rest))

	#get rest of labels
	restLabels = [item[0] for item in featuresByMean[cutoff+1:]]

	#get important features
	featuresByMean = [ item[0] for item in featuresByMean[:cutoff+1] ]
	featuresByMean.append('other')


	#significant factors
	meanLabels = [label+" - "+"{:.4f}%".format(perc) for label,perc in zip(featuresByMean,meanPercentages) ]

	#other factos
	rest = [label+" - "+"{:.4f}%".format(perc) for label,perc in zip(restLabels,rest)]

	return (meanLabels,meanPercentages,rest)

def pie(labels,numbers,others,figureNum):
	COLOR = 'black'
	matplotlib.rcParams['text.color'] = COLOR
	matplotlib.rcParams['axes.labelcolor'] = COLOR
	matplotlib.rcParams['xtick.color'] = COLOR
	matplotlib.rcParams['ytick.color'] = COLOR
	plt.figure(figureNum)
	colors = ['yellowgreen','red','gold','lightskyblue','white','lightcoral','blue','pink', 'darkgreen','yellow','grey','violet','magenta','cyan']

	patches, texts = plt.pie(numbers, colors=colors, startangle=90, radius=1.2)

	patches, labels, dummy =  zip(*sorted(zip(patches, labels, numbers),key=lambda x: x[2],reverse=True))

	plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),fontsize=8)

	plt.savefig('piechart{}.png'.format(figureNum), bbox_inches='tight')
	plt.show()
	print('other feautures :')
	for line in others:
		print(line)
