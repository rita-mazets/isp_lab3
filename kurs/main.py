import telebot

import config
import logging
from quistions import q_1, q_2,q_3 ,q_4

from aiogram import Bot, Dispatcher, executor, types
from sqleighter import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = telebot.TeleBot(token=config.API_TOKEN)

# инициализируем соединение с БД
db = SQLighter('db.db')

wallet=0
global info
global quiz

# Команда активации подписки
@bot.message_handler(commands=['subscribe'])
def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    bot.send_message(message.from_user.id,
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        bot.send_message(message.from_user.id,"Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        bot.send_message(message.from_user.id,"Вы успешно отписаны от рассылки.")



@bot.message_handler(commands=['start'])
def start(message):
	start1 = "Привет! Я Рита. \nТебе надоела скучная и рутинная жизнь? Тогда тебе сюда. \nУ меня есть несколько интересных идей, как можно интересно провести время"
	start2 = "/help - помощь\n/quiz - ты сможешь прокачать себя по полной\n/next - перейти к следующему заданию\n/wallet - баланс\n/transfer - пополнтить чужие запасы\n/passed - завершенные викторины"
	bot.send_message(message.from_user.id,start1)
	bot.send_message(message.from_user.id,start2)


@bot.message_handler(commands=['help'])
async def startf(message):
	start2 = "/help - помощь\n/quiz - ты сможешь прокачать себя по полной\n/next - перейти к следующему заданию\n/wallet - баланс\n/transfer - пополнтить чужие запасы\n/passed - завершенные викторины"
	await bot.send_message(message.from_user.id,start2)


@bot.message_handler(commands=['wallet'])
async def wallet(message: types.Message):
        await bot.send_message(message.from_user.id,f"В кошельке {db.subscriber_wallet(message.from_user.id)}")


@bot.message_handler(commands=['passed'])
async def passed(message: types.Message):
    is_quiz = db.subscriber_passed(message.from_user.id)
    str= "Завершенные викторины: "
    if is_quiz[0]:
        str += "1"
    if is_quiz[1]:
        str += "2"
    if is_quiz[2]:
        str += "3"
    if is_quiz[3]:
        str += "4"
    await bot.send_message(message.from_user.id,str)


@bot.message_handler(commands=['quiz'])
def quiz(message):
    quizstr = "Что выбираем?\n1. Случайные вопросы \n2. Эрудиция \n3. Музыка \n4. Еда "
    bot.send_message(message.from_user.id,quizstr)




@bot.message_handler(func=lambda m: True)
def register_quis(message):
    print("fff")
    quiz_number = db.subscriber_quiz(message.from_user.id)
    print(db.subscriber_quiz(message.from_user.id))
    global quiz
    quiz=message.text
    global info
    if quiz == '1':
        if quiz_number[0]>4:
            bot.send_message(message.from_user.id,"Этот раздел уже был пройден! Выбирай другой! Баллы просто так не зарабатываются")
        else:
            info=q_1[quiz_number[0]]
            print(info)
            is_quiz = info[4]
            quiz_id = info[3]
            print(is_quiz)
            print(quiz_id)
            db.update_quiz11_subscription(message.from_user.id, is_quiz)
            db.update_quiz12_subscription(message.from_user.id, quiz_id)
            keyboard = types.InlineKeyboardMarkup()
            key_1 = types.InlineKeyboardButton(text=info[0][0], callback_data=info[1][0])
            keyboard.add(key_1)
            key_2 = types.InlineKeyboardButton(text=info[0][1], callback_data=info[1][1])
            keyboard.add(key_2)
            key_3 = types.InlineKeyboardButton(text=info[0][2], callback_data=info[1][2])
            keyboard.add(key_3)
            key_4 = types.InlineKeyboardButton(text=info[0][3], callback_data=info[1][3])
            keyboard.add(key_4)
            bot.send_message(message.from_user.id,text=info[2], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global wallet
    if call.data == "Greek":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == 'Thailand' or call.data == 'Philippines' or call.data == 'Cyprus':
        bot.send_message(call.message.chat.id, "Эээ... Такого не знать... Конечно, это Греция!")
    elif call.data == "Japan":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Argentina" or call.data == "Belgium" or call.data == "German" :
        bot.send_message(call.message.chat.id, "Нее, что-то ты попутал... Это Япония")
    elif call.data == "church":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "telephone" or call.data == "different" or call.data == "auto" :
        bot.send_message(call.message.chat.id, "Не играл что ли? Тогда быстрее беги в церковь!")
    elif call.data == "researchers":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "source" or call.data == "scientist" or call.data == "Compass creator" :
        bot.send_message(call.message.chat.id, "Он одним из первых обследовал Австралию, а ещё воглавил три круглосветные экспедиции по исследованию Мирового океана")
    elif call.data == "Pugachev":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Razin" or call.data == "Ermak" or call.data == "Godynov" :
        bot.send_message(call.message.chat.id, "Цэ Пугачев")
    elif call.data == "Наука":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Базар" or call.data == "Счет" or call.data == "Обмен" :
        bot.send_message(call.message.chat.id, "Правильный ответ: наука")
    elif call.data == "Солнце":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Земля" or call.data == "Сатурн" or call.data == "Луна" :
        bot.send_message(call.message.chat.id, "Конечно же солнце!")
    elif call.data == "золото":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "корона" or call.data == "традиции" or call.data == "мифы" :
        bot.send_message(call.message.chat.id, "Золото! Латинское aurum  означает \"желтое\" и родственно с \"Авророй\" - утренней зарей")
    elif call.data == "мастер":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "герой" or call.data == "война" or call.data == "преступление" :
        bot.send_message(call.message.chat.id, "А это-то произведение \"Мастер и Маргарита\". Как это я про себя вопрос не задам?) Та ещё ведьма!)")
    elif call.data == "Глушитель":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Рессора" or call.data == "Пружина" or call.data == "Аммортизатор" :
        bot.send_message(call.message.chat.id, "Глушитель! Настоящие мужчины ответили правильно. Ну и Полина Зорко")
    elif call.data == "Кострами":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Небом" or call.data == "Камнями" or call.data == "Ветром" :
        bot.send_message(call.message.chat.id, "Кострами! Она не стала кострами")
    elif call.data == "хватит":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "жук" or call.data == "тетради" or call.data == "катя" :
        bot.send_message(call.message.chat.id, "Хватит")
    elif call.data == "Пропасть":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Кручу" or call.data == "Бездну" or call.data == "Жерло" :
        bot.send_message(call.message.chat.id, "Пропасть")
    elif call.data == "Рюмка водки":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Чашка чая" or call.data == "Кружка морса" or call.data == "Кружка морса" :
        bot.send_message(call.message.chat.id, "Не все так плохо. Водка есть - и хорошо")
    elif call.data == "Услышала":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Плачу" or call.data == "Коснулась" or call.data == "Звока" :
        bot.send_message(call.message.chat.id, "Не все так плохо. Водка есть - и хорошо")
    elif call.data == "Испании":
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Команлировке по Калыме" or call.data == "Сардинии" or call.data == "Португалии" :
        bot.send_message(call.message.chat.id, "Не все так плохо. Водка есть - и хорошо")
    elif call.data == "Форшмак":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Бешамэль" or call.data == "Крюшон" or call.data == "Стифадо" :
        bot.send_message(call.message.chat.id, "Форшмак! Я вот даже ночью бегала его кушать после этого вопроса)")
    elif call.data == "ОАЭ":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Египет" or call.data == "Азейбайджан" or call.data == "Греция" :
        bot.send_message(call.message.chat.id, "ОАЭ")
    elif call.data == "Славакия":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Литва" or call.data == "Хорватия" or call.data == "Украина" :
        bot.send_message(call.message.chat.id, "Славакия")
    elif call.data == "Креманка":
        bot.send_message(call.message.chat.id, "Правильно! Тебе начислено 10 баллов")
        wallet = db.subscriber_wallet(call.message.chat.id)
        db.update_wallet(call.message.chat.id, wallet + 10)
    elif  call.data == "Менажница" or call.data == "Пиала" or call.data == "Кокильница" :
        bot.send_message(call.message.chat.id, "Креманка")


# запускаем лонг поллинг
if __name__ == '__main__':
    bot.polling()