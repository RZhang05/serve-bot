# Serve auto sign up
A python script to open a browser instance using `Selenium` and auto enroll into a serve session. This script is designed to wait until a certain time, refresh the page, choose the most recent session and register.

## Features
- can only sign up for the first session in a day (i.e. will not be able to do the second (later) session on Fridays for example)
- currently uses the edge browser (may need to be updated to support other browsers)

## How to use
If any issues are encountered please reach out to me.

### Installation

#### Installing python
1. Go here https://www.python.org/downloads/ and follow the steps.
#### Cloning the repo
1. Make sure you have git installed (https://git-scm.com/downloads).
2. Using git bash, navigate to the folder you want the repo to be located.
3. Run `git clone https://github.com/RZhang05/serve-bot.git`.
#### Setting up the .env file
1. In the root directory of the repo (`/serve-bot/`) in the same folder as the `.env.example` file, copy the `.env.example` file and rename it to `.env`.
2. Change the `EMAIL` and `PASSWORD` fields to your credentials.
#### Setting up the python env
1. Open up a terminal at the root directory of the repo.
2. (Optional) Create a venv. (https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
3. Run `pip install -r requirements.txt`.

### Running the script
1. Change the `HOURS` and `MINUTES` fields to when you want the page to be refreshed (if a session opens at 9pm you would put `21` and `0` respectively).
2. Run `pytest -s`.
3. Wait until the time comes, the script should register you automatically, then **you will have 60 seconds to finish the registration process**.
4. Have fun at the serve session :)
