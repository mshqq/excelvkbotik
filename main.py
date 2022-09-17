#импортируем библиотеки и зависимости
#dev = "vk1.a.D-fpNfhiMevsybE67PEzjofN0fo3q8Tz0rULa4fv8l526myts35sExA_C2y5OSZo5PEvZ4TH0gZp_X-vja5IGM1cSoULqNDnyjXyd7l9puFj55doKD8Z_7QAlx_0Njyecj3BdliucdodfTUG-Magsb1jTtcG6k8UHHq8weaQja0PPpRQRC9k6cR3dD7CwmIt"
#prod = "vk1.a.6s7T854sQ9SJXCfyl2_Q2iofR9LWyVEcSungdfDsm0328JNfiIFhrJfTnipIm5gefZWyaIqOo4mL4EbDQkrlCgUY76aoifQmsu4p67yz_BHtSSLtahOfe6Kqzlg_6MflFyXoYYqpyW9SsL_UDTrt9iIUaULWFXi01bcSNYfuTZpnpPGtLo9Ts2XSqbEFY8pt"
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
from tinydb import TinyDB, Query
db = TinyDB('db.json')
User = Query()

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

#запускаем прослушку канала сообщений
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

#объявляем клавиатуру главного меню без рассылки
keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Завтра', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Послезавтра', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Выбор по дню недели', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
#keyboard.add_button('Рассылка', color=VkKeyboardColor.SECONDARY)
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



global res

