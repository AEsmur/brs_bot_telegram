import telebot
import backend_tel as back
bot = telebot.TeleBot('');

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет,с помощью меня ты можешь узнать свои баллы в брс:'
                                      ' Напишите номер курса,название специаальности,'
                                      ' номер семетра и'
                                      ' название группы (сначала краткое название группы потом дефис и номер'
                                      'Все, что выше через пробел,а название специальность через нижний слеш')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #data_info = back.main(message.text,0)
    data_info = message.text.split()
    #я знаю, что это тупо.
    print(len(data_info[1].split("_")))

    if len(data_info[1].split("_")) == 1:
        data_info[1] = data_info[1]
    else:
        s  = ''
        for i in data_info[1].split("_"):
            s += i +" "
        s = s[:(len(s)-1)]
        data_info[1] = s
    link_to_main = back.kurse_and_profile(data_info[0],data_info[1],data_info[2],data_info[3])
    fio = str(data_info[4]+" "+ data_info[5]+" "+ data_info[6])
    all_res = back.main(fio,link_to_main)
    print(link_to_main)
    bot.send_message(message.from_user.id, all_res)
bot.polling()

