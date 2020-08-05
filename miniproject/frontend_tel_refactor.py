import telebot
import backend_tel_refactor as back
bot = telebot.TeleBot('')
global all_candidate, choose_student, a
choose_student = True

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, чтобы узнать свои баллы в системе БРС напиши ФИО через пробел, можно также и просто фамилию и имя, а можно и фамилию')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global all_candidate, choose_student, a
    if not message.text.isdigit():
        print(message.text)
        all_candidate = back.all_candidate(message.text)
        if len(all_candidate) == 0:
            bot.send_message(message.from_user.id, "некорректный запрос")
        else:
            view_list = back.obrabotka_data_students(all_candidate)
            bot.send_message(message.from_user.id, view_list)
    elif choose_student:
        a = back.find_all_mark_student(all_candidate[int(message.text)-1][1],0)
        semestr = back.final_marks_students_for_view(a)
        choose_student = False
        bot.send_message(message.from_user.id,'выберите семестр')
    else:
        choose = back.choose_sem(a, int(message.text))
        bot.send_message(message.from_user.id, choose)

bot.polling()

