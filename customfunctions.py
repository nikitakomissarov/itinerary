from handlers import bot, dp
from handlers import Message
from handlers import Command
from handlers import cities
from handlers import types
from states import Answers
from aiogram.dispatcher.storage import FSMContext
from main import loop
from outervariables import Outervariables

class Driverfunc:
	defvar = ''

	def __init__(self, results='РЕЗАЛТПУСТО', city='СИТИПУСТО'):
		self.results = results
		self.city = city
		self.defvar = city

	async def choicecity(self, city, cities, message):
		print("gorod", city)
		if city not in cities:
			text1 = 'Не найден, введите название города снова или нажмите /exit, чтобы выйти'
			print(text1)
			await message.answer(text=text1, parse_mode=types.ParseMode.HTML)
			await Answers.usercity.set()


		else:
			text1 = f"Вы в <b>{message.text.upper()}</b>. Какая улица - ближайшая к вам?"
			await message.answer(text=text1, parse_mode=types.ParseMode.HTML)
			await Answers.userstreet.set()
			self.defvar = city
			print('dflskdflsd', self.defvar)


	async def dbasking(self, rightcity, street, message):
		import MySQLdb
		db = MySQLdb.connect(host="localhost",  # your host, usually localhost
						 user="root",  # your username
						 passwd="1234",  # your password
						 db="mydb")  # name of the data base
		cur = db.cursor()
	# Use all the SQL you like

		sqlstreet = "SELECT mydb.streets.id, prestreet, streets.name, latitude, longitude, CITIES_id FROM mydb.streets RIGHT OUTER JOIN mydb.cities ON mydb.streets.CITIES_id = (SELECT mydb.cities.id FROM mydb.cities WHERE mydb.cities.name  = '%s') WHERE mydb.streets.name = '%s' LIMIT 1" % (
			rightcity, street)
		cur.execute(sqlstreet)
		results = cur.fetchall()
		print(results)

		if results == ():
			messagestreet = ("Улица не найдена")
			await bot.send_message(chat_id=message.from_user.id, text=messagestreet)
			await Answers.userstreet.set()
		else:
			messagestreet = 'Улица ' + str(results[0][2]) + ' найдена! В каком радиусе ищем достопримечательности?'
			await bot.send_message(chat_id=message.from_user.id, text=messagestreet)
			await Answers.userradius.set()
			self.results = results
			print('Внешняя функция', self.results, 'DEFVAR')

	async def selection(self, streetcoordinates, message):
		import MySQLdb
		db = MySQLdb.connect(host="localhost",  # your host, usually localhost
							 user="root",  # your username
							 passwd="1234",  # your password
							 db="mydb")  # name of the data base
		cur = db.cursor()

		sqlattractions = "SELECT * FROM mydb.attractions WHERE ABS((attractions.latitude) - '%s') AND ABS((attractions.longitude)- '%s') <= 0.01" % (
		streetcoordinates[0], streetcoordinates[1])
		cur.execute(sqlattractions)
		results = cur.fetchall()
		print(results)










''' @dp.message_handler(content_types="text")
async def choosethenearest(message, results):
	streetcoordinates = results[0][3:5];
	print(type(results)), print(streetcoordinates[0]);
	print(streetcoordinates[1]);
	sqlattractions = "SELECT * FROM mydb.attractions WHERE ABS((attractions.latitude) - '%s') AND ABS((attractions.longitude)- '%s') <= 0.01" % (
	streetcoordinates[0], streetcoordinates[1])
	cur.execute(sqlattractions)
	results = cur.fetchall();
	print(results) '''
















