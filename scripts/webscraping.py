from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

"""
Exercise 4: Scrape CoinMarketCap's Top 10 Cryptocurrencies
Scrape 'Name', 'Symbol', and 'Market Cap' data
Identify the cryptocurrency with the highest market cap. """

# Setup our WebDriver
driver = webdriver.Chrome() 

# Open CoinMarketCap
driver.get("https://coinmarketcap.com/")

# Explicit wait until the elements are visible
wait = WebDriverWait(driver, 10) 

def getCurrencies(amount):
    names = []
    symbols = []
    marketCaps = []

    for i in range(1, amount + 1): 

        try:
            # find the xpath for each element we want to scrape
            name_xpath = f'//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[3]/div/a/div/div/div/p'
            symbol_xpath = f'//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[3]/div/a/div/div/div/div/p'
            marketCap_xpath = f'/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[4]/table/tbody/tr[{i}]/td[8]/p/span[2]'

            # Wait for each element to be present and get the text
            name = wait.until(EC.presence_of_element_located((By.XPATH, name_xpath))).text
            symbol = wait.until(EC.presence_of_element_located((By.XPATH, symbol_xpath))).text
            marketCap = wait.until(EC.presence_of_element_located((By.XPATH, marketCap_xpath))).text

            # Append the data to the lists
            names.append(name)
            symbols.append(symbol)
            marketCaps.append(marketCap)

        except Exception as e:
            print(f"Error fetching data for row {i}: {e}")

    return names, symbols, marketCaps 


def createDf(namesList, SymbolsList, mcLists):
    
    mcLists_cleaned = pd.to_numeric([cap.replace('$', '').replace(',', '') for cap in mcLists], errors='coerce')

    df = pd.DataFrame({
        'Name': namesList,
        'Symbol': SymbolsList,
        'Market Cap': mcLists_cleaned
    })

    return df

def exportData(df, LargestMcap):
    with open('cryptoData.txt', 'w') as f:
        f.write("Top 10 Cryptocurrencies:\n")
        f.write(df.to_string(index = False))
        f.write("\n\nCryptocurrency with the largest market cap:\n")
        f.write(LargestMcap.to_string())


# Fetch data for the top 10 cryptocurrencies
names, symbols, market_caps = getCurrencies(10)

# Create the DataFrame
df = createDf(names, symbols, market_caps)

# Find the cryptocurrency with the largest market cap
largestMcapIdx = df['Market Cap'].idxmax()
largestMcap = df.loc[largestMcapIdx]

#close the driver
driver.quit()

# Export our data to a txt file
exportData(df, largestMcap)
