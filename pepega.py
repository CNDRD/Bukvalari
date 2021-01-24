from bs4 import BeautifulSoup
from requests import Session
import json, os


def main():

    BAKAWEB_URL = 'https://bakaweb.cichnovabrno.cz/login'
    MARKS_URL = 'https://bakaweb.cichnovabrno.cz/next/prubzna.aspx'

    USERNAME = getLogin("Username")
    PASSWORD = getLogin("Password")
    print()

    LOGIN_DATA = {'username':USERNAME,'password':PASSWORD,'returnUrl':'/next/prubzna.aspx','login':''}

    with Session() as s:
        try:
            s.post(BAKAWEB_URL, LOGIN_DATA)
            dashboard = s.get(MARKS_URL)
            soup = BeautifulSoup(dashboard.content, 'html.parser')
            subjectsDiv = soup.find("div", {"id":"predmety"})
            subjects = subjectsDiv.find_all("div", {"class":"predmet-radek"})

            total_subjects = 0
            total_subj_marks = 0

            for p in subjects:
                name = p.find("h3").get_text()
                all_marks_divs = p.find_all('div',{'class':'znamka-v'})

                avg, NS, AS = getAvg(all_marks_divs)
                print(f"{name} -> {avg}{NS}{AS}")

                total_subjects += 1
                total_subj_marks += avg

            print(f"\nTotal average is {round(total_subj_marks / total_subjects, 2)}")

        except:
            print('\nSomehting went wrong.. Check the login credentials and try again')
            print(f"Login credentials: UN: '{USERNAME}' & PW: '{PASSWORD}'")
        input()


def getLogin(a):
    lgn = input(f'{a}: ')
    while lgn == '':
        lgn = input(f'{a}: ', end='\r')
    return lgn


def getAvg(all_marks_divs):
    _N = 0
    _A = 0
    all_marks = 0
    all_weights = 0

    for zn in all_marks_divs:
        data_clasif = zn.get('data-clasif')
        dcJson = json.loads(data_clasif)
        mark = dcJson['MarkText']
        weight = dcJson['vaha']

        if mark == 'A':
            _N += 1
            continue
        elif mark == 'N':
            _A += 1
            continue

        mark = mark.replace('-','.5')
        all_marks = all_marks + (float(mark) * int(weight))
        all_weights = all_weights + int(weight)

    avg = round(all_marks / all_weights, 2)
    NS = '' if _N == 0 else f' ({_N}x N)'
    AS = '' if _A == 0 else f' ({_A}x A)'

    return avg, NS, AS


if __name__ == '__main__':
    main()
