from bs4 import BeautifulSoup
from datetime import datetime, time

class SelfProfile:
    def __init__(self, page):
        account_soup = BeautifulSoup(page.content, 'lxml')
        user_info = account_soup.find('div', class_='account-info-container').find_all('div', class_="account-item")

        self.surname:     str = account_soup.find('input', id='LastName').get("value")
        self.name:        str = account_soup.find('input', id='FirstName').get("value")
        self.patronymic:  str = account_soup.find('input', id='MiddleName').get("value")
        self.email:       str = account_soup.find('input', id='Email').get("value")
        self.phone:       str = account_soup.find('input', id='Phone').get("value")
        self.type:        str = user_info[0].find('p', 'value').text
        self.reg_date         = datetime.strptime(user_info[1].find('p', 'value').text, "%d.%m.%Y")
        self.family_key:  str = user_info[2].find('p', 'value').text
        self.id:          str = user_info[3].find('p', 'value').text

class SelfSchedule:
    def __init__(self, page):
        account_soup = BeautifulSoup(page.content, 'lxml')
        schedule_info = account_soup.find('div', class_='diary')

        self.days = []

        for day in schedule_info.find_all('div', class_='diary-day'):
            day_lessons = []
            for lesson in day.find('table').find('tbody').find_all('tr'):
                task = lesson.find_all('td')[2].find('span')
                if task != None:
                    task = task.text
                day_lessons.append({
                    'start_time': lesson.find_all('td')[0].text,
                    'title':      lesson.find_all('td')[1].text,
                    'task':       task,
                    'theme':      lesson.find_all('td')[4].text,
                    'mark':       lesson.find_all('td')[5].text
                })
            self.days.append(day_lessons)


class SelfFinalMarks:
    def __init__(self, page):
        soup = BeautifulSoup(page.content, 'lxml')
        marks_info = soup.find('tbody').find_all('tr')

        self.first_quarter =  {}
        self.second_quarter = {}
        self.third_quarter =  {}
        self.fourth_quarter = {}
        self.year =           {}

        for tr in marks_info:
            tds = tr.find_all('td')
            name = tds[0].text
            mark1 = None if tds[1].text.replace('\n                                ', '').replace('    ', '') == '-' else tds[1].text.replace('\n                                ', '').replace('    ', '')
            mark2 = None if tds[2].text.replace('\n                                ', '').replace('    ', '') == '-' else tds[2].text.replace('\n                                ', '').replace('    ', '')
            mark3 = None if tds[3].text.replace('\n                                ', '').replace('    ', '') == '-' else tds[3].text.replace('\n                                ', '').replace('    ', '')
            mark4 = None if tds[4].text.replace('\n                                ', '').replace('    ', '') == '-' else tds[4].text.replace('\n                                ', '').replace('    ', '')
            mark5 = None if tds[5].text.replace('\n                                ', '').replace('    ', '') == '-' else tds[5].text.replace('\n                                ', '').replace('    ', '')
            self.first_quarter .update({name: mark1})
            self.second_quarter.update({name: mark2})
            self.third_quarter .update({name: mark3})
            self.fourth_quarter.update({name: mark4})
            self.year          .update({name: mark5})