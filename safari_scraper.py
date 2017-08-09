import requests
import pprint
import pdfkit
from selenium import webdriver
from bs4 import BeautifulSoup

def getLinks(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    parents = soup.find_all(class_ = 'toc-level-1 t-toc-level-1')
    
    links = []
    base = "https://www.safaribooksonline.com"

    for parent in parents:
        cur_link = base + parent.find('a').get('href')
        links.append(cur_link)

    return links

def linksToPdf(links):
    browser = webdriver.Firefox()
    
    browser.get(link[0])

    sign_in_url = browser.find_element_by_class_name('t-sign-in').get_attribute('href')
    print(sign_in_url)
    

if __name__ == '__main__':
    url = input("Enter the url of the book to scrape: ")

    links = getLinks(url)
    pprint.pprint(links)

    linksToPdf(links)    
