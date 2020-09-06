import mysql.connector 
from mysql.connector import Error
import csv
import copy
import pandas as pd
from sql_strings import dictionaryAdditional, createQueryAdditional, \
		insertQueryAdditional, dictionaryShort, createQueryShort, insertQueryShort


class Database:
    ##TODO: return infromation about tables available, (dictionary which {table_name :{fields[...]}}
	def __init__(self,name):
		self.connection = self.connectToDB("localhost","root","acidrain","bank_data")
		cursor = self.connection.cursor()
		queryString = "USE {}".format(name)
		try:
			cursor.execute(queryString) 
			self.connection.commit()
			print(queryString)
		except Error as e:
			print("Error {} occured.".format(e))
			self.createDB(name)
			self.query(queryString)


	def connectToDB(self,host,user,password,database=None):
		connection = None
		try:
			connection = mysql.connector.connect(host=host,user=user,passwd=password)
			print("Connected to db\nSuccessful SQL commands are printed on execution.")
		except Error as e:
			print("Error: {} occured.".format(e))
		return connection

	def createDB(self,name):
		cursor = self.connection.cursor()
		try:
			cursor.execute("CREATE DATABASE {}".format(name))
			print("Database created.")
		except Error as e:
			print("Error {} occured.".format(e))

	def query(self,queryString):
		cursor = self.connection.cursor()
		try:
			cursor.execute(queryString)
			self.connection.commit()
			print(queryString)
		except Error as e:
			print("Error {} occured.".format(e))

	def queryMany(self,string,parameters):
		cursor = self.connection.cursor()
		try:
			cursor.executemany(string,parameters)
			self.connection.commit()
			print("{} with {} parameters".format(string,len(parameters)))
		except Error as e:
			print("Error {} occured.".format(e))

    #get entries on [indexStart,indexStop)
		#specify if ID needed (programmer imposed keys for DB)

	def getEntries(self,table,indexStart,indexStop,inclID=False):
		cursor = self.connection.cursor()
		queryString = "SELECT * from {} LIMIT {}, {}".format(table,indexStart,indexStop)
		try:
			cursor.execute(queryString)
			#do not use list form if single entry
			if (indexStop-indexStart) == 1:
				if inclID:
					return cursor.fetchall()[0]
				else:
					return cursor.fetchall()[0][1:]
			else:
				if inclID:
					return cursor.fetchall()[0]
				else:
					#exclude IDs and return
					return [ entry[1:] for entry in cursor.fetchall() ]
		except Error as e:
			print("Error {} occured.".format(e))

	def getSize(self,table):
		cursor = self.connection.cursor()
		queryString = "SELECT COUNT(*) FROM {}".format(table)
		try:
			cursor.execute(queryString)
			return cursor.fetchall()[0][0]
		except Error as e:
			print("Error {} occured.".format(e))
	
    #get entries from from field list on [indexStart,indexStop)
		#pass either a single field, or list (len at least 2) of fields 
	def getEntriesByField(self,table,indexStart,indexStop,fieldList):
		cursor = self.connection.cursor()
		# SELECT y, isDefault FROM people LIMIT 0, 2;
		if isinstance(fieldList,list):
			if len(fieldList) > 1:
				queryString = "SELECT {} from {} LIMIT {}, {}".format(", ".join(fieldList),table,indexStart,indexStop)
			else:
				print('Pass single fields to getEntriesByField as the field itself, not in a list.')
				return -1
		else:
			queryString = "SELECT {} from {} LIMIT {}, {}".format(fieldList,table,indexStart,indexStop)
		try:
			cursor.execute(queryString)
			items = cursor.fetchall()
			if isinstance(fieldList,list):
				return items
			else:
				return [item[0] for item in items]
		except Error as e:
			print("Error {} occured.".format(e))
		
	#create table, load data in and convert verbose fields to CHAR to save space	
	def loadCsvToDB(self,fileName,dictionary,delimiter,insertQuery,createQuery=None,chunkSize=1000):
		#create dictionary that only has strings which require character mapping for pd.replace()
		csvDict = {}
		for key,value in dictionary.items():
			if isinstance(value,dict):
				csvDict[key] = value
		#create the table if needed
		if not createQuery == None:
			self.query(createQuery)
		#process chunkwise
		for chunk in pd.read_csv(fileName,chunksize=chunkSize,delimiter=';'):
			#dataframe now a lsit for insertion to database
			chunk = chunk.replace(csvDict)
			self.queryMany(insertQuery,[tuple(entry) for entry in chunk.values])


	#process and 'reverse' dictionaries used to read data in so they can be used by data analyzer
	def getMaps(self):
		#make deep copies, don't mess with data input dicts..
		mapAdditional = copy.deepcopy(dictionaryAdditional)
		mapShort = copy.deepcopy(dictionaryShort)



		for key in mapShort.keys():
			if isinstance(mapShort[key],dict):
				mapShort[key] = {val: ke for ke, val in mapShort[key].items()}

		#reorder to reflect original ordering, change default to reflect database
		mapShort = dict( ('isDefault', v) if k == 'default' else (k, v) for k, v in mapShort.items() )

		for key in mapAdditional.keys():
			if isinstance(mapAdditional[key],dict):
				mapAdditional[key] = {val: ke for ke, val in mapAdditional[key].items()}

		#reorder to reflect original ordering, change default to reflect database
		mapAdditional = dict( ('isDefault', v) if k == 'default' else (k, v) for k, v in mapAdditional.items() )
		return (mapShort,mapAdditional)
			

				





#items = database.getEntries('people',0,5)
database = Database("bank_data")
#preprocess dict to only contain needed items

database.loadCsvToDB("/Users/jake/proj/data/bank_marketing/bank-full.csv",dictionaryShort,';',insertQueryShort,createQueryShort) 

database.loadCsvToDB("/Users/jake/proj/data/bank_marketing/bank-additional/bank-additional-full.csv",dictionaryAdditional,';',insertQueryAdditional,createQueryAdditional) 
#database.connection.close()

