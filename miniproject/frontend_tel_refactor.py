import telebot
import backend_tel_refactor as back
bot = telebot.TeleBot('')
global all_candidate

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, чтобы узнать свои баллы в системе БРС напиши ФИО через пробел, можно также и просто фамилию и имя, а можно и фамилию')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global all_candidate
    if not message.text.isdigit():
        print(message.text)
        all_candidate = back.all_candidate(message.text)
        if len(all_candidate) == 0:
            bot.send_message(message.from_user.id, "некорректный запрос")
        else:
            view_list = back.obrabotka_data_students(all_candidate)
            bot.send_message(message.from_user.id, view_list)
    else:
        a = str(back.find_all_mark_student(all_candidate[int(message.text)-1][1],0))

        if len(a) > 4096:
            for x in range(0, len(a), 4096):
                bot.send_message(message.chat.id, a[x:x + 4096])
        else:
            bot.send_message(message.chat.id, a)
        #bot.send_message(message.from_user.id, a)

bot.polling()

