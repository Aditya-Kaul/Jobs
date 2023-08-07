from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

#REFERENCE
#author:arapfaik
#repo: https://github.com/arapfaik/scraping-glassdoor-selenium

def get_jobs(keyword, num_jobs, verbose,slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    url = 'https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14.htm'

    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.
        print('waitinggggggggggggggggggggggg')

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'.//button[@data-role-variant="ghost"]')))
            # driver.find_element(By.XPATH,'.//button[@data-role-variant="ghost"]').click()
            driver.find_element(By.CLASS_NAME,'selected').click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            driver.find_element(By.CLASS_NAME,"e1jbctw80 ").click()  #clicking to the X.
            print('X OUT WORKED')
        except NoSuchElementException:
            print('X OUT FAILED')
            pass

        
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CSS_SELECTOR,"a.jobCard")  #jl for Job Listing. These are the buttons we're going to click.
        print('JOBBSS================================================>>>>>>>>>>>>>>>>>>>>>')
        print(len(jobs))
        print(num_jobs)
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                print("=============>>> BROKEN")
                break
            print(job_button)
            job_button.click()  #You might 
            print(job_button)
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    print('==================-not collected_successfully')
                    company_name = driver.find_element(By.XPATH,'.//div[@data-test="employerName"]').text
                    location = driver.find_element(By.XPATH,'.//div[@data-test="location"]').text
                    job_title = driver.find_element(By.XPATH,'.//div[@data-test="jobTitle"]').text
                    job_description = driver.find_element(By.CLASS_NAME,'jobDescriptionContent').text
                    collected_successfully = True
                except:
                    print('==time.sleep(5)=====')
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.CLASS_NAME,'css-ey2fjr').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
            print('======================== VERBOSE')
            #Printing for debugging
            # if verbose:
            #     print("Job Title: {}".format(job_title))
            #     print("Salary Estimate: {}".format(salary_estimate))
            #     print("Job Description: {}".format(job_description[:500]))
            #     print("Rating: {}".format(rating))
            #     print("Company Name: {}".format(company_name))
            #     print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                # driver.find_element(By.ID,'.//div[@class="tab" and @data-tab-type="overview"]').click()
                driver.find_element(By.ID,'EmpBasicInfo')
                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    headquarters = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1

                try:
                    size = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Size"]//following-sibling::*').text
                    print(size)
                    print('================== SIZE ==========================')
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Founded"]//following-sibling::*').text
                    print(founded)
                    print('================== fOUNDED ==========================')
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Type"]//following-sibling::*').text
                    print(type_of_ownership)
                    print('================== TYPE ==========================')
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,'.//div[@class="e1pvx6aw0"]//span[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1
                print('======================= all MINUS -1')

                
            # if verbose:
            #     print("Headquarters: {}".format(headquarters))
            #     print("Size: {}".format(size))
            #     print("Founded: {}".format(founded))
            #     print("Type of Ownership: {}".format(type_of_ownership))
            #     print("Industry: {}".format(industry))
            #     print("Sector: {}".format(sector))
            #     print("Revenue: {}".format(revenue))
            #     print("Competitors: {}".format(competitors))
            #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs
        print('=========...................')
        #Clicking on the "next page" button
        try:
            driver.find_element('xpath','.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            #break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

path1 = "C:/Users/StraViso/Desktop/DS Proj/chromedriver"

path2 = "./chromedriver.exe"
data_csv = get_jobs("data scientist",30,True,15)

data_csv.to_csv('JOBS1.csv', header = True,mode='w')

