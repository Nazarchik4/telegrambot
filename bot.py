from typing import Text
import telebot
import sqlite3
import settings
from telebot import types
from datetime import *
import pendulum

#################################################################################
db = sqlite3.connect('db.db',check_same_thread=False)
curs = db.cursor()
bot = telebot.TeleBot(settings.token)
today_date = pendulum.today('Europe/Moscow').format('DD.MM')
tomorow_date = pendulum.tomorrow('Europe/Moscow').format('DD.MM')
counter = 0
day = 0
first_ss = "10:00-12:00"
second_ss = "12:00-14:00"
third_ss = "14:00-16:00"
fourth_ss = "16:00-18:00"
fifth_ss = "18:00-20:00"
date_from_user = None
button_date_from_user = None
date_counter = 0
dt = datetime.now()
td = timedelta(days=day)
# your calculated date
my_date = dt + td
####################################################################################

curs.execute("CREATE TABLE IF NOT EXISTS users(name TEXT,surname TEXT,date TEXT,time TEXT)")

@bot.message_handler(commands=['start'])
def start(message):
    
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Записатися")
    item2 = types.KeyboardButton("Інформація")
    markup.add(item2,item1)
    

    bot.send_message(message.chat.id,"Привіт {0.first_name} {0.last_name}, dfc вітає чат-бот, який допоможе вам записатися до Назіка на манікюр, перед використанням бота рекомендовано прочитати розділ інформація, оскільки там є розділ про формат часу, який зрозумілий для бота".format(message.from_user,bot.get_me()),reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handler(message):
    global counter
    global button_date_from_user
    global day
    global today_date
    global tomorow_date
    global dt
    global td
    global my_date
    day = 1
    # print(my_date.strftime('%d.%m'))
    name = message.from_user.first_name
    lastname = message.from_user.last_name

    if message.chat.type == 'private':
        if message.text == "Записатися":
            markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Сьогодні("+str(today_date)+")")
            item2 = types.KeyboardButton("Завтра("+str(tomorow_date)+")")
            item3 = types.KeyboardButton("Вибрати іншу дату")
            item4 = types.KeyboardButton("Назад")
            markup_main.add(item1,item2,item3,item4)

            bot.send_message(message.chat.id,"Виберіть ,будь ласка, один із запропонованих варіантів", reply_markup=markup_main)
        

        elif message.text == "Сьогодні("+str(today_date)+")":
            markup_today = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(first_ss)
            button2 = types.KeyboardButton(second_ss)
            button3 = types.KeyboardButton(third_ss)
            button4 = types.KeyboardButton(fourth_ss)
            button5 = types.KeyboardButton(fifth_ss)
            button6 = types.KeyboardButton("Назад")
            markup_today.add(button1,button2,button3,button4,button5,button6)

            gre = bot.send_message(message.chat.id,"Виберіть годину", reply_markup=markup_today)
            bot.register_next_step_handler(gre, today_date_reaction)

        elif message.text == "Завтра("+str(tomorow_date)+")":
            markup_today = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton(first_ss)
            button2 = types.KeyboardButton(second_ss)
            button3 = types.KeyboardButton(third_ss)
            button4 = types.KeyboardButton(fourth_ss)
            button5 = types.KeyboardButton(fifth_ss)
            button6 = types.KeyboardButton("Назад")
            markup_today.add(button1,button2,button3,button4,button5,button6)

            gre1 = bot.send_message(message.chat.id,"Виберіть годину", reply_markup=markup_today)
            bot.register_next_step_handler(gre1, tomorow_date_reaction)
        elif message.text == "Далі" or message.text == "Вибрати іншу дату":
            counter += 1
            for i in range(counter):
                new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in range(1):
                    day += 1
                    dt = datetime.now()
                    td = timedelta(days=day)
                    # your calculated date
                    my_date = dt + td
                    n_button1 = types.KeyboardButton(my_date.strftime('%d.%m'))
                for i in range(1):
                    day += 1
                    dt = datetime.now()
                    td = timedelta(days=day)
                    # your calculated date
                    my_date = dt + td
                    n_button2 = types.KeyboardButton(my_date.strftime('%d.%m'))
                for i in range(1):
                    day += 1
                    dt = datetime.now()
                    td = timedelta(days=day)
                    # your calculated date
                    my_date = dt + td
                    n_button3 = types.KeyboardButton(my_date.strftime('%d.%m'))
                for i in range(1):
                    day += 1
                    dt = datetime.now()
                    td = timedelta(days=day)
                    # your calculated date
                    my_date = dt + td
                    n_button4 = types.KeyboardButton(my_date.strftime('%d.%m'))
                for i in range(1):
                    n_button5 = types.KeyboardButton("Далі")
                for i in range(1):
                    n_button6 = types.KeyboardButton("Назад")
            new_markup.add(n_button1,n_button2,n_button3,n_button4,n_button5,n_button6)
            msg = bot.send_message(message.chat.id, "Виберіть дату, будь ласка", reply_markup=new_markup)
            bot.register_next_step_handler(msg,reaction)
        

        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup.add(b_item1,b_item2)
                
            bot.send_message(message.chat.id,"Ви повернулися назад",reply_markup=markup)

def today_date_reaction(message):
    global counter
    global today_date
    button_time_from_user = message.text
    if button_time_from_user == "Назад":
        handler(message)
        return
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    info = (name, lastname, today_date, button_time_from_user)
    # main_date = "[('" + date_from_user + "'," + " " +"'"+ time_from_user + "')]"
    main_date = [today_date,button_time_from_user]
    curs.execute('SELECT date,time FROM users WHERE date = ? AND time = ?',(today_date,button_time_from_user,))
    date_from_database = curs.fetchall()
    if str(date_from_database) == "[]":
        curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
        db.commit() # saving data
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_item1 = types.KeyboardButton("Записатися")
        b_item2 = types.KeyboardButton("Інформація")
        counter = 0
        markup1.add(b_item1,b_item2)
                
        bot.send_message(message.chat.id,"Ви успішно записані!!",reply_markup=markup1)
    else:
        date_from_database_wb = date_from_database[0]
        if main_date[0] == date_from_database_wb[0] and main_date[1] == date_from_database_wb[1]:
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup2.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup2)
            return
        elif main_date[0] == date_from_database_wb[0] and main_date != date_from_database_wb[1]:
            curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
            bot.send_message(message.chat.id,"Ви успішно записані!!")
            db.commit() # saving data
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup3.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup3)
    # #print(date_from_user)

