import time
import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

# ensure working directory is script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open('plates.json', 'r') as file:
    plates = json.load(file)

# initialize works.json
with open('works.json', 'w') as worker:
    json.dump([], worker)
with open('works.json', 'r') as worker:
    works = json.load(worker)

numdic = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
}

def webcheck(plates_subset, driver):
    def perrow(row, plate):
        rownum = driver.find_element(By.ID, f"MainContent_txtInputRow{numdic[row]}")
        rownum.send_keys(plate)

    driver.get("https://services.flhsmv.gov/mvcheckpersonalplate/")
    
    for row in range(1, len(plates_subset) + 1):
        perrow(row, plates_subset[row - 1])

    submit = driver.find_element(By.ID, "MainContent_btnSubmit")
    submit.click()

    time.sleep(1)

    for row in range(1, len(plates_subset) + 1):
        # note the output ID typo fix for rows 3–5
        out_id = (
            f"MainContent_lblOutPutRow{numdic[row]}"
            if row <= 2
            else f"MainContent_lblOutputRow{numdic[row]}"
        )
        rowresults = driver.find_element(By.ID, out_id)

        print(plates_subset[row - 1], rowresults.text)
        if rowresults.text == "AVAILABLE":
            works.append(plates_subset[row - 1])

# configure headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# use Service to avoid __init__() multiple-values error
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

numofentries = len(plates)
print(f"We will check this many plates: {numofentries}")

for i in range(0, numofentries, 5):
    plates_subset = plates[i:i + 5]
    webcheck(plates_subset, driver)

with open('works.json', 'w') as worker:
    json.dump(works, worker, indent=4)

driver.quit()
