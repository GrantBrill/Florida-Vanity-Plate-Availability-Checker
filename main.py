import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json

with open('Florida License Plate Project\plates.json', 'r') as file:
    plates = json.load(file)

with open('Florida License Plate Project\works.json', 'w') as worker:
    json.dump([], worker)
with open('Florida License Plate Project\works.json', 'r') as worker:
    works = json.load(worker)

numdic = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",

}


def webcheck(row, plate):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://services.flhsmv.gov/mvcheckpersonalplate/")

    row2 = driver.find_element(By.ID, "MainContent_txtInputRow" + numdic[int(row)])
    row2.send_keys(plate)

    submit = driver.find_element(By.ID, "MainContent_btnSubmit")
    submit.click()


    time.sleep(1)
    
    #who the hell wrote this shit ass website. The name changes from "OutPut" to "Output" after row two for fuck all?
    if row <= 2:
        rowresults = driver.find_element(By.ID, "MainContent_lblOutPutRow" + numdic[int(row)])
    else:
        rowresults = driver.find_element(By.ID, "MainContent_lblOutputRow" + numdic[int(row)])
    
    print(plate)
    print(rowresults.text)
    if rowresults.text == "AVAILABLE":
        works.append(plate)
    else:
        exit

    driver.quit()



for row in range (1, 6):
    webcheck(int(row), plates[row - 1])

with open('Florida License Plate Project/works.json', 'w') as worker:
    json.dump(works, worker, indent=4)