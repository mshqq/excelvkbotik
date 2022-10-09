#импортируем библиотеки и зависимости
from calendar import TUESDAY
from operator import mod
from tokenize import triple_quoted
from typing_extensions import Self
import vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import datetime
import os
import httplib2
import pytz
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import creds
import json
import asyncio
import schedule
import time
import random
import threading
import requests
import sqlite3

import creds

#функции Google API Service
def get_service_simple():
    return build('sheets', 'v4', developerKey=creds.api_key)

def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/creds/sacc1.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

#объяеляем Google Sheet
service = get_service_sacc()
sheet = service.spreadsheets()
sheet_id = "149qpJ-f7C8mWSMqpzsGTjoFqs1U4ANK6GClNvvw4iRc"

#подключаем vk_api
vk_session = vk_api.VkApi(
token='vk1.a.6s7T854sQ9SJXCfyl2_Q2iofR9LWyVEcSungdfDsm0328JNfiIFhrJfTnipIm5gefZWyaIqOo4mL4EbDQkrlCgUY76aoifQmsu4p67yz_BHtSSLtahOfe6Kqzlg_6MflFyXoYYqpyW9SsL_UDTrt9iIUaULWFXi01bcSNYfuTZpnpPGtLo9Ts2XSqbEFY8pt')
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

#объявляем клавиатуру главного меню без рассылки
keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Завтра', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Выбор по дню недели', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Выбор класса', color=VkKeyboardColor.PRIMARY)

#объявляем клавиатуру главного меню с рассылкой
keyboardSub = VkKeyboard(one_time=True)
keyboardSub.add_button('Подписаться на рассылку', color=VkKeyboardColor.POSITIVE)
keyboardSub.add_line()
keyboardSub.add_button('Отписаться от рассылки', color=VkKeyboardColor.NEGATIVE)
keyboardSub.add_line()
keyboardSub.add_button('Меню', color=VkKeyboardColor.PRIMARY)

#объяеляем клавиатуру выбора дня недели
keyboardDayOfTheWeek = VkKeyboard(one_time=True)
keyboardDayOfTheWeek.add_button('Понедельник', color=VkKeyboardColor.PRIMARY)
keyboardDayOfTheWeek.add_line()
keyboardDayOfTheWeek.add_button('Вторник', color=VkKeyboardColor.PRIMARY)
keyboardDayOfTheWeek.add_line()
keyboardDayOfTheWeek.add_button('Среда', color=VkKeyboardColor.PRIMARY)
keyboardDayOfTheWeek.add_line()
keyboardDayOfTheWeek.add_button('Четверг', color=VkKeyboardColor.PRIMARY)
keyboardDayOfTheWeek.add_line()
keyboardDayOfTheWeek.add_button('Пятница', color=VkKeyboardColor.PRIMARY)
keyboardDayOfTheWeek.add_line()
keyboardDayOfTheWeek.add_button('Суббота', color=VkKeyboardColor.PRIMARY)

