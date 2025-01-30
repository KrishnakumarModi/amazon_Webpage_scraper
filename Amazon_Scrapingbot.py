from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup the browser
service = Service(executable_path = "chromedriver.exe")
browser = webdriver.Chrome(service = service)
browser.get('https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar')
browser.maximize_window()
  

# Function to go to the next page
def next_Page():
    try:
        # Wait for the "Next" button to become clickable and click it
        next_Button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "s-pagination-item.s-pagination-next"))
        )
        next_Button.click()
        time.sleep(3)  # Give time for the page to load
    except Exception as e:
        print(f"Error while clicking the next button: {e}")

# List to store the product data
data = []

# Loop through pages (adjust the range as needed)
for i in range(1):  # Adjust the range as needed (2 means 2 pages)
    print(f"Scraping page {i + 1}")
    
    # Wait for the page to load properly
    time.sleep(3)

    # Find all product containers on the current page
    product_Container = browser.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")    

    # Loop through the products on the page
    for product in product_Container:
        try:
            # Get product name
            product_Name = product.find_element(By.XPATH, ".//h2[@class='a-size-base-plus a-spacing-none a-color-base a-text-normal']//span").text.strip()         
        except:
            product_Name = 'Not Available'

        try:
            # Get product price
            product_Price = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text.strip()              
        except:
            product_Price = 'Out of Stock'

        try:
            # Get product rating
            product_Rating = product.find_element(By.XPATH, ".//span[@class='a-size-base s-underline-text']").text.strip()         
        except:
            product_Rating = 'Not Available'

        # redirected into link 
        product_Link = product.find_element(By.LINK_TEXT, product_Name).get_attribute("href")
            
        browser.execute_script("window.open(arguments[0]);", product_Link)
        browser.switch_to.window(driver.window_handles[1])
        
        try:
            # Get seller name 
            product_Sellername = [product.find_element(By.XPATH, ".//a[@id='sellerProfileTriggerId']").text.replace('',',')]
            product_Sellername = product_Sellername[0]
        except:
            product_Sellername = 'Not Available'

        # Close link tab
        browser.close()
        browser.switch_to.window(driver.window_handles[0])
        
        # Append the product details to the data list
        data.append({
            "Product Name": product_Name,
            "Product Price": product_Price,
            "Product Rating": product_Rating,
            "Product Seller Name": product_Sellername
        })

    # Go to the next page after scraping the current page
    next_Page()

# Convert the data list into a pandas DataFrame
df = pd.DataFrame(data)

# Print the collected data
print(df)

# Save the data to a CSV file
df.to_csv('amazon_products.csv', index=False)

# Close the browser
browser.quit()