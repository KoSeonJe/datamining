from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import pandas as pd
import re

netflix_info = pd.read_excel('modified_dates_netflix.xlsx', engine='openpyxl')

netflix_info_df = pd.DataFrame(netflix_info)

titles = netflix_info_df['title']

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.fullscreen_window()
url = "https://www.imdb.com/?ref_=nv_home"
wb = Workbook()
ws1 = wb.active
ws1.title = "배우,감독,제작사,넷플릭스 오리지널 여부 정보"
col = ['actor1_awards, actor1_work_number, actor2_awards, actor2_work_number,actor3_awards, actor3_work_number director_awards, director_work_number, company_work_number, company_work_review_number, isNetflixOriginal']
ws1.append(col)

isFirst = True

def getActor(list) :
    filtered_action_temp = []
    if list :
        for title in list :
            if(title.select_one('a').text == 'Stars') :
                action_temp = title.select('div > ul > li > a')
                filtered_action_temp = [a for a in action_temp if a.text != 'Stars']    
    return filtered_action_temp

def getActor1Info(actor, driver) :
    if actor:
    # 선택한 요소의 href 속성 가져오기
        href = actor.get('href')
        if href:
            # 셀레니움으로 해당 href를 가진 a 태그 클릭하기
            actor1_element = driver.find_element(By.XPATH, f'//a[@href="{href}"]')
            actor1_element.send_keys(Keys.ENTER)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    actorInfo = []

    awards = soup.select_one('li[data-testid = "award_information"]')
    if(awards is not None) :
        awards_total = awards.select_one("div > ul > li > span")
        numbers = re.findall(r'\d+', awards_total.text)
        # 찾아낸 숫자들을 정수로 변환하여 더함
        total = sum(map(int, numbers))
        actorInfo.append(total)
    else :
        actorInfo.append(None)
    actor_workNumber = soup.select_one('#actor-previous-projects > div.ipc-accordion__item__header.ipc-accordion__item__header--sticky > label > span.ipc-accordion__item__title > ul > li.ipc-inline-list__item.credits-total')
    if(actor_workNumber is not None) :
        actor_workNumber = int(actor_workNumber.text)
    actress_workNumber = soup.select_one('#actress-previous-projects > div.ipc-accordion__item__header.ipc-accordion__item__header--sticky > label > span.ipc-accordion__item__title > ul > li.ipc-inline-list__item.credits-total')
    if(actress_workNumber is not None) :
        actress_workNumber = int(actress_workNumber.text)
    
    if(actor_workNumber is not None and actress_workNumber is not None) :
        actorInfo.append(max(actor_workNumber,actress_workNumber))
    elif (actor_workNumber is not None) :
        actorInfo.append(actor_workNumber)
    elif (actress_workNumber is not None) :
        actorInfo.append(actress_workNumber)
    return actorInfo

def getDirector(title_list) :
    director_temp = []
    if title_list :
        for direct in title_list :
            if(direct.select_one('span') is not None) :
                if(direct.select_one('span').text == 'Director' or direct.select_one('span').text == 'Directors') :
                    temp = direct.select('div.ipc-metadata-list-item__content-container a')[0]
                    director_temp.append(temp)
            if(direct.select_one('a') is not None) :
                if(direct.select_one('a').text == 'Creator' or direct.select_one('a').text == 'Creators') :
                    temp = direct.select('div.ipc-metadata-list-item__content-container a')[0]
                    director_temp.append(temp)
    if(director_temp == []) :
        return None
    return director_temp[0]

def getDirectorInfo(director, driver) :
    if director:
    # 선택한 요소의 href 속성 가져오기
        href = director.get('href')
        if href:
            # 셀레니움으로 해당 href를 가진 a 태그 클릭하기
            director_element = driver.find_element(By.XPATH, f'//a[@href="{href}"]')
            director_element.send_keys(Keys.ENTER)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    directorInfo = []
    awards = soup.select_one('li[data-testid = "award_information"]')
    if(awards is not None) : 
        awards_total = awards.select_one("div > ul > li > span")
        numbers = re.findall(r'\d+', awards_total.text)
        # 찾아낸 숫자들을 정수로 변환하여 더함
        total = sum(map(int, numbers))
        directorInfo.append(total)
    else :
        directorInfo.append(None)
    
    direct_workNumber = soup.select_one('#director-previous-projects > div.ipc-accordion__item__header.ipc-accordion__item__header--sticky > label > span.ipc-accordion__item__title > ul > li.ipc-inline-list__item.credits-total')
    if(direct_workNumber is not None) :
        direct_workNumber = int(direct_workNumber.text)
    produce_workNumber = soup.select_one('#producer-previous-projects > div.ipc-accordion__item__header.ipc-accordion__item__header--sticky > label > span.ipc-accordion__item__title > ul > li.ipc-inline-list__item.credits-total')
    if(produce_workNumber is not None) :
        produce_workNumber = int(produce_workNumber.text)
    if(direct_workNumber is not None and produce_workNumber is not None) :
        value = max(direct_workNumber, produce_workNumber)
        directorInfo.append(value)
    elif (direct_workNumber is not None) :
        directorInfo.append(direct_workNumber)
    elif (produce_workNumber is not None) :
        directorInfo.append(produce_workNumber)
    else :
        directorInfo.append(None)
    return directorInfo

