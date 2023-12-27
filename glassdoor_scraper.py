from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import progressbar

def get_position_links(url):
    '''
    This function sends a request to Glassdoor, crawls links with class 'jobLink',
    and collects data science job application links on a single page.

    Args:
        url (str): The URL of the page.

    Returns:
        list: A list containing links for job applications on the page.
    '''
    links = []
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links with class 'jobLink' and construct full URLs
    job_links = soup.find_all('a', class_='jobLink')
    for link in job_links:
        links.append('https://www.glassdoor.com' + link.get('href'))

    return links

def get_all_links(num_pages, base_url):
    '''
    Collects all job application links from multiple pages.

    Args:
        num_pages (int): Number of pages to crawl.
        base_url (str): The base URL of a single page.

    Returns:
        list: A list of lists containing job application links.
    '''
    all_links = []
    i = 1
    print('Collecting links....')
    while i <= num_pages:
        try:
            # Construct the URL for the current page
            url_main = f'{base_url}{i}.htm'
            all_links.append(get_position_links(url_main))
            i += 1
            time.sleep(0.5)
        except:
            print('No more pages found.')
    return all_links

def scrape_job_page(url):
    '''
    Collects data from a single job application page and stores it in a dictionary.

    Args:
        url (str): The URL of a job application page.

    Returns:
        dict: A dictionary containing collected data.
    '''
    data_dict = {}
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')

    try:
        data_dict['job_title'] = body.find('h2', class_='noMargTop margBotXs strong').text.strip()
    except:
        data_dict['job_title'] = np.nan

    try:
        data_dict['company_name'] = body.find('span', class_='strong ib').text.strip()
    except:
        data_dict['company_name'] = np.nan

    try:
        location = body.find('span', class_='subtle ib').text.strip().replace('–\xa0', '')
        data_dict['location'] = location
    except:
        data_dict['location'] = np.nan

    try:
        data_dict['salary_estimated'] = body.find('h2', class_='salEst').text.strip()
    except:
        data_dict['salary_estimated'] = np.nan

    try:
        data_dict['salary_min'] = body.find('div', class_='minor cell alignLt').text.strip()
    except:
        data_dict['salary_min'] = np.nan

    try:
        data_dict['salary_max'] = body.find('div', class_='minor cell alignRt').text.strip()
    except:
        data_dict['salary_max'] = np.nan

    try:
        date = body.find('span', class_='minor nowrap').text.strip()
        # Parse and convert the date to a standardized format
        data_dict['date_posted'] = parse_date(date)
    except:
        data_dict['date_posted'] = datetime.today().date()

    list_skills = []
    job_des = body.find('div', class_='jobDesc')

    for li in job_des.find_all("li"):
        list_skills.append(li.text.strip())

    data_dict['job_description'] = list_skills

    return data_dict

def parse_date(date_str):
    '''
    Parses and converts the date string to a standardized format.

    Args:
        date_str (str): The date string to parse.

    Returns:
        datetime: A datetime object representing the parsed date.
    '''
    split = date_str.split(" ")
    if "second" in split or "seconds" in split or "minute" in split or "minutes" in split or "hours" in split or "hour" in split:
        return datetime.today().date()
    elif "week" in split or "weeks" in split:
        return (datetime.today() - (timedelta(days=int(split[0]) * 7))).date()
    elif "days" in split or "day" in split:
        return (datetime.today() - timedelta(days=int(split[0]))).date()
    elif "month" in date_str or "months" in date_str:
        return (datetime.today() - (timedelta(days=int(split[0]) * 30))).date()
    else:
        return datetime.today().date()

if __name__ == '__main__':
    # Specify the base URL for data science jobs on Glassdoor
    base_url = 'https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP'
    # Number of pages to crawl
    num_pages = 30

    # Collect all job application links
    links = get_all_links(num_pages, base_url)
    # Flatten the list of links and remove duplicates
    unique_links = list(set(item for sublist in links for item in sublist))

    # UI progress bar
    bar = progressbar.ProgressBar(maxval=len(unique_links), \
                                  widgets=['Crawling the site: ', progressbar.Bar('=', '[', ']'), ' ',
                                           progressbar.Percentage()])
    list_results = []

    for page in unique_links:
        bar.update(unique_links.index(page))
        try:
            list_results.append(scrape_job_page(page))
        except:
            pass
        time.sleep(0.5)

    # Save the data in a DataFrame
    df_glass = pd.DataFrame(list_results)

    # Save the DataFrame to an Excel file
    with pd.ExcelWriter('data_glassdoor.xlsx', engine='openpyxl') as writer:
        df_glass.to_excel(writer, index=False)
