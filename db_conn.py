import pymysql

db = pymysql.connect("localhost","temp","123456","anime")

cursor = db.cursor()

cursor.execute("select * from user")

data = cursor.fetchone()

print(data)

db.close()