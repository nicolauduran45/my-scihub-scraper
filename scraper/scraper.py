# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
import time
import os
from os import path
import pandas  as pd
import random
import time
import json
import argparse
import warnings
import glob
from tqdm import tqdm
warnings.filterwarnings("ignore")

###PATH where the driver is located. Here I use the version 81 since
### it is the version of my google chrome.
## to see the Chrome driver go in Chrome->Settings->About 
#chrome_driver="chromedriver_81.exe"
#chrome_driver="scraper/chromedriver"

# Function to load IDs from a file
def load_ids(file_path, id_type):
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path)
        if id_type in data.columns:
            ids = data[id_type].dropna().unique().tolist()
        else:
            raise ValueError(f"{id_type} column not found in the CSV file.")
    elif file_path.endswith(".txt"):
        with open(file_path, 'r') as f:
            ids = [line.strip() for line in f.readlines()]
    else:
        raise ValueError("Unsupported file format. Please use a .csv or .txt file with an id per row.")
    return ids

def main(args):
    # Load IDs from the specified file
    ids = load_ids(args.file, args.id_type)
    ids = [str(i) for i in ids]

    # Handle output_dir
    output_dir = args.output_dir or os.path.join(os.getcwd(), "docs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Determine already downloaded IDs
    downloaded = []
    for fname in glob.glob(f"{output_dir}/*.pdf"):
        downloaded_id = fname.split('/')[-1].replace('.pdf', '').strip()
        downloaded.append(downloaded_id)

    ids_to_download = list(set(ids) - set(downloaded))

    # Get the list of files in the downloads directory before downloading
    existing_files = set(glob.glob(os.path.join(args.downloads_dir, "*.pdf")))


    # Setup Selenium WebDriver
    #chrome_driver = "scraper/chromedriver"
    for id_value in tqdm(ids_to_download, desc='Downloading IDs'):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(args.chromedriver, options=options)
        driver.set_page_load_timeout(99999)

        try:
            driver.get("https://sci-hub.tf")

            # Handle consent pop-up
            try:
                consent_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Accept") or contains(text(), "Consent")]'))
                )
                consent_button.click()
            except:
                print("Consent button not found or already accepted.")

            time.sleep(random.randint(2, 3))
            driver.find_element(By.NAME, "request").click()
            time.sleep(random.randint(2, 3))
            driver.find_element(By.NAME, "request").send_keys(id_value)
            driver.find_element(By.CSS_SELECTOR, "p > img").click()
            time.sleep(random.randint(2, 3))
            driver.find_element(By.CSS_SELECTOR, "button").click()
            time.sleep(random.randint(40, 45))

            # Get the list of files in the downloads directory after downloading
            new_files = set(glob.glob(os.path.join(args.downloads_dir, "*.pdf")))

            # Identify the new file(s) by subtracting the sets
            downloaded_files = new_files - existing_files

            dest_dir = args.output_dir
            # Process the new file
            if downloaded_files:
                new_file = downloaded_files.pop()  # Assuming only one new file is downloaded
                dest_file = os.path.join(output_dir, f"{id_value}.pdf")
                os.rename(new_file, dest_file)
                print(f"File downloaded and moved to: {dest_file}")
            else:
                print("No new file downloaded.")
                break
        except Exception as e:
            print(f"Error processing {id_value}: {e}")
        finally:
            driver.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape articles from SciHub using Selenium.")
    parser.add_argument(
        "--file", 
        required=True, 
        help="Path to the input file containing IDs (CSV or TXT)."
    )
    parser.add_argument(
        "--id_type", 
        required=True, 
        choices=["DOI", "PMID"], help="Type of IDs provided in the file."
    )
    parser.add_argument(
        "--chromedriver", 
        required=True, 
        help="Path to the Chrome driver executable."
    )
    parser.add_argument(
        "--output_dir", 
        required=False, 
        help="Directory to store the downloaded PDFs. Defaults to './docs'."
    )

    parser.add_argument(
        "--downloads_dir", 
        required=False, 
        default=os.path.join(os.path.expanduser("~"), "Downloads"),  # Default downloads directory
        help="Directory where files are downloaded by the browser. Defaults to '~/Downloads'."
    )

    args = parser.parse_args()

    main(args)

'''
python script_name.py \
    --file path/to/input_file.csv \
    --id_type DOI \
    --chromedriver path/to/chromedriver \
    --downloads_dir ~/Downloads
'''