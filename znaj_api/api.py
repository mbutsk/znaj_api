from bs4 import BeautifulSoup
import requests
from .classes import *
from .errors import *

class Session():
    def __init__(self, username, password):
        self.login(username, password)
    
    def login(self, username, password):
        self.session = requests.Session()

        # Ваши данные для авторизации
        payload = {
            'UserName': username,
            'Password': password
        }
        # Авторизация
        login_url = 'https://znaj.by/Account/LogOnInternalWithIpay'
        answ = self.session.post(login_url, data=payload)
        errors = eval(BeautifulSoup(answ.content, 'lxml').find('p').text.replace('null', "None").replace('true', 'True').replace('false', 'False'))['ErrorMessages']
        
        
        if errors == None: pass
        elif 'Неверный логин или пароль' in errors: raise InvalidCredentials('Login or password you provided are incorrect.')
        else: raise UnknownException(errors)
    
    def get_profile(self):
        if self.session != None:
            account_page = self.session.get('https://znaj.by/Account')
            return SelfProfile(account_page)
        else:
            raise SessionClosed('Session is closed, use login() to login')
    
    def get_schedule(self):
        if self.session != None:
            account_page = self.session.get('https://znaj.by/Client')
            return SelfSchedule(account_page)
        else:
            raise SessionClosed('Session is closed, use login() to login')
    
    def get_final_marks(self, SchoolId: str, ClassId: str, YearStart: int, PupilId: int):
        page = self.session.get(f'https://znaj.by/Client/GetPupilDiaryLastPage?SchoolId={SchoolId}&ClassId={ClassId}&YearStart={YearStart}&PupilId={PupilId}&X-Requested-With=XMLHttpRequest')
        page_soup = BeautifulSoup(page.content, 'lxml')
        error = page_soup.find('p')
        if error == None:
            return SelfFinalMarks(page)
        elif error.text == 'Извините, произошла ошибка, обратитесь к классному руководителю или в службу поддержки.':
            raise UnknownException('An error occurred, please contact your class teacher or support service.')
        elif error.text == 'Вам запрещен доступ к данному ребенку':
            raise AccessDenied('You are denied access to this child')
    
    def close(self):
        if self.session != None:
            self.session.close()
            self.session = None
        else:
            raise SessionClosed('Session is alredy closed.')