def getCompany(temps) :
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
                if(span.text == 'Production companies'or span.text == 'Production company') :
                    companies = temp.select('div > ul > li > a')
    # if companies:
    #     companies_filtering = []
    #     for company in companies :
    #         if company.text != 'Production companies' and company.text != 'Production company' :
    #             companies_filtering.append(company.text)
    #     if(companies_filtering != []) :
    #         company_str = ', '.join(companies_filtering)
    return companies[1]

def convert_to_number(count_text) :
    if 'K' in count_text:
        return int(float(count_text.replace('K', '')) * 1000)
    elif 'M' in count_text:
        return int(float(count_text.replace('M', '')) * 1000000)
    return int(count_text)

def getCompanyInfo(company, driver, index) :
    company_info = []
    if company:
    # 선택한 요소의 href 속성 가져오기
        href = company.get('href')
        if href:
            # 셀레니움으로 해당 href를 가진 a 태그 클릭하기
            # company_element = driver.find_element(By.XPATH, f'//a[@href="{href}"]')
            try :
                element = driver.find_element(By.XPATH, f'//a[@href="{href}"]')
                page = driver.find_element(By.CSS_SELECTOR, 'section[data-testid = "Details"]')
                driver.execute_script("arguments[0].scrollIntoView(true);", page)
                time.sleep(3)
                element.send_keys(Keys.ENTER)
            except :
                company_info.append(None)
                company_info.append(None)
                return company_info
            # 페이지 로딩 대기 시간 설정 (필요시 조정)

    released_dates = netflix_info_df['released_date']
    date = released_dates[index]
    year = date.year
    month = date.month
    release_year = str(year)+"-"+str(month)
    year = date.year-3
    past_year = str(year)+"-"+str(month)
    button = driver.find_element(By.CSS_SELECTOR, 'label[data-testid="accordion-item-releaseDateAccordion"]')
    button.send_keys(Keys.ENTER)
    start = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="releaseYearMonth-start"]')
    end = driver.find_element(By.CSS_SELECTOR, 'input[data-testid="releaseYearMonth-end"]')
    start.send_keys(past_year)
    end.send_keys(release_year)
    end.send_keys(Keys.RETURN) 
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    work_number = soup.select_one('#__next > main > div.ipc-page-content-container.ipc-page-content-container--center.sc-eb36f92a-0.bFWJaa > div.ipc-page-content-container.ipc-page-content-container--center > section > section > div > section > section > div:nth-child(2) > div > section > div.ipc-page-grid.ipc-page-grid--bias-left.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > div.sc-e3ac1175-6.kgkwWN > div.sc-e3ac1175-3.gJQFCa')
    if(work_number is not None) :
        match = re.search(r'([\d,]+)$', work_number.text)
        company_info.append(match.group(1))
    else :
        company_info.append(None)

    review_counts = soup.select('.ipc-rating-star--voteCount')
    review_counts = review_counts[:10]
    total_reviews = 0
    for review_count in review_counts:
        count_text = review_count.get_text()  # 리뷰 개수 텍스트 추출
        matches = re.search(r'\((.*?)\)', count_text)
        total_reviews += convert_to_number(matches.group(1))
    company_info.append(total_reviews)
    return company_info

