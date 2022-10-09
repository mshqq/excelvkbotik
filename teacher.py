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

def day_week(self):
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    return today.isoweekday()

def get_timedata(self, day):
    dayWeek = day
    if dayWeek == 1:
        dayLetter1 = "C"
        dayLetter2 = "M"
    if dayWeek == 2:
        dayLetter1 = "N"
        dayLetter2 = "X"
    if dayWeek == 3:
        dayLetter1 = "Y"
        dayLetter2 = "AI"
    if dayWeek == 4:
        dayLetter1 = "AJ"
        dayLetter2 = "AT"
    if dayWeek == 5:
        dayLetter1 = "AU"
        dayLetter2 = "BE"
    if dayWeek == 6:
        dayLetter1 = "BF"
        dayLetter2 = "BP"
    if dayWeek == 6:
        timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C58:C66").execute()
    else:
        timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
    timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C3:C13").execute()
    resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Учителя!{dayLetter1}3:{dayLetter2}3").execute()
    values = resp.get('values', [])
    values2 = timetableOfCalls.get('values', [])
    count = len(values2)
    listtt = []
    listtt2 = []
    for i in range(0, count):
        print(i)
        listtt.append((str(values[i]))[1:][:-1])
        listtt2.append((str(values2[i]))[2:][:-2])
        print(listtt)
        print("\n")
        listtt = listtt[0]
        print(listtt2)
        print("\n")
        listtt = listtt.split(',')
        text = f'Расписание на сегодня:\n\n'
        text2 = '\n\nХорошего дня!'
        res = text + '\n'.join(
        '{}.({}) {}'.format(i, ''.join(map(str, g)), ''.join(map(str, t))) for i, (g, t) in enumerate(zip(listtt2, listtt), 1)) + text2
    return res

def day_week(Self):
        return datetime.datetime.today().isoweekday()

def emptiness_day():
    return "Воскресенье - выходной день, уроков нет\nХорошего отдыха!🥳"

def get_today(self):
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%d.%m.%Y")
    day = day_week(self)
    if int(day) > 6:
        emptiness_day()
    text = f'Расписание на сегодня:\n\n'
    teacher = 1
    res = text + get_timedata(self, day, teacher)
    return res

print(get_timedata(Self, day=1))