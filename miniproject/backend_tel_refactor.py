import requests
from bs4 import BeautifulSoup
import urllib.request

def all_candidate(student):
    #находим линки всех курсов
    data_students_kurse = get_all_curse_link()
    #находим студентов, у которых ФИО такое же, как и у того, что было прислано
    data_students_N = find_all_same_student(data_students_kurse, student)
    return data_students_N
    
def final_marks_students_for_view(data_marks):
    view, semestr = [], []
    
    for i in data_marks:
        view.append(i[0][0])
        there_is_kt0 = True        
        for k in i[1][0]:
            if k != '0':
                there_is_kt0 = False
                
        for i1 in i[1][1:]:
            for j in range(len(i1[0])):
                if i1[0][j: j+2] in ['н)', 'т)']:
                    view.append(i1[0][: j+2])
                    if there_is_kt0 == False:
                        [view.append(f'КТ{k+1}: ' + i1[k+1])
                         for k in range(len(i[1][0][1:-3]))]
                        view.extend(['Баллы за экзамен: ' + i1[-3],
                                    '∑баллов: ' + i1[-2],
                                    'Оценка: ' + i1[-1]])
                    else:
                        [view.append(f'КТ{k}: ' + i1[k+1])
                         for k in range(len(i[1][0][1:-3]))]
                        view.extend(['Баллы за экзамен: ' + i1[-3],
                                    '∑баллов: ' + i1[-2],
                                    'Оценка: ' + i1[-1]])
                    break
                
        semestr.append('\n' + '\n'.join(view))
        view = []        
    return semestr

def choose_sem(data_marks, numb):
    semesters = final_marks_students_for_view(data_marks)
    return semesters[-numb]

def obrabotka_data_students(data_students_N):
    view_list = ''
    for i in range(len(data_students_N)):
        view_list += str(i+1) + ". " + data_students_N[i][0] +'\n'
    return view_list

def final_data_mark_student(semestr_data):
    res = ''
    semestr_all = []
    for i in semestr_data:
        res += str(i[0])+'\n'
        for i1 in i[1]:
            res += str(i1)+'\n'
        semestr_all.append(res)
        res = ''
    return semestr_all

def get_all_curse_link():
    vgm_url = 'http://www.rating.unecon.ru/rating.php?&f=1&p=12684&is_rating_vipusk=0&y=2018&y_vipusk=2020&s=none'
    soup = parse_html(vgm_url)
    data_students_kurse = []
    for a in soup.find_all('a',href=True)[2:7]:
        data_students_kurse.append([a.get_text(), 'http://www.rating.unecon.ru/' + a.get('href')])
    return data_students_kurse

def find_all_same_student(data_student_kurse, student):
    data_students_N = []
    for N_curse_link in data_student_kurse:
        soup = parse_html(N_curse_link[1])

        for prob_N in soup.find_all('table'):
            for student_N in prob_N.find_all('a', href=True):

                prom = compare_stundents(student_N, student)
                if prom != -1:
                    data_students_N.append(prom)

    return data_students_N

def compare_stundents(student_N, student):
    check_fam = False
    k = 0
    student_data = student.split(" ")
    student_N_data = student_N.get_text().split(" ")
    if len(student_N_data) < len(student_data):
        for check in student_N_data:
            if student_data[k].lower() == check.lower():
                check_fam = True
                print(student_data)
            else:
                check_fam = False
                break
            k += 1
    else:
        for check1 in student_data:
            if check1.lower() == student_N_data[k].lower():
                check_fam = True
            else:
                check_fam = False
                break
            k += 1
    if check_fam:
        return [student_N.get_text(), 'http://www.rating.unecon.ru/' + student_N.get('href')]
    else:
        return -1

#парсит как и индивидуальные страницы, так и общие
# 0 - частная, 1 - общая
def find_all_mark_student(link_student, type_tabl):
    soup = parse_html(link_student)
    numberSemestr_data = []
    prom_semestr_subject = []
    prom_subject_and_marks = []
    prom = []
    prom_first_sem = True
    for link in soup.find_all('table'):
        for lines_in_table in link.find_all("tr"):
            for comp_of_line in lines_in_table.find_all("td"):
                #добавление нового семестра и очистка
                if "семестр" in comp_of_line.get_text():
                    numberSemestr_data.append([prom_semestr_subject.copy(), prom_subject_and_marks.copy()])
                    prom_semestr_subject.clear()
                    prom_subject_and_marks.clear()
                    prom_semestr_subject.append(comp_of_line.get_text())
                    prom_first_sem = False
                else:
                    prom.append(comp_of_line.get_text())
            if prom_first_sem:
                prom_subject_and_marks.append(prom.copy())
                prom.clear()
            prom_first_sem = True
    numberSemestr_data.append([prom_semestr_subject.copy(), prom_subject_and_marks.copy()])
    if type_tabl == 0:
        numberSemestr_data.remove([[], []])
    if type_tabl == 1:
        numberSemestr_data[0][1].remove([])
        numberSemestr_data[0][1].remove([])
        numberSemestr_data = numberSemestr_data[0][1]
    #for i in numberSemestr_data:
        #for i1 in i[1]:
            #print(i1)
    return numberSemestr_data

#парсит шапку таблицы ОБЩЕЙ, А НЕ ОПРЕДЕЛЕННОГО СТУДЕНТА
def find_some(link_table_one):
    name_sub = []
    soup = parse_html(link_table_one)
    for i in soup.find_all('table'):
        for i1 in i.find_all('thead'):
            for i2 in i1.find_all('th'):
                name_sub.append(i2.get_text())
    name_sub.remove('∑баллов')
    name_sub.append('∑баллов')
    print(name_sub)
    return name_sub

def parse_html(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup

#final_marks_students_for_view(find_all_mark_student('http://www.rating.unecon.ru/stud_cd.php?stud=535578',0))
#choose_sem(find_all_mark_student('http://www.rating.unecon.ru/stud_cd.php?stud=554679',0),2)
#all_candidate("Осипов")
#частные случай
#find_all_mark_student('http://www.rating.unecon.ru/stud_cd.php?stud=554679',0)
#общие таблицы
#find_all_mark_student("http://www.rat ing.unecon.ru/index.php?&y=2018&k=1&f=1&up=12020&s=4&g=all&sort=fio&ball=hide&upp=244506",1)
#find_some('http://www.rating.unecon.ru/index.php?&y=2018&k=1&f=1&up=12020&s=4&g=all&sort=fio&ball=hide&upp=244506')
