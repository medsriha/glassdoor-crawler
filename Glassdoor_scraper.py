from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import progressbar


def get_position_link(url):

    links = []
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    a = soup.find_all('a', class_='jobLink')
    for i in a:
        links.append('https://www.glassdoor.com' + i.get('href'))

    return links


def get_all_links(num_page, url):
    link = []
    i = 1
    print('Collecting links....')
    while i <= num_page:
        try:
            url_main = url + str(i) + '.htm'
            link.append(get_position_link(url_main))
            i = i + 1
            time.sleep(0.5)
        except:
            print('No more pages found.')
    return link


def scrap_job_page(url):
    dic = {}
    br_list = []
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')
    #     print(title)

    try:
        #         job title
        dic['job_title'] = body.find('h2', class_='noMargTop margBotXs strong').text.strip()
    except:
        dic['job_title'] = np.nan

    try:
        # company name
        dic['company_name'] = body.find('span', class_='strong ib').text.strip()
    except:
        dic['company_name'] = np.nan

    try:
        # location
        location = body.find('span', class_='subtle ib').text.strip().replace('–\xa0', '')
        dic['location'] = location
    except:
        dic['location'] = np.nan


    try:
        dic['salary_estimated'] = body.find('h2', class_='salEst').text.strip()
    except:
        dic['salary_estimated'] = np.nan
    try:
        dic['salary_min'] = body.find('div', class_='minor cell alignLt').text.strip()
    except:
        dic['salary_min'] = np.nan
    try:

        dic['salary_max'] = body.find('div', class_='minor cell alignRt').text.strip()
    except:
        dic['salary_max'] = np.nan

    try:
        # date
        date = body.find('span', class_='minor nowrap').text.strip()
        split = date.split(" ")
        if "second" in split or "seconds" in split:
            dic["date_posted"] = datetime.today().date()
        if "minute" in split or "minutes" in split:
            dic["date_posted"] = datetime.today().date()
        if "hours" in split or "hour" in split:
            dic["date_posted"] = datetime.today().date()
        if "week" in split or "weeks" in split:
            dic["date_posted"] = (datetime.today() - (timedelta(days=int(split[0]) * 7))).date()
        if "days" in split or "day" in split:
            dic["date_posted"] = (datetime.today() - timedelta(days=int(split[0]))).date()
        if "month" in date or "months" in date:
            dic["date_posted"] = (datetime.today() - (timedelta(days=int(split[0]) * 30))).date()
    except:

        dic["date_posted"] = datetime.today().date()

    #     Job description
    list_skills = []
    job_des = body.find('div', class_='jobDesc')

    for i in job_des:
        try:
            for li in i.find_all("li"):
                list_skills.append(li.text.strip())
        except:
            break
    try:

        dic['job_description'] = list_skills
    except:
        dic['job_description'] = np.nan

    return dic


if __name__ == '__main__':

    links = get_all_links(30, 'https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP')
    flatten = [item for sublist in links for item in sublist]
    remove_duplicates = list(set(flatten))
    bar = progressbar.ProgressBar(maxval=len(remove_duplicates), \
                                  widgets=['Crawling the site: ', progressbar.Bar('=', '[', ']'), ' ',
                                           progressbar.Percentage()])
    list_result = []

    for page in remove_duplicates:
        bar.update(remove_duplicates.index(page))
        try:
            list_result.append(scrap_job_page(page))
        except:
            pass
        time.sleep(0.5)

    #Write into Excel
    df_glass = pd.DataFrame.from_dict(list_result)
    writer = pd.ExcelWriter('glassdoor position scraping.xlsx', engine='openpyxl')
    df_glass.to_excel(writer, index=False)
    df_glass.to_excel(writer, startrow=len(df_glass) + 2, index=False)
    writer.save()
