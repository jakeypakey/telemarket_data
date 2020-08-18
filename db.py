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
		cursor = connection.cursor()
		try:
			cursor.execute(queryString)
			connection.commit()
			print(queryString)
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
		with open(fileName) as fi:
			reader = csv.reader(fi,delimiter=';')
			firstRow = True


	
      #['58;"management";"married";"tertiary";"no";2143;"yes";"no";"unknown";5;"may";261;1;-1;0;"unknown";"no"']
			count = 0
			for row in reader:
				if firstRow:
					print(row)
      		#get first line of .csv, the catagories
					catagories = [ item for item in row]
					firstRow = False
				else:
					print("ROW: {}".format(count))
					for i in range(len(catagories)):
						print('catagory: {}'.format(catagories[i]))
						if isinstance(dictionary[catagories[i]],dict):
							print(dictionary[catagories[i]][row[i]])
						else:
							print(int(row[i]))
				count+=1
        
        



database = Database()
database.loadCsvToDB(None,"/Users/jake/proj/data/bank_marketing/bank-full.csv")
