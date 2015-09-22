from database import *

def main():
	print("OSU")
	db = Database("test.db", debug=True)
	db.connect()
	
	#read tables
	
	print(db.read_table_structure(db.read_table_lists()[1][0]))
	
	#test join
	print(db.create_inner_join(["TABLE_1","TABLE_2"],[["Field1","Field1"],["Field2","Field2"]]))


if __name__ == "__main__":
	main()