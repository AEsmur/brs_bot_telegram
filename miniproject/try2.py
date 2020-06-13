import requests
from bs4 import BeautifulSoup
import numpy as np
def all_spic(name_student):
    vgm_url = 'http://www.rating.unecon.ru/rating.php?&f=1&p=12684&is_rating_vipusk=0&y=2018&y_vipusk=2020&s=none'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data_students_kurse = []
    i = 0
    for a in soup.find_all('a', href=True):
        if i < 6:
            data_students_kurse.append([a.get_text(),  'http://www.rating.unecon.ru/' + a.get('href')])
        else:
            break
        i += 1
    data_students_N = []
    for i in data_students_kurse[2::]:
        vgm_url = i[1]
        html_text = requests.get(vgm_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        i = 0
        for a in soup.find_all('a', href=True):
            if name_student in a.get_text():
                data_students_N.append([a.get_text() ,'http://www.rating.unecon.ru/' + a.get('href')])
    print(data_students_N)
