import mysql.connector 
from mysql.connector import Error
import csv
import copy

dictionaryShort = { "age": 0,
		#"job"; - CHAR - ad(M)in, (B)lue-collar, (E)ntrepreneur, (H)ousemaid, (M)anagement, (R)etired, sel(F)-employed, ser(V)ices, (S)tudent, (T)echnician, (U)nemplyed, unknown(?)
		"job": {"admin.": 'M', "blue-collar": 'B', "entrepreneur": 'E', "housemaid": 'H', "management": 'M', "retired": 'R', 
			"self-employed": 'F', "services": 'V', "student": 'S', "technician": 'T', "unemployed": 'U', "unknown": '?'},
		#"marital"; - CHAR -  (D)ivorced, (M)arried, (S)ingle, unknown(?)
		"marital": {"divorced": 'D', "married": 'M', "single": 'S', "unknown": '?'},
		#"education"; - CHAR - (P)rimary, (S)econdary, (T)ertiary, unknown(?)
		"education": {"primary": "P", "secondary": 'S', "tertiary": 'T', "unknown": '?'},
		#"default"; - CHAR - (Y)es, (N)o, unknown(?)
		"default": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"balance"; -  INTEGER
		"balance": 2,
		#"housing"; -  CHAR - (Y)es, (N)o, unknown(?)
		"housing": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"loan"; - CHAR - (Y)es, (N)o, unknown(?)
		"loan":  {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"contact"; - CHAR - (C)ell, (T)elephone, (U)nknown ?
		"contact": {"cellular": 'C', "telephone": 'T', "unknown": '?'},
		#"day"; - TINYINT 
		"day": 0, 
		#"month"; TINYINT - (1-12) <-> (jan-dec)
		"month": {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12},
		#"duration"; - SMALLINT
		"duration": 1,
		#"campaign"; - TINYINT
		"campaign": 0,
		#"pdays"; - SMALLINT
		"pdays": 1,
		#"previous"; - SMALLINT
		"previous": 1,
		#"poutcome"; - CHAR - (S)uccess, (F)ailure, (O)ther, unknown(?)
		"poutcome": {"success": 'S', "failure": 'F', "other": 'O', "unknown": '?'},
		#"y"' - CHAR - (Y)es, (N)o
		"y": {"yes": 'Y', "no": 'N'}}

#This descibes the datatypes/mappings for the data which 
#includes additional fields, and some other differences
#tinyint - 0, smallint - 1, int - 2, float - -1 
#['age; - TINYINT
dictionaryAdditional = { "age": 0,
		#"job"; - CHAR - ad(M)in, (B)lue-collar, (E)ntrepreneur, (H)ousemaid, (M)anagement, (R)etired, sel(F)-employed, ser(V)ices, (S)tudent, (T)echnician, (U)nemplyed, unknown(?)
		"job": {"admin.": 'M', "blue-collar": 'B', "entrepreneur": 'E', "housemaid": 'H', "management": 'M', "retired": 'R', 
			"self-employed": 'F', "services": 'V', "student": 'S', "technician": 'T', "unemployed": 'U', "unknown": '?'},
		#"marital"; - CHAR -  (D)ivorced, (M)arried, (S)ingle, unknown(?)
		"marital": {"divorced": 'D', "married": 'M', "single": 'S', "unknown": '?'},
		#"education"; - CHAR - basic.(4)y, basic.(6)y, basic.(9)y, pro(F)essional.course, (H)igh.school, (U)niversity, (I)lliterate, unknown(?)
		"education": {"basic.4y": '4', "basic.6y": '6', "basic.9y": '9', "professional.course": 'F', "high.school": 'H', 
			"university.degree": 'U', "illiterate": 'I', "unknown": '?'},
		#"default"; - CHAR - (Y)es, (N)o, unknown(?)
		"default": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"housing"; -  CHAR - (Y)es, (N)o, unknown(?)
		"housing": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"loan"; - CHAR - (Y)es, (N)o, unknown(?)
		"loan":  {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"contact"; - CHAR - (C)ell, (T)elephone, (U)nknown ?
		"contact": {"cellular": 'C', "telephone": 'T', "unknown": '?'},
		#"month"; TINYINT - (1-12) <-> (jan-dec)
		"month": {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12},
		#"day_of_week"; - TINYINT 
		"day_of_week": {"mon":1, "tue":2, "wed":3, "thu":4, "fri":5, "sat":6, "sun":7},
		#"duration"; - SMALLINT
		"duration": 1,
		#"campaign"; - TINYINT
		"campaign": 0,

		#NO BALANCE IN THE "ADDITIONAL" DATASET
		#"balance"; -  INTEGER
		#"balance": 2,

		#"pdays"; - SMALLINT
		"pdays": 1,
		#"previous"; - SMALLINT
		"previous": 1,
		#"poutcome"; - CHAR - (S)uccess, (F)ailure, (O)ther, unknown(?), (N)onexistent
		"poutcome": {"success": 'S', "failure": 'F', "other": 'O', "unknown": '?', "nonexistent":'N'},
		#emp.var.rate DECIMAL(3,1)
		"emp.var.rate": -1,
		#cons.price.idx DECIMAL(6,3)
		"cons.price.idx": -1,
		#cons.conf.idx DECIMAL(4,1)
		"cons.conf.idx": -1,
		#euribor3m DECIMAL(5,3)
		"euribor3m": -1,
		#nr.employed DECIMAL(6,1)
		"nr.employed": -1,
		#"y"' - CHAR - (Y)es, (N)o
		"y": {"yes": 'Y', "no": 'N'}}

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
	def getEntries(self,table,indexStart,indexStop):
		cursor = self.connection.cursor()
		queryString = "SELECT * from {} LIMIT {}, {}".format(table,indexStart,indexStop)
		try:
			cursor.execute(queryString)
			return cursor.fetchall()
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
	def loadCsvToDB(self,fileName,dictionary,create_query,insert_query,delimiter):
		with open(fileName) as fi:
			reader = csv.reader(fi,delimiter=delimiter)
			firstRow = True
			#create table
			self.query(create_query)
			#values for entries
			params = []
			for row in reader:
				#get catagories from the first row of the file
				if firstRow:
					#get first line of .csv, the catagories
					catagories = [ item for item in row]
					print("The fields in this file: {}\n".format(catagories))
					firstRow = False
			#process data for following rows
				else:
				#clear current entry
					entry =  [] #process each field according to type
					for i in range(len(catagories)):
						if isinstance(dictionary[catagories[i]],dict):
							entry.append(dictionary[catagories[i]][row[i]])
						elif dictionary[catagories[i]] > 0:
							entry.append(int(row[i]))
						else:
							entry.append(float(row[i]))

						params.append(tuple(entry))
				self.queryMany(insert_query,params)

	#process and 'reverse' dictionaries used to read data in so they can be used by data analyzer
	def getMaps(self):
		#make deep copies, don't mess with data input dicts..
		mapAdditional = copy.deepcopy(dictionaryAdditional)
		mapShort = copy.deepcopy(dictionaryShort)

		#default was removed from the data because it appears to be a SQL keyword
		mapAdditional['isDefault'] = mapAdditional.pop('default')
		mapShort['isDefault'] = mapShort.pop('default')
		#inv_map = {v: k for k, v in my_map.items()}

		for key in mapShort.keys():
			if isinstance(mapShort[key],dict):
				mapShort[key] = {val: ke for ke, val in mapShort[key].items()}

		for key in mapAdditional.keys():
			if isinstance(mapAdditional[key],dict):
				mapAdditional[key] = {val: ke for ke, val in mapAdditional[key].items()}
		return (mapShort,mapAdditional)
			

				

#This descibes the datatypes/mappings for SQL
#tinyint - 0, smallint-1, int-2
#['age; - TINYINT
insertQueryShort = """INSERT INTO people ( age, job, maritial, education, 
isDefault, balance, housing,
loan, contact, day, month,
duration, campaign, pdays,
previous, poutcome, y )
VALUES ( %s, %s, %s, %s, 
				%s, %s, %s, 
				%s, %s, %s, %s, 
				%s, %s, %s, 
				%s, %s, %s  )"""


#database.loadCsvToDB("/Users/jake/proj/data/bank_marketing/bank-full.csv",dictionary,create_query,insert_query,';')



#['age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed', 'y']

createQueryAdditional = """ CREATE TABLE IF NOT EXISTS people_additional (
id INT AUTO_INCREMENT,
age TINYINT,
job CHAR(1),
maritial CHAR(1),
education CHAR(1),
isDefault CHAR(1),
housing CHAR(1),
loan CHAR(1),
contact CHAR(1),
day TINYINT,
month TINYINT,
duration SMALLINT,
campaign TINYINT,
pdays SMALLINT,
previous SMALLINT,
poutcome CHAR(1),
emp_var_rate DECIMAL(3,1),
cons_price_idx DECIMAL(6,3),
cons_conf_idx DECIMAL(4,1),
euribor3m DECIMAL(5,3),
nr_employed DECIMAL(6,1),
y CHAR(1),
PRIMARY KEY (id)) ENGINE = InnoDB
"""

insertQueryAdditional = """INSERT INTO people_additional ( age, job, maritial, education, 
isDefault, housing,
loan, contact, day, month,
duration, campaign, pdays,
previous, poutcome, emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m,
nr_employed, y )

VALUES ( %s, %s, %s, %s, 
%s, %s,  
%s, %s, %s, %s, 
%s, %s, %s, 
%s, %s, %s, 
%s, %s, %s, 
%s, %s  )"""




#items = database.getEntries('people',0,5)


#database = Database("bank_data")
#database.loadCsvToDB("/Users/jake/proj/data/bank_marketing/bank-full.csv",dictionaryShort,createQueryShort,insertQueryShort,';') 
#database.loadCsvToDB("/Users/jake/proj/data/bank_marketing/bank-additional/bank-additional-full.csv",dictionaryAdditional,createQueryAdditional,insertQueryAdditional,';') 
#database.connection.close()

