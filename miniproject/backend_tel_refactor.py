import requests
from bs4 import BeautifulSoup
def all_candidate(student):
    #находим линки всех курсов
    data_students_kurse = get_all_curse_link()
    #находим студентов, у которых ФИО такое же,как и у того, что было прислано
    data_students_N = find_all_same_student(data_students_kurse,student)
    #здесь каким-то магическим образом студент находит себя и "дает" ссылку на себя
    find_all_mark_student(data_students_N[0][1])

def get_all_curse_link():
    vgm_url = 'http://www.rating.unecon.ru/rating.php?&f=1&p=12684&is_rating_vipusk=0&y=2018&y_vipusk=2020&s=none'
    soup = parse_html(vgm_url)
    data_students_kurse = []
    for a in soup.find_all('a',href=True)[2:7]:
        data_students_kurse.append([a.get_text(), 'http://www.rating.unecon.ru/' + a.get('href')])
    return data_students_kurse

def find_all_same_student(data_student_kurse,student):
    data_students_N = []
    len_student_info = len(student.split(" "))
    for N_curse_link in data_student_kurse:
        soup = parse_html(N_curse_link[1])

        for prob_N in soup.find_all('table'):
            for student_N in prob_N.find_all('a', href=True):

                prom = find_same_student(len_student_info,student_N,student)
                if prom != -1:
                    data_students_N.append(prom)
                len_student_info = len(student.split(" "))

    return data_students_N

def find_same_student(len_student_info,student_N,student):
    check_fam = False
    k = 0
    for check in student_N.get_text().split(" "):
        if len_student_info > 0:
            if student.split(" ")[k].lower() == check.lower():
                check_fam = True
            else:
                check_fam = False
                break
        k += 1
        len_student_info -= 1
    if check_fam:
        return [student_N.get_text(), 'http://www.rating.unecon.ru/' + student_N.get('href')]
    else:
        return -1

def find_all_mark_student(link_student):
    soup = parse_html(link_student)
    print(soup)
    for tabl in soup.find_all('tbody'):
        print(tabl)

def parse_html(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup
all_candidate("Иванов Александр")
