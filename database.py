from sqlite3 import *
import os
import inspect

class Database():
	""" class to handle a database this class MUST implement __init__ """
	def __init__(self, name, debug = True):
		# Connect to an access database using pyodbc
		self.debug = debug
		self.dbname = name

	def __del__(self):
		""" disconnect properly from database """
		self.disconnect()

	def connect(self):
		""" connect to a database """
		if (self.debug):
			print("Connecting to " + os.path.abspath(self.dbname))
		try:
			#Try to connect to db
			self.cnx = connect(os.path.abspath(self.dbname))
			print("Connection to db " + self.dbname + " successfull")

		except:
			print("Connection to db " + self.dbname + " failed")

	def disconnect(self):
		""" disconnect from a database """
		try:
			self.cnx.close()
			print("Connection to database " + self.dbname + " closed")
		except:
			pass


	def execute_query(self, query):
		"""retrieve values within db return a list containing all the informations """
		try:
			cursor = self.cnx.cursor()
			#execute the SQL change
			if self.debug == True:
				print("Executing following SQL command : " + query + "on db :" + self.dbname)
			lines = cursor.execute(query)
			data = cursor.fetchall()
			return data
		except:
			if self.debug == True:
				print("Error executing : " + query + " on db :" + self.dbname)
			return "Error"


	def commit_query(self, SQLquery):
		""" Commiting change a SQL query"""
		try:
			cursor = self.cnx.cursor()
			#execute the SQL change
			if self.debug == True:
				print("Executing following SQL command : " + SQLquery + " on db : " + self.dbname)
			cursor.execute(SQLquery)
			#commit change in db
			self.cnx.commit()
			return 0
		except:
			self.cnx.rollback()
			if self.debug == True:
				print("Error executing : " + SQLquery + " on db : " + self.dbname)
			return 1

	def define_function(self, function_name, function):
		""" include function inside the database """
		""" need positional argument in function only """
		self.cnx.create_function(function_name, len(inspect.signature(function).parameters), function)
