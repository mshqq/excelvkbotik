#импортируем библиотеки и зависимости
#dev = "vk1.a.D-fpNfhiMevsybE67PEzjofN0fo3q8Tz0rULa4fv8l526myts35sExA_C2y5OSZo5PEvZ4TH0gZp_X-vja5IGM1cSoULqNDnyjXyd7l9puFj55doKD8Z_7QAlx_0Njyecj3BdliucdodfTUG-Magsb1jTtcG6k8UHHq8weaQja0PPpRQRC9k6cR3dD7CwmIt"
#prod = "vk1.a.6s7T854sQ9SJXCfyl2_Q2iofR9LWyVEcSungdfDsm0328JNfiIFhrJfTnipIm5gefZWyaIqOo4mL4EbDQkrlCgUY76aoifQmsu4p67yz_BHtSSLtahOfe6Kqzlg_6MflFyXoYYqpyW9SsL_UDTrt9iIUaULWFXi01bcSNYfuTZpnpPGtLo9Ts2XSqbEFY8pt"
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

#объяеляем клавиатуру главного меню
keyboard = VkKeyboard(one_time=False)
keyboard.add_button('Сегодня', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Завтра', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Послезавтра', color=VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Выбор по дню недели', color=VkKeyboardColor.PRIMARY)

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

#приветственное сообщение
def start():
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message="Вас приветствует бот с расписанием для 10А класса\nВоспользуйтесь клавиатурой для выбора дня",
        keyboard=keyboard.get_keyboard()
    )

#расписание на сегодня
def timetableToday():
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    weekOfTheDay = datetime.datetime.weekday(today)
    print(today, weekOfTheDay)
    if weekOfTheDay == 0:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W3:W13").execute()
    if weekOfTheDay == 1:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W14:W24").execute()
    if weekOfTheDay == 2:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W25:W35").execute()
    if weekOfTheDay == 3:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W36:W46").execute()
    if weekOfTheDay == 4:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W47:W57").execute()
    if weekOfTheDay == 5:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W58:W68").execute()
    if weekOfTheDay == 6:
        resp = "Сегодня воскресенье. Уроков нет."
    print(resp)
    values = resp.get('values', [])
    print(values)
    count = len(values)
    listtt = []
    for i in range(0, count):
        listtt.append((str(values[i]))[2:][:-2])
        text = f'Расписание на сегодня {today}:\n\n'
        text2 = '\n\nХорошего дня!'
        res = text + '\n'.join(
        '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
    vk.messages.send(
        user_id=event.user_id,
        message=res,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )

def timetableTomorrow():
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    weekOfTheDay = datetime.datetime.weekday(today) + 1
    print(today, weekOfTheDay)
    if weekOfTheDay == 0:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W3:W13").execute()
    if weekOfTheDay == 1:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W14:W24").execute()
    if weekOfTheDay == 2:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W25:W35").execute()
    if weekOfTheDay == 3:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W36:W46").execute()
    if weekOfTheDay == 4:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W47:W57").execute()
    if weekOfTheDay == 5:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W58:W68").execute()
    if weekOfTheDay == 6:
        resp = "Завтра воскресенье. Уроков нет."
    print(resp)
    values = resp.get('values', [])
    print(values)
    count = len(values)
    listtt = []
    for i in range(0, count):
        listtt.append((str(values[i]))[2:][:-2])
        text = 'Расписание на завтрашний день:\n\n'
        text2 = '\n\nХорошего дня!'
        res = text + '\n'.join(
        '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
    vk.messages.send(
        user_id=event.user_id,
        message=res,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )

def timetableNextNextday():
    today = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
    weekOfTheDay = datetime.datetime.weekday(today) + 2
    print(today, weekOfTheDay)
    if weekOfTheDay == 0:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W3:W13").execute()
    if weekOfTheDay == 1:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W14:W24").execute()
    if weekOfTheDay == 2:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W25:W35").execute()
    if weekOfTheDay == 3:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W36:W46").execute()
    if weekOfTheDay == 4:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W47:W57").execute()
    if weekOfTheDay == 5:
        resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W58:W68").execute()
    if weekOfTheDay == 6:
        resp = "Послезавтра воскресенье. Уроков нет."
    print(resp)
    values = resp.get('values', [])
    print(values)
    count = len(values)
    listtt = []
    for i in range(0, count):
        listtt.append((str(values[i]))[2:][:-2])
        text = 'Расписание на послезавтра:\n\n'
        text2 = '\n\nХорошего дня!'
        res = text + '\n'.join(
        '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
    vk.messages.send(
        user_id=event.user_id,
        message=res,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() == "начать":
            start()
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
        if event.text.lower() == "понедельник":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W3:W13").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на понедельник:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text.lower() == "вторник":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W14:W24").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на вторник:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text.lower() == "среда":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W25:W35").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на среду:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text.lower() == "четверг":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W36:W46").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на четверг:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text.lower() == "пятница":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W47:W57").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на пятницу:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )
        if event.text.lower() == "суббота":
            resp = sheet.values().get(spreadsheetId=sheet_id, range="Уроки!W58:W68").execute()
            print(resp)
            values = resp.get('values', [])
            print(values)
            count = len(values)
            listtt = []
            for i in range(0, count):
                listtt.append((str(values[i]))[2:][:-2])
                text = 'Расписание на субботу:\n\n'
                text2 = '\n\nХорошего дня!'
                res = text + '\n'.join(
                '{}. {}'.format(i, ''.join(map(str, t))) for i, t in enumerate(listtt, 1)) + text2
            vk.messages.send(
                user_id=event.user_id,
                message=res,
                random_id=get_random_id(),
                keyboard=keyboard.get_keyboard()
            )