keyboardClassChoice = VkKeyboard(one_time=True)
keyboardClassChoice.add_button('5А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('5Б', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('5В', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('5Г', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_line()
keyboardClassChoice.add_button('6А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('6Б', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('6В', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_line()
keyboardClassChoice.add_button('7А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('7Б', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('7В', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('7Г', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_line()
keyboardClassChoice.add_button('8А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('8Б', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('8В', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('8Г', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_line()
keyboardClassChoice.add_button('9А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('9Б', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('9В', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('9Г', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_line()
keyboardClassChoice.add_button('10А', color=VkKeyboardColor.PRIMARY)
keyboardClassChoice.add_button('11А', color=VkKeyboardColor.PRIMARY)

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

class bot:
    def main(self):

        week_names = [
            'понедельник',
            'вторник',
            'среду',
            'четверг',
            'пятницу',
            'субботу'
        ]

        def emptiness_day():
            vk.messages.send(
                user_id=event.user_id,
                message="Выходной день",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )

        def day_week(self):
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            return today.isoweekday()

        def get_timedata(self, day, letterOfTheClass):
            weekOfTheDay = day
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            if weekOfTheDay == 1:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}3:{letterOfTheClass}13").execute()
            if weekOfTheDay == 2:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}14:{letterOfTheClass}24").execute()
            if weekOfTheDay == 3:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}25:{letterOfTheClass}35").execute()
            if weekOfTheDay == 4:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}36:{letterOfTheClass}46").execute()
            if weekOfTheDay == 5:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}47:{letterOfTheClass}57").execute()
            if weekOfTheDay == 6:
                timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C58:C35").execute()
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}58:{letterOfTheClass}68").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text2 = '\n\nХорошего дня!'
                res ='\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            return res

        def get_today(self, user_id):
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%d.%m.%Y")
            day = day_week(self)
            letterForUser, letterOfTheClass = checkUserClass(user_id)
            if int(day) > 6:
                emptiness_day()
            text = f'Расписание {letterForUser} на сегодня {today}:\n\n'
            res = text + get_timedata(self, day, letterOfTheClass)
            try:
                send_message(message=res)
            except:
                error_message()

        def get_tomorrow(self, user_id):
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            tomorrow = today + datetime.timedelta(days=1)
            day = day_week(self) + 1
            letterForUser, letterOfTheClass = checkUserClass(user_id)
            if int(day) > 6:
                day = 1
            text = f'Расписание {letterForUser} на завтра {tomorrow.strftime("%d.%m.%Y")}:\n\n'
            res = text + get_timedata(self, day, letterOfTheClass)
            try:
                send_message(message=res)
            except:
                error_message()

        def get_day_timetable(self, day, user_id):
            letterForUser, letterOfTheClass = checkUserClass(user_id)
            text = f'Расписание {letterForUser} на {week_names[day - 1]}:\n\n'
            res = text + get_timedata(self, day, letterOfTheClass)
            
            try:
                send_message(message=res)
            except:
                error_message()

        def send_message(message):
            vk.messages.send(
                    user_id=event.user_id,
                    message=message,
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard()
            )
        def unknown_message():
            vk.messages.send(
                user_id=event.user_id,
                message="Не понимаю вашу команду!\nВозвращаю клавиатуру...",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        def error_message():
            vk.messages.send(
                user_id=event.user_id,
                message="Не удалось получить расписание на этот день!\nВозвращаю клавиатуру...",
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )

        def userInfo():
            us_id = event.user_id
            user_get=vk.users.get(user_ids = (event.user_id))
            user_get=user_get[0]
            us_name = user_get['first_name']
            us_sname = user_get['last_name']
            us_class = "11А"
            sub = False
            return us_id, us_name, us_sname, us_class, sub;

        def registerUser(user_id: int, user_name: str, user_surname: str, user_class: str, sub: bool):
            cursor.execute('INSERT INTO ExcelVKBot (user_id, user_name, user_surname, user_class, sub) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, user_class, sub))
            conn.commit()

        def updateUser(user_id: int, user_class: str):
            cursor.execute('UPDATE ExcelVKBot SET user_class =? WHERE user_id =?', (user_class, user_id))
            conn.commit()

        def existsUser():
            info = cursor.execute('SELECT * FROM ExcelVKBot WHERE user_id=?', (event.user_id, ))
            if info.fetchone() is None: 
                return False
            else:
                return True

        def checkUserClass(user_id):
            userClass = cursor.execute('SELECT * FROM ExcelVKBot WHERE user_id=?', (user_id, ))
            classs = cursor.fetchall()
            if classs[0][4] == "5А":
                letterOfTheClass = "D"
            if classs[0][4] == "5Б":
                letterOfTheClass = "E"
            if classs[0][4] == "5В":
                letterOfTheClass = "F"
            if classs[0][4] == "5Г":
                letterOfTheClass = "G"
            if classs[0][4] == "6А":
                letterOfTheClass = "H"
            if classs[0][4] == "6Б":
                letterOfTheClass = "I"
            if classs[0][4] == "6В":
                letterOfTheClass = "J"
            if classs[0][4] == "7А":
                letterOfTheClass = "K"
            if classs[0][4] == "7Б":
                letterOfTheClass = "L"
            if classs[0][4] == "7В":
                letterOfTheClass = "M"
            if classs[0][4] == "7Г":
                letterOfTheClass = "N"
            if classs[0][4] == "8А":
                letterOfTheClass = "O"
            if classs[0][4] == "8Б":
                letterOfTheClass = "P"
            if classs[0][4] == "8В":
                letterOfTheClass = "Q"
            if classs[0][4] == "8Г":
                letterOfTheClass = "R"
            if classs[0][4] == "9А":
                letterOfTheClass = "S"
            if classs[0][4] == "9Б":
                letterOfTheClass = "T"
            if classs[0][4] == "9В":
                letterOfTheClass = "U"
            if classs[0][4] == "9Г":
                letterOfTheClass = "V"
            if classs[0][4] == "10А":
                letterOfTheClass = "W"
            if classs[0][4] == "11А":
                letterOfTheClass = "X"
            userClass = classs[0][4]
            return userClass, letterOfTheClass

        #приветственное сообщение
        def startMessage():
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Вас приветствует бот с расписанием для школы №10\nВоспользуйтесь клавиатурой для выбора класса\n\n(В случае ошибки вы всегда сможете поменять класс в главном меню)",
                keyboard=keyboardClassChoice.get_keyboard()
            )

        while True:    
            try:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        allVars = ['начать', 'меню', 'сегодня', 'завтра', 'выбор по дню недели', 'выбор класса', 
                        'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 
                        '5а', '5б', '5в', '5г', '6а', '6б', '6в', '7а', '7б', '7в', '7г', '8а', '8б', '8в', '8г', '9а', '9б', '9в', '9г', '10а', '11а']
                        if event.text.lower() not in allVars:
                            unknown_message()
                        if event.text.lower() == "начать" or event.text.lower() == "меню":
                            startMessage()
                        if event.text.lower() == "сегодня":
                            get_today(self=self, user_id=event.user_id)
                        if event.text.lower() == "завтра":
                            get_tomorrow(self=self, user_id=event.user_id)
                        if event.text.lower() == "выбор по дню недели":
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="Воспользуйтесь клавиатурой для выбора дня",
                                keyboard=keyboardDayOfTheWeek.get_keyboard()
                            )
                        if event.text.lower() == "выбор класса":
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="Воспользуйтесь клавиатурой для выбора класса",
                                keyboard=keyboardClassChoice.get_keyboard()
                            )
                        if event.text.lower() == "понедельник":
                            get_day_timetable(self, day=1, user_id=event.user_id)
                        if event.text.lower() == "вторник":
                            get_day_timetable(self, day=2, user_id=event.user_id)
                        if event.text.lower() == "среда":
                            get_day_timetable(self, day=3, user_id=event.user_id)
                        if event.text.lower() == "четверг":
                            get_day_timetable(self, day=4, user_id=event.user_id)
                        if event.text.lower() == "пятница":
                            get_day_timetable(self, day=5, user_id=event.user_id)
                        if event.text.lower() == "суббота":
                            get_day_timetable(self, day=6, user_id=event.user_id)
                        if event.text.lower() == "5а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "5А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5б":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "5Б"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5в":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "5В"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5г":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "5Г"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "6А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6б":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "6Б"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6в":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "6В"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "7А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7б":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "7Б"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7в":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "7В"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7г":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "7Г"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "8А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8б":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "8Б"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8в":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "8В"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8г":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "8Г"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "9А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9б":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "9Б"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9в":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "9В"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9г":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "9Г"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "10а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "10А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "11а":
                            us_id, us_name, us_sname, us_class, sub = userInfo()
                            userClassChoice = "11А"
                            if existsUser() == True:
                                updateUser(user_class=userClassChoice, user_id=event.user_id)
                                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                            else:
                                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=userClassChoice, sub=sub)
                                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
                                vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        
            except requests.exceptions.RequestException:
                print("\n Переподключение к серверам ВК \n")
                time.sleep(3)
            except:
                b.main()

b = bot()

def scheduleRunner(self):
    schedule.every().day.at("01:00").do(b.main().job)
    while True:
        schedule.run_pending()
        time.sleep(1)

b.main().job().run()

