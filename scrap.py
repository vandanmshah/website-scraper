from bs4 import BeautifulSoup
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# import urllib2
import re

# import requests
import re
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def init_driver():
    path_to_chromedriver = '/chromedriver/chromedriver' # change path as needed
    driver = webdriver.Chrome(executable_path = path_to_chromedriver)
    driver.wait = WebDriverWait(driver, 5)
    return driver
def get_all_links(url,driver):
    list_of_links = []
    selen_html = driver.page_source
    soup = BeautifulSoup( selen_html)
    list_of_links=[]
    for link in soup.find_all('a', href=True):
        list_of_links.append(link['href'])
    list_of_links=list(set(list_of_links))
    return list_of_links

def reduce_list(temp_list):   # This functions removes extra spaces and remove duplicates from list
    for x in xrange(0,len(temp_list)):
        temp_list[x] = temp_list[x].strip()
    temp_list = list(set(temp_list))
    return temp_list
def lookup(driver, query,url):
    try:
        html_links=[url]
        list_search = []
        list_mobile_numbers = []
        pos = list_duplicates_of(url, '/')
        start_pos = pos[1] + 1
        end_pos = len(url)
        if(len(pos)>2):
            end_pos = pos[2]
        print url[start_pos:end_pos]
        f = open(url[start_pos:end_pos], 'w')
        f.write('Emails srcraped from :- ' + url + "\nList of Emails and mobile numbers we have got :-\n")
        for x in html_links:
            print "Scraping E-Mails from :- " + x
            driver.get(x)
            list_of_links = []
            list_of_links = get_all_links(x, driver)

            indices = [i for i, x in enumerate(list_of_links) if re.search(r'[-a-zA-Z0-9@:%._\+~#=/]{2,256}\.[(html)(aspx)(php)]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', x)]
            for x in xrange(0,len(list_of_links)):  # if there is like another domain linked to given url then we have to find all http links
                if('http' in list_of_links[x]):
                    temp_match = re.findall( r'[-a-zA-Z0-9@:%._\+~#=/]{2,256}\.[(html)(aspx)(php)]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',list_of_links[x])
                    if temp_match:
                        if(url in list_of_links[x]):
                            indices.append(x)
            indices1 = [i for i, x in enumerate(list_of_links) if re.search(r'[http:]*[/]+[?=\w._@/-]*', x)]
            for g in indices1:
                if("http" in list_of_links[g]):
                    # temp_match = re.findall( r'[-a-zA-Z0-9@:%._\+~#=/]{2,256}\.[(html)(aspx)(php)]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',list_of_links[g])
                    # if temp_match:    
                    if (url in list_of_links[g] ):
                        if((list_of_links[g]) not in html_links):
                            html_links.append(list_of_links[g])
                elif ((url + "/" + list_of_links[g]) not in html_links):    
                 # elif :
                    temp_match = re.findall( r'[-a-zA-Z0-9@:%._\+~#=/]{2,256}\.[(html)(aspx)(php)]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',list_of_links[g])
                    if temp_match: 
                        index = 0
                        # print "--------------	-------------------------------"

                        current_url = driver.current_url
                        list_of_occour = [] 
                        while index < len(current_url):
                            index = current_url.find('/', index)
                            if index == -1:
                                break
                            list_of_occour.append(index)
                            index += 1
                        end_posi = len(current_url)
                        if(len(list_of_occour)>2):
                            end_posi = list_of_occour[2]
                        html_links.append(current_url[0:end_posi] + "/" + list_of_links[g])
            for x in indices:
                if("http" in list_of_links[x]):
                    if (url in list_of_links[x] ):
                        temp_match = re.findall( r'\s[^@\s]+@[a-zA-Z]+\.[a-zA-Z.]*',list_of_links[x])
                        if temp_match:
                            if((list_of_links[x]) not in html_links):
                            # print list_of_links[x] + "------------------"
                                html_links.append(list_of_links[x])
                elif ((url + "/" + list_of_links[x]) not in html_links):   
                    index = 0
                    current_url = driver.current_url
                    list_of_occour = [] 
                    while index < len(current_url):
                        index = current_url.find('/', index)
                        if index == -1:
                            break
                        list_of_occour.append(index)
                        index += 1
                    end_posi = len(current_url)
                    if(len(list_of_occour)>2):
                        end_posi = list_of_occour[2] 
                    html_links.append(current_url[0:end_posi] + "/" + list_of_links[x])
            del list_of_links
            
            time.sleep(2)
            selen_html = driver.page_source
            matchObj1 = re.sub( r'<[^>]*>',' ',selen_html)
            matchObj = re.findall( r'\s[^@\s]+@[a-zA-Z]+\.[a-zA-Z.]*',matchObj1)
            matchObj_mobile_number = re.findall( r'[+]*\b\d{3}[-.]?\d{3}[-.]?\d{4,7}\b',matchObj1)
            if matchObj_mobile_number:
                print "\tVoila got " + str(len(matchObj_mobile_number)) + " mobile numbers from this web page...\n"
                for z in matchObj_mobile_number:                    
                    z.strip()
                    f.write(z + "\n")
                    list_mobile_numbers.append(z)    
            if matchObj:
                print "\tVoila got " + str(len(matchObj)) + " E-Mails from this web page...\n"
                for z in matchObj:
                    f.write(z + "\n")
                    list_search.append(z)
        f.close()
        f = open(url[start_pos:end_pos], 'w')
        # f.seek(0, 0)
        f.write('Emails srcraped from :- ' + url + "\nList of Emails and mobile numbers we have got :-\n")
        list_search = reduce_list(list_search) 
        list_mobile_numbers = reduce_list(list_mobile_numbers)   
        print "\nTotal searched pages :- " + str(len(html_links))
        print "Total scraped E-Mails :- " + str(len(list_search))
        print "Total scraped Mobile numbers :- " + str(len(list_mobile_numbers))
        for x in list_search:
            f.write(x + "\n")
            # print x
        f.write("\nList of mobile numbers we have got :-\n")
        for x in list_mobile_numbers:
            f.write(x + "\n")
        f.write("\n")
        f.close()
        print "All Emails and mobile numbers are scraped and saved sucessfully.. See the file email.txt"
    except TimeoutException:
        print("Box or Button not found in google.com")


url =  raw_input("Enter your URL to scrap :- ")
driver = init_driver()
lookup(driver, "Selenium",url)
driver.quit()