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

	def loadCsvToDB(self,dbName,fileName):
		with open(fileName) as fi:
			reader = csv.reader(fi,delimiter=';')
      #get first line of .csv, the catagories
			firstRow = True
      #['age;"job";"marital";"education";"default";"balance";"housing";"loan";"contact";"day";"month";"duration";"campaign";"pdays";"previous";"poutcome";"y"']
      #['58;"management";"married";"tertiary";"no";2143;"yes";"no";"unknown";5;"may";261;1;-1;0;"unknown";"no"']
			for row in reader:
				if firstRow:
					print(row)
					catagories = [ item for item in row]
          #remove trailing semicolon character from strings
					firstRow = False
				else:
					print(catagories)
					print(row)
					break
        
        



database = Database()
database.loadCsvToDB(None,"/Users/jake/proj/data/bank_marketing/bank-full.csv")
