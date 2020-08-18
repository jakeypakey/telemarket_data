import mysql.connector 
from mysql.connector import Error
import csv


class Database:
	def __init__(self):
		self.connection = self.connectToDB("localhost","root","acidrain","bank_data")

	def connectToDB(self,host,user,password,database=None):
		connection = None
		try:
			connection = mysql.connector.connect(host=host,user=user,passwd=password)
			print("Connected to db.")
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

  #this has not been checked
	def query(self,queryString):
		cursor = self.connection.cursor()
		try:
			cursor.execute(queryString)
			connection.commit()
			print(queryString)
		except Error as e:
 			print("Error {} occured.".format(e))

	def queryMany(self,string,parameters):
		cursor = self.connection.cursor()
		try:
			#cursor.executemany(string,parameters)
			#connection.commit()
			print("{} with {} parameters".format(string,len(parameters)))
		except Error as e:
 			print("Error {} occured.".format(e))


	#Parse, clean and 'compress' data for storage in db
	def loadCsvToDB(self,dbName,fileName):
		#This descibes the datatypes/mappings for SQL
		#tinyint - 0, smallint-1, int-2
  	#['age; - TINYINT
		dictionary = { "age": 0,
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
		#"previous"; - TINYINT
		"previous": 0,
		#"poutcome"; - CHAR - (S)uccess, (F)ailure, (O)ther, unknown(?)
		"poutcome": {"success": 'S', "failure": 'F', "other": 'O', "unknown": '?'},
		#"y"' - CHAR - (Y)es, (N)o
		"y": {"yes": 'Y', "no": 'N'}}

		create_query = """ CREATE TABLE IF NOT EXISTS entries (
											 id INT AUTO_INCREMENT,
											 age TINYINT,
											 job CHAR(1),
											 maritial CHAR(1),
											 education CHAR(1),
											 isDefault CHAR(1),
											 balance INT,
											 housing CHAR(1),
											 loan CHAR(1),
											 contact CHAR(1),
											 day TINYINT,
											 month TINYINT,
											 duration SMALLINT,
											 campaign TINYINT,
											 pdays SMALLINT,
											 previous TINYINT,
											 poutcome CHAR(1),
											 y CHAR(1),
											 PRIMARY KEY (id)) ENGINE = InnoDB
											 """
		#sql = "INSERT INTO likes ( user_id, post_id ) VALUES ( %s, %s )"
		insert_query = """INSERT INTO entries ( age, job, maritial, education, 
																						isDefault, balance, housing,
																						loan, contact, day, month,
																						duration, campaign, pdays,
																						previous, poutcome, y )
																	 VALUES ( %d, %c, %c, %c, 
																	 					%c, %d, %c, 
																						%c, %c, %d, %d, 
																						%d, %d, %d, 
																						%d, %d, %c,  )"""
		with open(fileName) as fi:
			reader = csv.reader(fi,delimiter=';')
			firstRow = True

			self.query(create_query)
			#values for entries
			params = []
	
			count = 0
			for row in reader:
				#get catagories from the first row of the file
				if firstRow:

      		#get first line of .csv, the catagories
					catagories = [ item for item in row]



					firstRow = False
				#process data for following rows
				else:
					#print("ROW: {}".format(count))
					#clear current entry
					entry =  []
					#process each field according to type
					for i in range(len(catagories)):
						if isinstance(dictionary[catagories[i]],dict):
							entry.append(dictionary[catagories[i]][row[i]])
						else:
							entry.append(int(row[i]))

					params.append(tuple(entry))
				count+=1
			self.queryMany(insert_query,params)
        
        



database = Database()
database.loadCsvToDB(None,"/Users/jake/proj/data/bank_marketing/bank-full.csv")
