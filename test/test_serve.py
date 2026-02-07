import pytest
import os
import pause

from dotenv import load_dotenv
from selenium import webdriver
import datetime
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture()
def driver():
    os.environ["SE_DRIVER_MIRROR_URL"] = "https://msedgedriver.microsoft.com"
    driver = webdriver.Edge()
    yield driver
    driver.quit()
    del os.environ["SE_DRIVER_MIRROR_URL"]


def test_serve(driver):
    # wait for elements
    driver.implicitly_wait(5)
    # make sure full screen so elements are not hidden
    driver.maximize_window()

    # load env variables and force update
    load_dotenv(verbose=True, override=True)

    # go to serve page
    driver.get(
        "https://warrior.uwaterloo.ca/Program/GetProgramDetails?courseId=2882ad00-6e10-4b25-ac28-238a716ab8c5"
    )

    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    hours = int(os.getenv("HOURS"))
    minutes = int(os.getenv("MINUTES"))
    # is testing true
    testing = os.getenv("TESTING") == "true"

    wait = WebDriverWait(driver, 10)

    # log in if necessary
    try:
        # sign in button
        signInButton = wait.until(EC.element_to_be_clickable((By.ID, "loginLinkBtn")))
        signInButton.click()

        # the WATIAM button is disabled temporarily, wait for 1 second for consistency
        pause.sleep(1)

        # WATIAM button
        WATIAMButton = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-sign-in"))
        )
        WATIAMButton.click()

        # input username
        email_input = wait.until(
            EC.presence_of_element_located((By.ID, "userNameInput"))
        )
        email_input.send_keys(email)
        driver.find_element(By.ID, "nextButton").click()

        # input password
        password_input = wait.until(
            EC.presence_of_element_located((By.ID, "passwordInput"))
        )
        password_input.send_keys(password)
        driver.find_element(By.ID, "submitButton").click()

    except Exception as e:
        print(e)

    # wait for login success
    wait.until(EC.presence_of_element_located((By.ID, "profileUserThumbId")))

    # accept cookies :)
    driver.find_element(By.ID, "gdpr-cookie-accept").click()

    # wait until chosen time
    d = datetime.datetime.now()

    chosen_time = datetime.datetime(d.year, d.month, d.day, hours, minutes, 0)

    if not testing:
        pause.until(chosen_time)

    # check pfp before refresh
    pfp = driver.find_element(By.ID, "profileUserThumbId")

    # benchmarking
    t0 = datetime.datetime.now()

    # time to register
    # refresh page
    driver.refresh()
    # wait for page refresh to invalidate old pfp button
    wait.until(EC.staleness_of(pfp))

    # wait for newest session button to be clickable
    newest_session = driver.find_elements(
        By.CSS_SELECTOR,
        ".single-date-select-one-click",
    )[-1]
    newest_session.click()

    select_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".program-select-btn"))
    )
    select_btn.click()

    # register
    register = wait.until(EC.element_to_be_clickable((By.ID, "registerBtn")))
    register.click()

    # benchmarking
    t1 = datetime.datetime.now()
    print("Execution time: ", t1 - t0)

    # 60 seconds to finish registration process
    time.sleep(120)
