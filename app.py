from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from time import sleep
import pandas as pd

def get_data():
    
    # declare url
    url = "https://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway=return&srcAirport=Warsaw+%5BWAW%5D+%28%2BWMI%2CLCJ%2CSZY%2CLUZ%29&srcap0=WMI&srcap1=LCJ&srcap2=SZY&srcap3=LUZ&srcFreeAirport=&srcTypedText=pra&srcFreeTypedText=&srcMC=&dstAirport=Milan+%5BMXP%5D+%28%2BLIN%2CBGY%29&dstap0=LIN&dstap1=BGY&dstFreeAirport=&dstTypedText=mil&dstFreeTypedText=&dstMC=MIL_ALL&depmonth=202303&depdate=2023-03-15&aid=0&arrmonth=202303&arrdate=2023-03-31&minDaysStay=5&maxDaysStay=5&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=true&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&autoprice=true&adults=1&children=0&infants=0&maxChng=1&currency=EUR&lang=en&indexSubmit=Search"
    while url == "":
        url = input("provide azair link:")
        url = url.strip()
    print('\nPROCESSING...')
    
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(2)
    # get all flight by class
    results = driver.find_elements(By.CLASS_NAME, "result ")
    
    flight_links = driver.find_elements(By.TAG_NAME, "a") 
    f_number = []
    for link in flight_links:
        link = link.get_attribute("href")
        if link.startswith("https://www.flightradar24.com/data/flights/"):
            link = link + "\n"
            f_number.append(link)
    
    with open('records.txt', 'w') as file:
        counter = 0
        for result in results:
            file.writelines(f_number[counter])
            file.writelines(f_number[counter + 1])
            file.writelines(result.text)
            counter += 2


def analyze():
    print("\nPROCESING DATA...")
    with open('records.txt', 'r') as file:
        offers = []
        # analyze every line:
        link_counter = 0
        for line in file:
            
            line = line.strip()
            
            # Flight data
            if line.startswith('THERE'):
                line = line.split()
                start_date = line[2]
                start_time = line[3]
                f_from = line[4]
                airport_f_from = line[5]
                f_to = line[7]
                airport_f_to = line[8]
            
            # Return flight data
            elif line.startswith('BACK'):
                line = line.split()
                back_date = line[2]
                back_time = line[3]
                r_from = line[5]
                r_to = line[8]
            
            elif line.startswith('https://www.flightradar24'):
                
                line = line.split('/')
                if link_counter == 0:
                    f_number_to = line[-1]
                else:
                    f_number_return = line[-1]
                link_counter += 1
                
            # price line
            elif len(line) < 9 and len(line) != 0:
                # check if line starts with currency symbol or not
                if line[0].isnumeric():
                    line = line.split()
                    price = line[0]
                    currency = line[1]
                else:
                    price = line[1:]
                    currency = line[0]
                
                
            # after this line start new record
            elif line.startswith('Length of stay'):
                
                link_counter = 0
                try:
                    offers.append((f_from, f_to, airport_f_from, airport_f_to, f_number_to, price, currency, start_date, start_time, back_date, back_time, r_from, r_to, f_number_return))
                except:
                    print('Data error!')
        
        # create table
        print("\nCREATING TABLE...")
        df = pd.DataFrame(offers, columns=['FROM', 'TO', 'F_AIRPORT', 'T_AIRPORT', 'FLIGHT_NUMBER', 'PRICE', 'CURRENCY', 'FLIGHT', 'FLIGHT_TIME', 'RETURN', 'RETURN_TIME', 'F_AIRPORT', 'T_AIRPORT', 'RETURN_FLIGHT_NUMBER'])
        
        # name a file
        name = input("\nname the file or leave blank for date:")
        if name =="":
            output = date.today()
        else:
            output = name
        print("\nSAVING TO EXCEL FILE...")
        df.to_excel(f'{airport_f_from}_{output}.xlsx', index=False)
                
def main():
    get_data()
    analyze()
    
    print('SUCCES!')

if __name__ == "__main__":
    main()
