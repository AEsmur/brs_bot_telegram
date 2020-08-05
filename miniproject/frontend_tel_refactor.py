import telebot
import backend_tel_refactor as back
bot = telebot.TeleBot('')
global all_candidate
global marks_of_student
global check_sem
check_sem = True
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, чтобы узнать свои баллы в системе БРС напиши ФИО через пробел, можно также и просто фамилию и имя, а можно и фамилию')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global all_candidate
    global marks_of_student
    global check_sem

    if not message.text.isdigit():
        check_sem = True
        print(message.text)
        all_candidate = back.all_candidate(message.text)
        if len(all_candidate) == 0:
            bot.send_message(message.from_user.id, "некорректный запрос")
        else:
            view_list = back.obrabotka_data_students(all_candidate)
            bot.send_message(message.from_user.id, view_list)
    else:
        if check_sem:
            a = back.find_all_mark_student(all_candidate[int(message.text)-1][1],0)
            marks_of_student = back.final_marks_students_for_view(a)
            print(marks_of_student)
            check_sem = False
            bot.send_message(message.from_user.id, "Напишите номер семетра, который хотите посмотреть")
            # for sem in marks_of_student:
            #     bot.send_message(message.from_user.id,sem)
        else:
            marks_of_student.reverse()
            bot.send_message(message.from_user.id, marks_of_student[int(message.text)-1])
            bot.send_message(message.from_user.id, "Напишите номер семетра, который хотите посмотреть или напишите ФИО следующего")
        #bot.send_message(message.from_user.id, a)

bot.polling()

