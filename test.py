import psycopg2

conn = psycopg2.connect(database='postgres',
                        host='localhost',
                        user='postgres',
                        password='1002',
                        port='5432')
#establishing the connection
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database mydb''';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")

#Closing the connection
conn.close()