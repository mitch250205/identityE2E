SET UP:
******
Code was written using a MAC
Make sure your machine has python 3 installed
Clone this repository
Create a virtual environment
python -m venv .venv
Install dependencies with:
pip install -r requirements.txt

in config/config.py set the location of the input (eg car_input-V6.txt) and output data (eg car_output-V6.txt) files.
It is possible to have multiple input and output *.txt files.
Headless mode is set to False for this release

HOW TO RUN TESTS:
****************
in directory identityE2E:
to run all tests: pytest -v -s

to run all tests using confused.com: pytest -v -s -m confused

Notes:
******
1. Deafult BASE_URL is set to https://www.confused.com/ so only this site will be used in this release.
   Additionally tests using Motorway.com are skipped since I was unable to use it after a number of tests due to automation so these are not fully completed and validated
3. I have included some code to capture and deal with an AI helper pop up, however this happened very rarely and I was unable to fully validate it in this release.
4. This code is not currently designed to run in headless mode.




IdentityE2E - Test Automation Framework 

Setup Instructions 🛠️

Prerequisites:

Developed and tested on macOS.

Ensure Python 3 is installed:

python3 --version

Install Git if not already installed:

git --version

Installation Steps

1. Clone this repository

git clone <repository_url>
cd identityE2E

2. Create a virtual environment

python -m venv .venv

3.Activate the virtual environment

macOS/Linux:

source .venv/bin/activate

Windows:

.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Configure test data files in config/config.py:

CAR_INPUT_TXT_FILE = "car_input-V6.txt"
CAR_OUTPUT_TXT_FILE = "car_output-V6.txt"

You can use multiple input/output .txt files.

Headless mode is disabled by default.

Running Tests

Run All Tests:

pytest -v -s

Run Tests for Confused.com Only:

pytest -v -s -m confused

Important Notes 📌

1. Default Site:

The BASE_URL is set to https://www.confused.com/, meaning all tests are currently designed for this site.

Motorway.com tests are skipped because access was restricted due to automation. These tests are not fully validated.

2. AI Helper Pop-up Handling:

The framework includes logic to detect and dismiss an AI helper pop-up.

However, this pop-up appears very rarely and inconsistently, so validation is not fully completed.

3. Headless Mode:

The tests are not currently optimized for headless execution.

If required, this can be enabled in config/config.py.