class bot:
    def main(self):
        global resp
        def addUserToClass(user_id, userChoice):
            db.insert({'user_id': user_id, 'classOfTheUser': userChoice})

        def updateUserClass(user_id, userChoice):
            db.update({'user_id': user_id, 'classOfTheUser': userChoice})

        def checkUserClass(user_id):
            userChoice = db.get(User['user_id'] == user_id)['classOfTheUser']
            if userChoice.lower() == "5а":
                letterOfTheClass = "D"
            if userChoice.lower() == "5б":
                letterOfTheClass = "E"
            if userChoice.lower() == "5в":
                letterOfTheClass = "F"
            if userChoice.lower() == "5г":
                letterOfTheClass = "G"
            if userChoice.lower() == "6а":
                letterOfTheClass = "H"
            if userChoice.lower() == "6б":
                letterOfTheClass = "I"
            if userChoice.lower() == "6в":
                letterOfTheClass = "J"
            if userChoice.lower() == "7а":
                letterOfTheClass = "K"
            if userChoice.lower() == "7б":
                letterOfTheClass = "L"
            if userChoice.lower() == "7в":
                letterOfTheClass = "M"
            if userChoice.lower() == "7г":
                letterOfTheClass = "N"
            if userChoice.lower() == "8а":
                letterOfTheClass = "O"
            if userChoice.lower() == "8б":
                letterOfTheClass = "P"
            if userChoice.lower() == "8в":
                letterOfTheClass = "Q"
            if userChoice.lower() == "8г":
                letterOfTheClass = "R"
            if userChoice.lower() == "9а":
                letterOfTheClass = "S"
            if userChoice.lower() == "9б":
                letterOfTheClass = "T"
            if userChoice.lower() == "9в":
                letterOfTheClass = "U"
            if userChoice.lower() == "9г":
                letterOfTheClass = "V"
            if userChoice.lower() == "10а":
                letterOfTheClass = "W"
            if userChoice.lower() == "11а":
                letterOfTheClass = "X"
            return letterOfTheClass
        def job():
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            weekOfTheDay = datetime.datetime.weekday(today)
            with open('Subs.txt', 'r') as f:
                subs = f.readlines()
            subs_int = [int(x) for x in subs]
            vk.messages.send(
                user_id=subs_int,
                random_id=get_random_id(),
                message="Автоматическая рассылка расписания!",
                keyboard=keyboard.get_keyboard()
            )
            if weekOfTheDay == 0:
                monday(user_id=subs_int)
            if weekOfTheDay == 1:
                tuesday(user_id=subs_int)
            if weekOfTheDay == 2:
                wednesday(user_id=subs_int)
            if weekOfTheDay == 3:
                thursday(user_id=subs_int)
            if weekOfTheDay == 4:
                friday(user_id=subs_int)
            if weekOfTheDay == 5:
                saturday(user_id=subs_int)
        #приветственное сообщение
        def start():
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Вас приветствует бот с расписанием для школы №10\nВоспользуйтесь клавиатурой для выбора класса\n\n(В случае ошибки вы всегда сможете поменять класс в главном меню)",
                keyboard=keyboardClassChoice.get_keyboard()
            )

        def checkSub(user_id):
            with open("Subs.txt", "r") as f:
                listOfSubscriptions = f.read().splitlines()
            print(listOfSubscriptions)
            print(user_id)
            if str(user_id) in listOfSubscriptions:
                return True
            else:
                return False

        def deleteSub(user_id):
            with open("Subs.txt", "r") as f:
                listOfSubscriptions = f.read().splitlines()
            if checkSub(user_id=event.user_id) is True:
                listOfSubscriptions.remove(str(user_id))
                with open("Subs.txt", "w") as f:
                    for item in listOfSubscriptions:
                        f.write(item)
                        f.write('\n')
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Вы успешно отписались от рассылки!",
                    keyboard=keyboard.get_keyboard()
                )
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    message="Вы и так не подписаны на рассылку!",
                    keyboard=keyboard.get_keyboard()
                )
        #расписание на сегодня
        def timetableToday():
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            todayDay = todayDay.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            weekOfTheDay = datetime.datetime.weekday(today)
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            if weekOfTheDay == 0:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}3:{letterOfTheClass}13").execute()
            if weekOfTheDay == 1:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}14:{letterOfTheClass}24").execute()
            if weekOfTheDay == 2:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}25:{letterOfTheClass}35").execute()
            if weekOfTheDay == 3:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}36:{letterOfTheClass}46").execute()
            if weekOfTheDay == 4:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}47:{letterOfTheClass}57").execute()
            if weekOfTheDay == 5:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}58:{letterOfTheClass}68").execute()
            if weekOfTheDay == 6:
                vk.messages.send(
                    user_id=event.user_id,
                    message="В воскресенье уроков нет.",
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard()
            )
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на сегодня {todayDay}:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание за сегодня")

        def timetableTomorrow():
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            weekOfTheDay = datetime.datetime.weekday(today) + 1
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            if weekOfTheDay == 0:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}3:{letterOfTheClass}13").execute()
            if weekOfTheDay == 1:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}14:{letterOfTheClass}24").execute()
            if weekOfTheDay == 2:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}25:{letterOfTheClass}35").execute()
            if weekOfTheDay == 3:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}36:{letterOfTheClass}46").execute()
            if weekOfTheDay == 4:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}47:{letterOfTheClass}57").execute()
            if weekOfTheDay == 5:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}58:{letterOfTheClass}68").execute()
            if weekOfTheDay == 6:
                vk.messages.send(
                    user_id=event.user_id,
                    message="В воскресенье уроков нет.",
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard()
            )
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на завтра {tomorrow}:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на завтра")

        def subStatus(user_id):
            if checkSub(user_id=event.user_id) == True:
                status = "оформлена"
            else:
                status = "не оформлена"
            msg = f'Текущий статус вашей подписки: "{status}"\nВоспользуйтесь меню'
            vk.messages.send(
                user_id=event.user_id,
                message=msg,
                random_id=get_random_id(),
                keyboard=keyboardSub.get_keyboard()
            )

        def timetableNextNextday():
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            NextNextDay = todayDay + datetime.timedelta(days=2)
            NextNextDay = NextNextDay.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            weekOfTheDay = datetime.datetime.weekday(today) + 2
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            if weekOfTheDay == 0:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}3:{letterOfTheClass}13").execute()
            if weekOfTheDay == 1:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}14:{letterOfTheClass}24").execute()
            if weekOfTheDay == 2:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}25:{letterOfTheClass}35").execute()
            if weekOfTheDay == 3:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}36:{letterOfTheClass}46").execute()
            if weekOfTheDay == 4:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}47:{letterOfTheClass}57").execute()
            if weekOfTheDay == 5:
                resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}58:{letterOfTheClass}68").execute()
            if weekOfTheDay == 6:
                vk.messages.send(
                    user_id=event.user_id,
                    message="В воскресенье уроков нет.",
                    random_id=get_random_id(),
                    keyboard=keyboard.get_keyboard()
            )
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на послезавтра {NextNextDay}:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на послезавтра")

        def addUserToSub(user_id):
            localState = checkSub(user_id=event.user_id)
            print(localState)
            if (localState == False):
                sub = str(user_id)
                with open("Subs.txt", "a") as file:
                    file.write(sub + '\n')
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),                
                    message="Вы успешно оформили подписку на рассылку, ожидайте...",
                    keyboard=keyboard.get_keyboard()
                )
            

            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),                
                    message="Вы уже подписаны на рассылку, ожидайте...",
                    keyboard=keyboard.get_keyboard()
                )

        def monday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}3:{letterOfTheClass}13").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на понедельник:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на понедельник")

        def tuesday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}14:{letterOfTheClass}24").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на вторник:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на вторник")

        def wednesday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}25:{letterOfTheClass}35").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на среду:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на среду")

        def thursday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}36:{letterOfTheClass}46").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на четверг:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на четверг")

        def friday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}47:{letterOfTheClass}57").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на пятницу:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание на пятницу")

        def saturday(user_id):
            now = datetime.datetime.now()
            now.strftime("%Y-%m-%d %H:%M")
            userUserid = event.user_id
            user_get=vk.users.get(user_ids = userUserid)
            user_get=user_get[0]
            first_name=user_get['first_name']
            last_name=user_get['last_name']
            full_name=first_name+" "+last_name
            todayDay = datetime.date.today()
            tomorrow = todayDay + datetime.timedelta(days=1)
            tomorrow = tomorrow.strftime("%d.%m.%Y")
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            letterForUser = db.get(User['user_id'] == event.user_id)['classOfTheUser']
            timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
            resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!{letterOfTheClass}58:{letterOfTheClass}68").execute()
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = f'Расписание {letterForUser.upper()} на субботу:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
            print(f"{now}: {full_name}({userUserid}) - {letterForUser.upper()} - получил расписание за субботу")

        while True:    
            try:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        if event.text.lower() == "начать" or event.text.lower() == "меню":
                            start()
                        if event.text.lower() == "рассылка":
                            subStatus(user_id=event.user_id)
                        if event.text.lower() == "подписаться на рассылку":
                            addUserToSub(user_id=event.user_id)
                        if event.text.lower() == "отписаться от рассылки":
                            deleteSub(user_id=event.user_id)
                        if event.text.lower() == "сегодня":
                            timetableToday()
                        if event.text.lower() == "завтра":
                            timetableTomorrow()
                        if event.text.lower() == "послезавтра":
                            timetableNextNextday()
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
                            monday(user_id=event.user_id)
                        if event.text.lower() == "вторник":
                            tuesday(user_id=event.user_id)
                        if event.text.lower() == "среда":
                            wednesday(user_id=event.user_id)
                        if event.text.lower() == "четверг":
                            thursday(user_id=event.user_id)
                        if event.text.lower() == "пятница":
                            friday(user_id=event.user_id)
                        if event.text.lower() == "суббота":
                            saturday(user_id=event.user_id)
                        if event.text.lower() == "5а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="5а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="5а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5б":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="5б")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="5б")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5в":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="5в")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="5в")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "5г":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="5г")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="5г")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="6а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="6а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6б":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="6б")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="6б")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "6в":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="6в")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="6в")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="7а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="7а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7б":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="7б")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="7б")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7в":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="7в")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="7в")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "7г":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="7г")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="7г")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="8а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="8а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8б":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="8б")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="8б")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8в":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="8в")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="8в")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "8г":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="8г")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="8г")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="9а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="9а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9б":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="9б")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="9б")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9в":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="9в")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="9в")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "9г":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="9г")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="9г")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "10а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="10а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="10а")
                            vk.messages.send(
                                    user_id=event.user_id,
                                    message="Данные о вашем классе успешно сохранены!\nВоспользуйтесь клавиатурой для выбора дня",
                                    random_id=get_random_id(),
                                    keyboard=keyboard.get_keyboard()
                            )
                        if event.text.lower() == "11а":
                            if db.contains(User["user_id"] == event.user_id) == True:
                                updateUserClass(user_id=event.user_id, userChoice="11а")
                            else:
                                addUserToClass(user_id=event.user_id, userChoice="11а")
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