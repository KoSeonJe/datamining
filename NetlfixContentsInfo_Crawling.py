from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import pandas as pd

def getTitle() :
    title = soup.select_one('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-3.frxYSZ > div.sc-b7c53eda-0.dUpRPQ > h1 > span')
    #__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-3.frxYSZ > div.sc-b7c53eda-0.dUpRPQ > h1 > span
    if(title != None) :
        title = title.text
    return title

def getContentType() :
    # ul.ipc-inline-listipc-inline-list--show-dividerssc-d8941411-2cdJsTzbaseAlt > 
    temp = soup.select_one('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-3.frxYSZ > div.sc-b7c53eda-0.dUpRPQ > ul > li:nth-child(1)')
    if(temp != None) :
         temp = temp.text
         if(temp != 'TV Series') :
            temp = None
    return temp

def getRated() :
    rated = soup.select_one('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-3.frxYSZ > div.sc-b7c53eda-0.dUpRPQ > ul > li:nth-child(3) > a')
    if(rated != None) :
        rated = rated.text
    return rated

def getGenres() :
    temps = soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > div.sc-92625f35-10.dwKwMe > section > div.ipc-chip-list--baseAlt.ipc-chip-list > div.ipc-chip-list__scroller > a')
    if(temps != None) :
        genres = [genre.text for genre in temps]
        genre_str = ', '.join(genres)
    return genre_str

def getGrade() :
    temp = soup.select_one('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > div.sc-92625f35-11.eyxQlE > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-5.cxlubq > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK')
    if(temp == None) :
        temp = soup.select_one('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > section > div:nth-child(5) > section > section > div.sc-92625f35-4.iDcoFI > div.sc-92625f35-6.gHKhNg > div.sc-92625f35-11.eyxQlE > div.sc-3a4309f8-0.bjXIAP.sc-b7c53eda-5.cxlubq > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK')
        if(temp == None) :
            return temp
        else :
            temp = temp.text
    else :
        temp = temp.text
    return temp

def getActor() :
    list = soup.select('li[data-testid="title-pc-principal-credit"]')
    filtered_action_temp = []
    if list :
        for title in list :
            if(title.select_one('a').text == 'Stars') :
                action_temp = title.select('div > ul > li > a')
                filtered_action_temp = [a for a in action_temp if a.text != 'Stars']    
    return filtered_action_temp

def getDirector() :
    title_list = soup.select('li[data-testid="title-pc-principal-credit"]')

    director_temp = []
    if title_list :
        for direct in title_list :
            if(direct.select_one('span') is not None) :
                if(direct.select_one('span').text == 'Director') :
                    temp = direct.select('div.ipc-metadata-list-item__content-container a')[0].text
                    director_temp.append(temp)
            if(direct.select_one('a') is not None) :
                if(direct.select_one('a').text == 'Creator') :
                    temp = direct.select('div.ipc-metadata-list-item__content-container a')[0].text
                    director_temp.append(temp)
    if(director_temp == []) :
        return None
    return director_temp[0]

def getReleaseDate() :
    temps = soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section[data-testid="Details"] > div.sc-f65f65be-0.bBlII > ul > li')
    aTemp = None
    spanTemp = None
    for temp in temps :
        aTemp = temp.select('a')
        spanTemp = temp.select('span')
        if(aTemp is not None) :
            for a in aTemp :
                if(a.text == "Release date") :
                    return temp.select('div.ipc-metadata-list-item__content-container a')[0].text
        if(spanTemp is not None) :
            for span in spanTemp :
                if(span.text == "Release date") :
                    return temp.select('div.ipc-metadata-list-item__content-container a')[0].text
def getDetails(title) :
    temps = soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section[data-testid="Details"] > div.sc-f65f65be-0.bBlII > ul > li')
    aTemp = None
    spanTemp = None
    for temp in temps :
        aTemp = temp.select('a')
        spanTemp = temp.select('span')
        if(aTemp is not None) :
            for a in aTemp :
                if(a.text == title) :
                    return temp.select_one('div > ul > li > a').text
        if(spanTemp is not None) :
            for span in spanTemp :
                if(span.text == title) :
                    return temp.select_one('div > ul > li > a').text

