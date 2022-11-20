
from main import bot, dp
from states import Answers
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram import types
from config import admin_id
from aiogram.dispatcher.filters import Command
from locations import cities
from aiogram.dispatcher.storage import FSMContext
import asyncio
from main import loop
import time
from outervariables import Outervariables
from customfunctions import Driverfunc

funcvar = Driverfunc()

async def send_to_admin(dp):
	await bot.send_message(chat_id=admin_id, text="Бот запущен")

@dp.message_handler(commands=['start'])
async def starting(message: Message):
	text = f"Привет, {message.chat.first_name}! В каком городе ты находишься?"
	info = message.message_id, message.from_user.id

	print(info)

	await bot.send_message(chat_id=message.from_user.id, text=text)
	await Answers.usercity.set()

@dp.message_handler(content_types="text", state=Answers.usercity)
async def choice(message: Message, state: FSMContext):
	await state.update_data(usercity=message.text)
	city = message.text.upper()

	from locations import cities
	from customfunctions import Driverfunc

	print(city, cities)

	data = await state.get_data("usercity")
	usercity = data.get("usercity")
	answertext1 = f"Ответ 1 = {usercity}!"

	await funcvar.choicecity(city, cities, message)

	await bot.send_message(chat_id=message.from_user.id, text=answertext1)

@dp.message_handler(content_types="text", state=Answers.userstreet)
async def choicestreet(message: Message, state: FSMContext):
	text2 = f"Проверяем наличие улицы <b>{message.text.upper()},</b> секунду... "
	await message.answer(text=text2, parse_mode=types.ParseMode.HTML)
	await message.answer(text='****', parse_mode=types.ParseMode.HTML)
	time.sleep(1)
	street = message.text


	await state.update_data(userstreet=message.text)
	data = await state.get_data("userstreet")
	userstreet = data.get("userstreet")
	textanswer2 = f"ОТВЕТ 2 = {userstreet}"

	rightcity = data.get("usercity")
	print('RIGHT CITY', rightcity)

	await funcvar.dbasking(rightcity, street, message)



	await bot.send_message(chat_id=message.from_user.id, text=textanswer2)

@dp.message_handler(content_types="text", state=Answers.userradius)
async def choseradius(message: Message, state: FSMContext):
	print ('ИЗ ВНЕШЕЙ В ХЭНДЛЕР', funcvar.results)
	streetcoordinates = funcvar.results[0][3:5]

	await funcvar.selection(streetcoordinates, message)


	userradius = message.text.upper()
	await state.update_data(userradius=message.text)
	data = await state.get_data("userradius")
	userradius = data.get("userradius")
	textanswer3 = f"ОТВЕТ 3 = {userradius}"
	await bot.send_message(chat_id=message.from_user.id, text=textanswer3)




#@dp.message_handler(commands=['exit'], state=Answers.Q1)
#async def closing(message: Message):
#	text = f"До свидания!, {message.chat.first_name}! Напишите /start, чтобы начать поиск снова"
	#info1 = message.text
	#print(info1)
	#await bot.send_message(chat_id=message.from_user.id, text=text)
	#await state.finish()



#@dp.message_handler()
#async def choice(message: Message):
	#city = message.text.upper()
	#from locations import cities
	#from customfunctions import choicecity
	#print(city, cities)
	#await choicecity(city, cities, message, bot)
	#if info in cities:
	#	text1 = f"Вы в <b>{message.text.upper()}</b>"
	#	await message.answer(text=text1, parse_mode=types.ParseMode.HTML)
	#else:
	#	text2 = 'Не найден, введите название города снова или нажмите /exit, чтобы выйти'
	#	print(text2)
	#	await bot.send_message(chat_id=message.from_user.id, text=text2)
