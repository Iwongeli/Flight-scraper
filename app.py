# Constants
EXCEL_FILE_PATH = r'C:\Users\tomas\OneDrive\Pulpit\flight_scraper/record.xlsx'
URLS_FILE_PATH = r'C:\Users\tomas\OneDrive\Pulpit\flight_scraper/urls.txt'

from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_data(url):
    # declare url
    
    print('Searching for:', url)
    
    driver = webdriver.Chrome()
    driver.get(url)
    # get all flight by class
    results = driver.find_elements(By.CLASS_NAME, "result ")
    flight_links = driver.find_elements(By.TAG_NAME, "a") 
    f_numbers = []
    for link in flight_links:
        link = link.get_attribute("href")
        if link.startswith("https://www.flightradar24.com/data/flights/"):
            link = link.split("/")[-1]
            f_numbers.append(link)
    return results, f_numbers


def analyze_data(results, f_numbers):
    data = []
    current_datetime = datetime.now()
    current_time = f"{current_datetime.hour}:{current_datetime.minute}"

    for i in range(len(results)):
        record = results[i].text + f_numbers[i] + '\n'
        record = str(record)
        record = record.strip()
        record = record.split()
        record = record[-1:] + record[2:7] + record[-10:-7] + record[-3:-1]
        record.append(current_datetime.date())
        record.append(current_time)
        data.append(record)

    column_names = ['Number', 'Date', 'Time', 'From', 'From_Code', 'Landing_Time', 'To', 'To_Code', 'Length', 'Price', 'Currency', 'Record_Date', 'Timestamp']
    df = pd.DataFrame(data, columns=column_names)

    print(df)
    return df


def update_record_base(df):
    try:
        existing_df = pd.read_excel(EXCEL_FILE_PATH)
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['Number', 'Date', 'Time', 'From', 'From_Code', 'Landing_Time', 'To', 'To_Code', 'Length', 'Price', 'Currency', 'Record_Date', 'Timestamp'])

    updated_df = pd.concat([existing_df, df], ignore_index=True)

    try:
        updated_df.to_excel(EXCEL_FILE_PATH, index=False)
    except:
        updated_df.to_excel('record.xlsx', index=False)

    print("Data appended and saved to Excel successfully.")


def read_urls():
    res = []
    try:
        with open(URLS_FILE_PATH, 'r') as file:
            for line in file:
                if line.startswith('https://'):
                    res.append(line.strip())
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except IOError:
        print("Error occurred while reading the file.")

    return res


def main():
    urls = read_urls()
    if not urls:
        urls = [""]
        
    for url in urls:
        while not url:
            url = input("Provide Azair link: ").strip()
        data, flights = get_data(url)
        df = analyze_data(data, flights)
        update_record_base(df)


if __name__ == "__main__":
    main()
