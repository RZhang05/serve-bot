import pytest
import os

from dotenv import load_dotenv
from selenium import webdriver
import datetime
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

@pytest.fixture()
def driver():
    driver = webdriver.Edge()
    yield driver
    driver.quit()

@pytest.fixture()
def dotenv_info():
    load_dotenv()

    yield (os.getenv('EMAIL'), os.getenv('PASSWORD'), os.getenv("HOURS"), os.getenv("MINUTES"), os.getenv("TESTING"))

def test_prints_page(driver, dotenv_info):
    # wait for elements
    driver.implicitly_wait(5)
    # make sure full screen so elements are not hidden
    driver.maximize_window()

    # go to serve page
    driver.get("https://warrior.uwaterloo.ca/Program/GetProgramDetails?courseId=2882ad00-6e10-4b25-ac28-238a716ab8c5")

    email = dotenv_info[0]
    password = dotenv_info[1]
    hours = dotenv_info[2]
    minutes = dotenv_info[3]
    
    # log in if necessary
    try:
        driver.find_element(By.ID, "loginLinkBtn").click()
        wait = WebDriverWait(driver, 5)
        login = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@title="WATIAM USERS" and not(@disabled)]')))
        login.click()

        # input username
        email_input = wait.until(EC.presence_of_element_located((By.ID, "userNameInput")))
        email_input.send_keys(email) 
        driver.find_element(By.ID, "nextButton").click()

        # input password
        password_input = wait.until(EC.presence_of_element_located((By.ID, "passwordInput")))
        password_input.send_keys(password)
        driver.find_element(By.ID, "submitButton").click()

    except Exception as e: print(e)

    # wait for login success
    wait.until(EC.presence_of_element_located((By.ID, "profileUserThumbId")))

    # wait until chosen time
    while True:
        d = datetime.datetime.now()

        if d.hour == hours and d.minute == minutes or dotenv_info[4]:
            # time to register
            # refresh page
            driver.refresh()
            # wait for page load
            wait.until(EC.presence_of_element_located((By.ID, "profileUserThumbId")))
            # find most recent session button and click it
            buttons = driver.find_elements(By.XPATH, '//button[@class="btn date-selector-btn-secondary single-date-select-button single-date-select-one-click position-relative"]')
            button = wait.until(EC.element_to_be_clickable(buttons[-1]))  
            button.click()

            # select session
            driver.find_elements(By.XPATH, '//button[@class="btn btn-outline-primary program-select-btn w-100 mb-2"]').click()
            # register
            register = wait.until(EC.element_to_be_clickable((By.ID, "registerBtn")))
            register.click()
            time.sleep(5)
        else:
            time.sleep(0.1)

