import requests
from bs4 import BeautifulSoup
import numpy as np
def main(name_student,link_real):
    vgm_url = link_real
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    kol_subject = -1
    bol = False
    name_subject = []
    non_or_yes = -1
    for link in soup.find_all('th'):
            non_or_yes += 1
            if "∑баллов" == link.get_text() or bol :
                bol = True
                kol_subject+=1
    for link in soup.find_all('th'):
        name_subject.append(link.get_text())
    if non_or_yes - kol_subject == 3:
        name_subject = name_subject[4::]
        name_subject.insert(0, "номер")
        name_subject.insert(1, "ФИО")
    else:
        name_subject = name_subject[5::]
        name_subject.insert(0,"номер")
        name_subject.insert(1,"ФИО")
        name_subject.insert(2,"№ группы")
    kol_subject+=2
    students = []
    for link in soup.find_all('tbody'):
        for link2 in link.find_all('td'):
            prom = link2.get_text()
            if prom == "":
                prom = "0"
            students.append(prom)
    students = np.array(students)
    all_students = np.split(students,len(students)/(len(name_subject)+1))
    print(name_subject)
    print(name_student)
    return all_students

def obrabotka(data_student,name_subject):
    str = ''
    for i in range(len(name_subject)):
        str += data_student[i] + " "+ name_subject[i] +"\n"
    return str
#будем считать что человек пишет только номер курса
def kurse_and_profile(number_kurse, name_spec ,numb,group):
    vgm_url = 'http://www.rating.unecon.ru'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data_students_kurse = {}
    i = 0
    for a in soup.find_all('a', href=True):
        if i < 6:
            data_students_kurse[a.get_text()] = 'http://www.rating.unecon.ru/' + a.get('href')
        else:
            break
        i+=1
    #находим нужный курс
    vgm_url = data_students_kurse.get(number_kurse+" курс")
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data_students_kurse.clear()
    for a in soup.find_all('a', href=True):
        data_students_kurse[a.get_text()] = 'http://www.rating.unecon.ru/' + a.get('href')
    #находим нужную специальность
    vgm_url = data_students_kurse.get(name_spec)
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data_students_kurse.clear()
    for a in soup.find_all('a', href=True):
        data_students_kurse[a.get_text()] = 'http://www.rating.unecon.ru/' + a.get('href')
    #выбираем семетр
    vgm_url =data_students_kurse.get(numb+" семестр (текущий)")
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data_students_kurse.clear()
    for a in soup.find_all('a', href=True):
        data_students_kurse[a.get_text()] = 'http://www.rating.unecon.ru/' + a.get('href')
    #выбираем группу
    return data_students_kurse.get(group)
sil1 = kurse_and_profile('2','Экономика','4',"Э-1801")
sil2 = kurse_and_profile('2','Экономика','4',"Э-1802")
sil3 = kurse_and_profile('2','Экономика','4',"Э-1803")
sil4 = kurse_and_profile('2','Экономика','4',"Э-1804")
spic1 = main("gdfgdf",sil1)
spic2 = main("gdfgdf",sil2)
spic3 = main("gdfgdf",sil3)
spic4 = main("gdfgdf",sil4)
pm16 = 0
for i in spic1:
    pm16+=int(i[5])
pm17 = 0
for i in spic2:
    pm17+=int(i[5])
pm18 = 0
for i in spic3:
    pm18+=int(i[5])
pm19 = 0
for i in spic4:
    pm19+=int(i[5])
print(pm16/len(spic1))
print(pm17/len(spic2))
print(pm18/len(spic3))
print(pm19/len(spic4))

