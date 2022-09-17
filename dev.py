import random, vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import sqlite3

vk_session = vk_api.VkApi(
token='vk1.a.6s7T854sQ9SJXCfyl2_Q2iofR9LWyVEcSungdfDsm0328JNfiIFhrJfTnipIm5gefZWyaIqOo4mL4EbDQkrlCgUY76aoifQmsu4p67yz_BHtSSLtahOfe6Kqzlg_6MflFyXoYYqpyW9SsL_UDTrt9iIUaULWFXi01bcSNYfuTZpnpPGtLo9Ts2XSqbEFY8pt')
from vk_api.longpoll import VkLongPoll, VkEventType

#запускаем прослушку канала сообщений
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()

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

def userInfo():
    us_id = event.user_id
    user_get=vk.users.get(user_ids = (event.user_id))
    user_get=user_get[0]
    us_name = user_get['first_name']
    us_sname = user_get['last_name']
    us_class = "11А"
    sub = False
    return us_id, us_name, us_sname, us_class, sub;

def checkUserClass(user_id):
    userClass = cursor.execute('SELECT * FROM ExcelVKBot WHERE user_id=?', (event.user_id, ))
    classs = cursor.fetchall()
    return classs[0][4]

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text.lower() == "dev":
            vk.messages.send(
                user_id = event.user_id,
                message = 'Привет)',
                random_id = get_random_id()
            )
            us_id, us_name, us_sname, us_class, sub = userInfo()
            try:
                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class=us_class, sub=sub)
            except sqlite3.IntegrityError:
                print("Уже есть в базе данных!")
        
        if event.text.lower() == "dev5a":
            us_id, us_name, us_sname, us_class, sub = userInfo()
            userClassChoice = "5А"
            if existsUser() == True:
                updateUser(user_class=userClassChoice, user_id=event.user_id)
                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
            else:
                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class="5А", sub=sub)
                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
        if event.text.lower() == "dev6a":
            us_id, us_name, us_sname, us_class, sub = userInfo()
            userClassChoice = "6А"
            if existsUser() == True:
                updateUser(user_class=userClassChoice, user_id=event.user_id)
                print(f"{us_name} {us_sname}:{us_id} обновил свой класс - {userClassChoice}")
            else:
                registerUser(user_id=us_id, user_name=us_name, user_surname=us_sname, user_class="6А", sub=sub)
                print(f"{us_name} {us_sname}:{us_id} зарегистрировался - {userClassChoice}")
        
        if event.text.lower() == "devcheck":
            checkUserClass(user_id=event.user_id)
