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



def timetableToday():
            letterOfTheClass = checkUserClass(user_id=event.user_id)
            today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            weekOfTheDay = datetime.datetime.weekday(today)
            print(today, weekOfTheDay)
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
                resp = "Сегодня воскресенье. Уроков нет."
            print(resp)
            values = resp.get('values', [])
            values2 = timetableOfCalls.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            listtt2 = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                listtt2.append((str(values2[i]))[2:][:-2])
                text = 'Расписание на сегодня:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}.({}) {}'.format(i, ''.join(map(str, t)), ''.join(map(str, g))) for i, (g, t) in enumerate(zip(listtt, listtt2), 1)) + text2
            print(res)

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
