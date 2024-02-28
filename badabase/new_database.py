import mysql.connector

mydb = mysql.connector.connect(
  host="cs1.ucc.ie",
  user="facialrecognition2024",
  password="caipu",
  database="facialrecognition2024"
)

mycursor = mydb.cursor()
'''
Show the databases to connect to the facial recognition 1

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)
'''

#created a table where we will add their name and their percentage
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), percentage INT(255))")
'''
Inserted a new row to make sure the table works before adding any of the code
sql = "INSERT INTO customers (name, percentage) VALUES (%s, %s)"
val = ("Elena", 85 )
mycursor.execute(sql, val)
mydb.commit()

print(mycursor.rowcount, "record inserted.")
'''

#show all the rows in the table
mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