def getCompany() :
    temps = soup.select('#__next > main > div > section.ipc-page-background.ipc-page-background--base.sc-304f99f6-0.fSJiHR > div > section > div > div.sc-978e9339-1.ihWZgK.ipc-page-grid__item.ipc-page-grid__item--span-2 > section[data-testid="Details"] > div.sc-f65f65be-0.bBlII > ul > li')
    aTemp = None
    spanTemp = None
    companies = None
    company_str = None
    for temp in temps :
        aTemp = temp.select('a')
        spanTemp = temp.select('span')
        if(aTemp is not None) :
            for a in aTemp :
                if(a.text == 'Production companies' or a.text == 'Production company') :
                    companies = temp.select('div > ul > li > a')
        if(spanTemp is not None) :
            for span in spanTemp :
                if(span.text == 'Production companies'or a.text == 'Production company') :
                    companies = temp.select('div > ul > li > a')
    if companies:
        companies_filtering = []
        for company in companies :
            if company.text != 'Production companies' and company.text != 'Production company' :
                companies_filtering.append(company.text)
        if(companies_filtering != []) :
            company_str = ', '.join(companies_filtering)
    return company_str

df = pd.read_excel('netflix_watched.xlsx', engine='openpyxl')
df.columns = ['blank', 'Title', 'Globally', 'date', 'viewed']
keywords = df['Title'].tolist()

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
url = "https://www.imdb.com/?ref_=nv_home"

wb = Workbook()
ws1 = wb.active
ws1.title = "넷플릭스 콘텐츠 정보"
col = ['origin_keyword','title', 'content_type','rated','genre', 'grade', 'actor1','actor2', 'director', 'released_date','country','language','company','running_time']
ws1.append(col)

for keyword in keywords :
    print(keyword)
    driver.get(url)
    time.sleep(1)
    search_box = driver.find_element(By.ID, "suggestion-search")
    search_button = driver.find_element(By.ID, "suggestion-search-button")

    if '//' in keyword:
        keyword = keyword.split('//')[0]

    if ':' in keyword:
        if('Season' in keyword.split(':')[1] or 'Series' in keyword.split(':')[1]) :
            keyword = keyword.split(':')[0]
    
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)
    try:
        search_first = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[1]/div[2]/div/a')
        search_first_text = search_first.text
        if(search_first == None) :
            continue
        search_first.click()
    except NoSuchElementException:
        pass

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    title = getTitle()
    print('제목--', end="")
    print(title)
    content_type = getContentType()
    print('컨텐츠 종류--', end="")
    print(content_type)
    rated = getRated()
    print('연령 등급--', end="")
    print(rated)
    genres = getGenres()
    print('장르--', end="")
    print(genres)
    grade = getGrade()
    print('평점--', end="")
    print(grade)
    actors = getActor()
    if(actors != []) :
        actor1 = actors[0].text
    else :
        actor1 = None
    print('배우1--', end="")
    print(actor1)
    if(actors != []) :
        actor2 = actors[1].text
    else :
        actor2 = None
    print('배우2--', end="")
    print(actor2)
    director = None
    if getDirector():
        director = getDirector()
    print('감독--', end="")
    print(director)

    time.sleep(1)

    release_date = getReleaseDate()
    print('출시일--', end="")
    print(release_date)
    country = getDetails('Country of origin')
    print('국가--', end="")
    print(country)
    language = getDetails('Language')
    print('언어--', end="")
    print(language)
    company = getCompany()
    print('제작사--', end="")
    print(company)
    print('========================================')
    row = pd.DataFrame({
        'origin_keyword' : [keyword],
        'title': [title],
        'content_type': [content_type],
        'rated': [rated],  
        'genre': [genres],
        'grade': [grade],
        'actor1': [actor1],
        'actor2': [actor2],
        'director': [director],
        'released_date': [release_date],
        'country': [country],
        'language': [language],
        'company': [company],
        'running_time': [None]
    }, columns=col)   
    row_list = row.iloc[0].tolist()
    ws1.append(row_list)
    wb.save(filename='넷플릭스 콘텐츠 정보.xlsx')
driver.quit()

# workbook = Workbook()
# sheet1 = workbook.active
# sheet1.title = "넷플릭스 콘텐츠 정보"

# 제목, 콘텐츠 종류, 연령등급, 러닝타임(드라마라면? 에피소드 개수?), 장르, 평점, 배우 두명, 감독, 출시 일, 국가, 언어, 제작사

