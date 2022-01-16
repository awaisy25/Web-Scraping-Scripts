#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 18:25:30 2021

@author: awais
Script to get the jobs slary data from the resource
This one is set up for dice site, to get salary reports from dice's site
"""
import gspread
import requests
import time
from bs4 import BeautifulSoup
from itertools import product
    
#read file from google sheets, passing in cred from google console
client = gspread.service_account(filename="google_drive_client_secret.json")

Job_Data = client.open("New Jobs Salary Data").sheet1

#not inlcuding the first two rows from column 1
Jobs = Job_Data.col_values(1)[2:]

States =Job_Data.row_values(1)[1:]
#removing the empty list itemst
States = [State for State in States if len(State) > 1]

#years formated as entry:1 Mid-Level:4 Senior:8
Years = ["1", "4", "8"]
base_url = "https://www.dice.com/salary-calculator?title={0}&location={1}&experience={2}"

for Job in Jobs:
    Job_loc_sheet = Job_Data.find(Job)
    #row number will be fixed, column will be unfixed with + 1 index from orignal location
    col = Job_loc_sheet.col + 1
    row = Job_loc_sheet.row 
    #creating a cartesian product of the lists to have all pair combinations
    for job, state, year in product([Job], States, Years):
        url_search = base_url.format(job,state,year)
        page = requests.get(url_search)
        soup = BeautifulSoup(page.content, 'html.parser')
        #looking at dice page want to get the max slary from id attribute maxSal
        Max_sal = soup.find(id="maxSal")
        print(f"Max Salary for {job} in {state} for {year} of experience is: {Max_sal.text}")
        #inserting the job salary for that job's row. increment column to move to the next column
        Job_Data.update_cell(row, col, Max_sal.string)
        print(f"Max Salary for {job} in {state} for {year} has been inserted in row: {row} col:{col}")
        col +=1
        time.sleep(1)

    
    