def tomorow_date_reaction(message):
    global counter
    global tomorow_date
    button_time_from_user = message.text
    if button_time_from_user == "Назад":
        handler(message)
        return
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    info = (name, lastname,tomorow_date, button_time_from_user)
    # main_date = "[('" + date_from_user + "'," + " " +"'"+ time_from_user + "')]"
    main_date = [tomorow_date,button_time_from_user]
    curs.execute('SELECT date,time FROM users WHERE date = ? AND time = ?',(tomorow_date,button_time_from_user,))
    date_from_database = curs.fetchall()
    if str(date_from_database) == "[]":
        curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
        db.commit() # saving data
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_item1 = types.KeyboardButton("Записатися")
        b_item2 = types.KeyboardButton("Інформація")
        counter = 0
        markup1.add(b_item1,b_item2)
                
        bot.send_message(message.chat.id,"Ви успішно записані!!",reply_markup=markup1)
    else:
        date_from_database_wb = date_from_database[0]
        if main_date[0] == date_from_database_wb[0] and main_date[1] == date_from_database_wb[1]:
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup2.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup2)
            return
        elif main_date[0] == date_from_database_wb[0] and main_date != date_from_database_wb[1]:
            curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
            bot.send_message(message.chat.id,"Ви успішно записані!!")
            db.commit() # saving data
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup3.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup3)
def reaction(message):
    global date_from_user
    global fifth_ss
    global first_ss
    global second_ss
    global third_ss
    global fourth_ss
    global day

    if message.chat.type == 'private':
        if message.text == message.text and message.text != "Назад" and message.text != "Далі": # checking text
            date_from_user = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(first_ss)
            item2 = types.KeyboardButton(second_ss)
            item3 = types.KeyboardButton(third_ss)
            item4 = types.KeyboardButton(fourth_ss)
            item5 = types.KeyboardButton(fifth_ss)
            item6 = types.KeyboardButton("Назад")

            markup.add(item1,item2,item3,item4,item5,item6)
            msg = bot.send_message(message.chat.id, "Виберіть зручну для вас годину",reply_markup=markup)
            bot.register_next_step_handler(msg,date_reaction)
            return date_from_user 
        else:
            handler(message)
              

def date_reaction(message):
    global counter
    global date_counter
    time_from_user = message.text
    if time_from_user == "Назад":
        handler(message)
        return
    name = message.from_user.first_name
    lastname = message.from_user.last_name
    info = (name, lastname, date_from_user, time_from_user)
    # main_date = "[('" + date_from_user + "'," + " " +"'"+ time_from_user + "')]"
    main_date = [date_from_user,time_from_user]

    print(main_date)
    curs.execute('SELECT date,time FROM users WHERE date = ? AND time = ?',(date_from_user,time_from_user,))
    date_from_database = curs.fetchall()
    if str(date_from_database) == "[]":
        curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
        db.commit() # saving data
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_item1 = types.KeyboardButton("Записатися")
        b_item2 = types.KeyboardButton("Інформація")
        counter = 0
        markup1.add(b_item1,b_item2)
                
        bot.send_message(message.chat.id,"Ви успішно записані!!",reply_markup=markup1)
        return
    else:
        date_from_database_wb = date_from_database[0]
        if main_date[0] == date_from_database_wb[0] and main_date[1] == date_from_database_wb[1]: 
            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup2.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup2)
            return
        elif main_date[0] == date_from_database_wb[0] and main_date != date_from_database_wb[1]:
            curs.execute("INSERT INTO users VALUES(?, ?, ?, ?);", info) # inserting data into database
            bot.send_message(message.chat.id,"Ви успішно записані!!")
            db.commit() # saving data
            markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            b_item1 = types.KeyboardButton("Записатися")
            b_item2 = types.KeyboardButton("Інформація")
            counter = 0
            markup3.add(b_item1,b_item2)
            bot.send_message(message.chat.id,"Нажаль, такий час уже зайнятий, виберіть, будь ласка, іншу годину,або інше число",reply_markup=markup3)
            return
db.commit()
bot.polling(none_stop=True)