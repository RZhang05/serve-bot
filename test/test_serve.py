import pytest
import os
import pause

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

def test_prints_page(driver):
    # wait for elements
    driver.implicitly_wait(5)
    # make sure full screen so elements are not hidden
    driver.maximize_window()

    # load env variables and force update
    load_dotenv(verbose=True, override=True)

    # go to serve page
    driver.get("https://warrior.uwaterloo.ca/Program/GetProgramDetails?courseId=2882ad00-6e10-4b25-ac28-238a716ab8c5")

    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    hours = int(os.getenv("HOURS"))
    minutes = int(os.getenv("MINUTES"))
    testing = os.getenv("TESTING")

    wait = WebDriverWait(driver, 5)
    
    # log in if necessary
    try:
        driver.find_element(By.ID, "loginLinkBtn").click()
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
    d = datetime.datetime.now()

    chosen_time = datetime.datetime(d.year, d.month, d.day, hours, minutes, 0)
    pause.until(chosen_time)

    # check pfp before refresh
    pfp = driver.find_element(By.ID, "profileUserThumbId")

    # accept cookies :)
    driver.find_element(By.ID, "gdpr-cookie-accept").click()

    # time to register
    # refresh page
    driver.refresh()
    # wait for page refresh to invalidate old pfp button
    wait.until(EC.staleness_of(pfp))
    # keep track of old session button
    old_session = driver.find_element(By.XPATH, '//button[@class="btn btn-outline-primary program-select-btn w-100 mb-2"]')
    # find most recent session button and click it
    buttons = driver.find_elements(By.XPATH, '//button[@class="btn date-selector-btn-secondary single-date-select-button single-date-select-one-click position-relative"]')
    button = wait.until(EC.element_to_be_clickable(buttons[-1]))  
    button.click()

    # wait for old session button to be invalidated
    wait.until(EC.staleness_of(old_session))
    # select new session
    session = driver.find_element(By.XPATH, '//button[@class="btn btn-outline-primary program-select-btn w-100 mb-2"]')
    session.click()
    # register
    register = wait.until(EC.element_to_be_clickable((By.ID, "registerBtn")))
    register.click()
    # 60 seconds to finish registration process
    time.sleep(60)

