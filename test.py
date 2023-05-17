import mysql.connector
db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="wwoorrlldD1",
    database="testdatabase"
)
mycursor=db.cursor()
mycursor.execute(" DROP TABLE god")
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)