#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:25:25 2021

@author: awais
Script to get the jobs slary data from the resource
This one is set up for Indeed  site, to get salary reports from Indeed's site
"""
import gspread
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import re
    

#read file from google sheets, passing in cred from google console
client = gspread.service_account(filename="google_drive_client_secret.json")

Job_Data = client.open("New Jobs Salary Data").get_worksheet(1)

#getting the states and rmeoving the '' elements
States = Job_Data.row_values(1)[1:]
States = [s for s in States if len(s) > 1]

#getting the job cell location to append the salaries for that job. Col increment 1 to start
Job_loc = Job_Data.find("Marketing Coordinator")
col = Job_loc.col + 1
row = Job_loc.row

#function to insert salary data into respective order in google sheetr
def Insert_Salaries(Salary):
    #global keyword to increment the columns
    global col
    for sal in Salary:
        Job_Data.update_cell(row, col, sal)
        col +=1
    print("salaries been inserted")

#using selenium to open the page and get the content
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

driver.get("https://www.indeed.com/career/marketing-coordinator/salaries")
#iterate through each state to get the salaries for each state
for state in States:
    #first clearing the search through indeed clear button, then filling in new state
    driver.find_element_by_id('clear-location-localized').click()
    driver.find_element_by_id("input-location-autocomplete").send_keys(state)
    #clicking the search button
    time.sleep(0.5)
    driver.find_element_by_id("title-location-search-btn").click()
    #getting the content from the page placing it in beautiful soup
    time.sleep(2)
    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'lxml')
    #class that contains all of the salaries
    Salary_elements = soup.find_all('span', class_='align-right')
    #new list that turns the tag elemnets in the list to string and removes the ",". 
    #Only the elemnets that have the $ are the ones that show salaries. Getting only the digits in a list
    Salary_string = [str(s).replace(',','') for s in Salary_elements if '$' in str(s)]
    Salaries = ["".join(re.findall('\d', s)) for s in Salary_string]
    print(f"Insertin salaries {Salaries} for {state}")
    Salaries.sort()
    #updating the salary in their respected levels in the google sheet using map on the list
    Insert_Salaries(Salaries)
    #cool down for a sec before going to next state
    time.sleep(1)