def getIsNetflix(temps, driver) :
    aTemp = None
    spanTemp = None
    sites = None
    flag= False
    for temp in temps :
        aTemp = temp.select('a')
        spanTemp = temp.select('span')
        if(aTemp is not None) :
            for a in aTemp :
                if(a.text == 'Official sites' or a.text == 'Official site') :
                    sites = temp.select('div > ul > li > a')
        if(spanTemp is not None) :
            for span in spanTemp :
                if(span.text == 'Official sites'or span.text == 'Official site') :
                    sites = temp.select('div > ul > li > a')

    if(sites is None) :
        return flag
    
    for site in sites :
        if("Netflix" in site.text) :
            flag = True
            break
    # if companies:
    #     companies_filtering = []
    #     for company in companies :
    #         if company.text != 'Production companies' and company.text != 'Production company' :
    #             companies_filtering.append(company.text)
    #     if(companies_filtering != []) :
    #         company_str = ', '.join(companies_filtering)
    return flag


def clickSource(driver, index) :
    # try:
    #     #__next > main > div.ipc-page-content-container.ipc-page-content-container--full.sc-eb36f92a-0.bFWJaa > div.ipc-page-content-container.ipc-page-content-container--center > section > div > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(4) > div.sc-ffc93fc1-2.ditJlF > ul > li:nth-child(1) > div.ipc-metadata-list-summary-item__c > div > a
    #     print("실행")
    #     if(search_first == None) :
    #         return
    # except NoSuchElementException:
    #     pass  
    search_first = driver.find_element(By.CSS_SELECTOR, '#__next > main > div.ipc-page-content-container.ipc-page-content-container--full.sc-eb36f92a-0.bFWJaa > div.ipc-page-content-container.ipc-page-content-container--center > section > div > div.ipc-page-grid__item.ipc-page-grid__item--span-2 > section:nth-child(4) > div.sc-ffc93fc1-2.ditJlF > ul > li > div.ipc-metadata-list-summary-item__c > div > a')
    search_first.send_keys(Keys.ENTER)
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    list = soup.select('li[data-testid="title-pc-principal-credit"]')
    actor = getActor(list)
    actor1_info = getActor1Info(actor[0], driver)
    print("actor1_info")
    print(actor1_info[0])
    print(actor1_info[1])
    driver.back()
    actor2_info = getActor1Info(actor[1], driver)
    print("actor2_info")
    print(actor2_info[0])
    print(actor2_info[1])
    driver.back()
    print("actor3_info")
    actor3_info = [None, None]
    if(actor[2] is not None) :
        actor3_info = getActor1Info(actor[2], driver)
        print(actor3_info[0])
        print(actor3_info[1])
        driver.back()
    title_list = soup.select('li[data-testid="title-pc-principal-credit"]')
    director = getDirector(title_list)
    director_info = getDirectorInfo(director, driver)
    print("director_info")
    print(director_info[0])
    print(director_info[1])
    driver.back()
    
    temps = soup.select('li[data-testid="details-officialsites"]')
    isNetflixOriginal = getIsNetflix(temps, driver)
    print("isNetflixOriginal")
    print(isNetflixOriginal)
    temps = soup.select('li[data-testid="title-details-companies"]')
    company = getCompany(temps)
    company_info = getCompanyInfo(company,driver, index)
    print("company_info")
    print(company_info[0])
    print(company_info[1])

    row = pd.DataFrame({
        'actor1_awards' : [actor1_info[0]],
        'actor1_work_number' : [actor1_info[1]],
        'actor2_awards' : [actor2_info[0]],
        'actor2_work_number' : [actor2_info[1]],
        'actor3_awards' : [actor3_info[0]],
        'actor3_work_number' : [actor3_info[1]],
        'director_awards' : [director_info[0]],
        'director_work_number' : [director_info[1]],
        'company_work_number' : [company_info[0]],
        'company_work_review_number' : [company_info[1]],
        'isNetflixOriginal' : [isNetflixOriginal]
    })
    row_list = row.iloc[0].tolist()
    ws1.append(row_list)
    wb.save(filename='actor,director,company_score.xlsx')


for index, title in enumerate(titles) :
    if(isFirst) :
        driver.get(url)
        search_box = driver.find_element(By.ID, "suggestion-search")
        search_button = driver.find_element(By.ID, "suggestion-search-button")
        search_box.send_keys(title)
        search_box.send_keys(Keys.RETURN)
        clickSource(driver, index)
        isFirst = False
        continue
    search_box = driver.find_element(By.ID, "suggestion-search")
    search_button = driver.find_element(By.ID, "suggestion-search-button")
    search_box.send_keys(title)
    search_box.send_keys(Keys.RETURN)
    clickSource(driver, index)   
    
