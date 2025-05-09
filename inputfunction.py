import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import json

# Load plates and initialize works list
with open('Florida License Plate Project/plates.json', 'r') as file:
    plates = json.load(file)

with open('Florida License Plate Project/works.json', 'w') as worker:
    json.dump([], worker)  # Clear previous works list
with open('Florida License Plate Project/works.json', 'r') as worker:
    works = json.load(worker)

numdic = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
}

def webcheck(plates_subset):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (needed for headless on some systems)
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing (needed on some systems)
    driver.get("https://services.flhsmv.gov/mvcheckpersonalplate/")
    
    # Per row plate enter
    def perrow(row, plate):
        rownum = driver.find_element(By.ID, "MainContent_txtInputRow" + numdic[row])
        rownum.send_keys(plate)

    # iterate over rows 5 at a time
    for row in range(1, len(plates_subset) + 1):  # Adjust to handle the number of plates in the subset
        perrow(row, plates_subset[row - 1])

    # Submit
    submit = driver.find_element(By.ID, "MainContent_btnSubmit")
    submit.click()

    time.sleep(1)

    # Check the results for each row
    for row in range(1, len(plates_subset) + 1):  # Adjust to handle the number of plates in the subset
        if row <= 2:
            rowresults = driver.find_element(By.ID, "MainContent_lblOutPutRow" + numdic[row])
        else:
            rowresults = driver.find_element(By.ID, "MainContent_lblOutputRow" + numdic[row])

        print(plates_subset[row - 1])  # Plate being checked
        print(rowresults.text)  # Output for the row

        if rowresults.text == "AVAILABLE":
            works.append(plates_subset[row - 1])

    driver.quit()

# Calculate number of entries and break into batches of 5
numofentries = len(plates)
print(f"We will check this many plates: {numofentries}")

# Process plates in chunks of 5
for i in range(0, numofentries, 5):  # start with 5, increment by 5
    plates_subset = plates[i:i + 5]  # grab next 5
    webcheck(plates_subset)

# Save the updated works list back to the json list
with open('Florida License Plate Project/works.json', 'w') as worker:
    json.dump(works, worker, indent=4)
