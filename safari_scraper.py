import re
import requests
import pprint
import pdfkit
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def getLinks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    parents = soup.find_all(class_ = 'toc-level-1 t-toc-level-1')
    
    links = []
    # base = "https://www.safaribooksonline.com"

    for parent in parents:
        # cur_link = base + parent.find('a').get('href')
        cur_link = parent.find('a').get('href')
        links.append(cur_link)

    return links

def linksToPdf(url, links):
    browser = webdriver.Firefox()

    base = "https://www.safaribooksonline.com"

    names = []
    
    for idx, link in enumerate(links):
        browser.get(base + link)

        #sign in
        try:
            link_elem = browser.find_element_by_class_name('t-sign-in')
            link_elem.click()
            remember = browser.find_element_by_name('remember')
            remember.click()
            # CHANGE CREDENTIALS HERE
            email_elem = browser.find_element_by_id('id_email')
            email_elem.send_keys('Your username/email')
            pass_elem = browser.find_element_by_id('id_password1')
            pass_elem.send_keys('Your password')
            pass_elem.submit()
        except:
            pass

        delay = 10

        if idx == 0:
            element_present = EC.presence_of_element_located((By.ID, 'preface'))
            chapter = WebDriverWait(browser, delay).until(element_present)
        else:
            try:
                chapter = browser.find_element_by_class_name('chapter')    
            except:
                chapter = browser.find_element_by_class_name('annotator-wrapper')

        html = chapter.get_attribute('innerHTML')
        name = link.split('/')[-1].split('#')[0]
        print(name)
        names.append(name)
        file = open(name, 'w')
        file.write(html)
        file.close()
    
    pdfkit.from_file(names, 'out.pdf')


if __name__ == '__main__':
    url = input("Enter the url of the book to scrape: ")

    links = getLinks(url)
    pprint.pprint(links)

    linksToPdf(url, links)
