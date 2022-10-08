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

def timetable():
    timetableOfCalls = sheet.values().get(spreadsheetId=sheet_id, range=f"Уроки!C25:C35").execute()
    resp = sheet.values().get(spreadsheetId=sheet_id, range=f"Учителя!C3:M3").execute()
    print(resp)
    print("\n")
    values = resp.get('values', [])
    print(values)
    print("\n")
    values2 = timetableOfCalls.get('values', [])
    count = len(values)
    print(count)
    print("\n")
    listtt = []
    listtt2 = []
    for i in range(0, count):
        listtt.append((str(values[i]))[1:][:-1])
        print(listtt)
        print("\n")
        listtt = listtt[0]
        print(listtt)
        print("\n")
        listtt = listtt.split(',')
        for y in range(0, len(listtt)):
            if listtt[y] == "":
                listtt[y] = "Окно"
        print(listtt[2])
        text = f'Расписание на сегодня:\n\n'
        text2 = '\n\nХорошего дня!'
        res = text + '\n'.join(
        '{}.{}'.format(i, ''.join((map(str, t)))) for i, t in enumerate(listtt, 1)) + text2
        print(res)
timetable()
def day_week(self):
        return datetime.datetime.today().isoweekday()
print(day_week(self))