import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json

with open('Florida License Plate Project/plates.json', 'r') as file:
    plates = json.load(file)

with open('Florida License Plate Project/works.json', 'w') as worker:
    json.dump([], worker)
with open('Florida License Plate Project/works.json', 'r') as worker:
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
        rownum = driver.find_element(By.ID, "MainContent_txtInputRow" + numdic[row])
        rownum.send_keys(plate)

    driver.get("https://services.flhsmv.gov/mvcheckpersonalplate/")
    
    for row in range(1, len(plates_subset) + 1):
        perrow(row, plates_subset[row - 1])

    submit = driver.find_element(By.ID, "MainContent_btnSubmit")
    submit.click()

    time.sleep(1)

    for row in range(1, len(plates_subset) + 1):
        if row <= 2:
            rowresults = driver.find_element(By.ID, "MainContent_lblOutPutRow" + numdic[row])
        else:
            rowresults = driver.find_element(By.ID, "MainContent_lblOutputRow" + numdic[row])

        print(plates_subset[row - 1]) 
        print(rowresults.text)

        if rowresults.text == "AVAILABLE":
            works.append(plates_subset[row - 1])

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

numofentries = len(plates)
print(f"We will check this many plates: {numofentries}")

for i in range(0, numofentries, 5):
    plates_subset = plates[i:i + 5]
    webcheck(plates_subset, driver)

with open('Florida License Plate Project/works.json', 'w') as worker:
    json.dump(works, worker, indent=4)

driver.quit()
