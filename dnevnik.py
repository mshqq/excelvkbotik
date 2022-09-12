from tinydb import TinyDB, Query
db = TinyDB('db.json')
User = Query()

def insert():
	db.insert({"Name": "Олег", "SENDER_ID": "153159"})
	db.insert({"Name": "Михаил", "SENDER_ID": "3634"})
	db.insert({"Name": "Иван", "SENDER_ID": "1524778"})

def search():
	result = db.contains(User['SENDER_ID'] == '3634')
	print(result)

def update():
	db.update({"age": a}, User.name == 'Alex')

def delete():
	db.remove(User.name == "Ivan")

#print(db.all())
#update()
#delete()
print(db.all())
search()