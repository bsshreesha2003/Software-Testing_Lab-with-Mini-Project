import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver using the inbuilt chromedriver module
driver = webdriver.Chrome()

try:
    # Step 1: Navigate to Max Fashion
    driver.get("https://www.maxfashion.in/in/en/")
    driver.maximize_window()
    print("Navigated to Max Fashion homepage.")

    # Step 2: Close any pop-ups or overlays if they appear
    try:
        close_popup = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '✕')]"))
        )
        close_popup.click()
        print("Popup closed.")
    except TimeoutException:
        print("No popup to close or unable to find popup.")
    time.sleep(2)  # Allow time for any remaining pop-ups to close

    # Step 3: Find the search box element and perform a search
    search_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='js-site-search-input']"))
    )
    search_box.send_keys("T Shirts for Men")
    search_box.submit()
    print("Search performed.")
    time.sleep(5)  # Allow time for the search results to load

    # Step 4: Wait for search results to load
    specific_product_xpath = '//*[@id="product-1000013589357-Pink-PINK"]/div[1]/a'
    product_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, specific_product_xpath))
    )
    print("Search results loaded.")
    time.sleep(3)  # Allow time for the examiner to see the search results

    # Step 5: Get the product link URL
    product_url = product_link.get_attribute("href")
    
    # Step 6: Open a new tab and navigate to the product URL
    driver.execute_script(f"window.open('{product_url}', '_blank');")
    print("Specific product link opened in new tab.")
    time.sleep(2)  # Allow time for the new tab to open

    # Step 7: Switch to the new tab
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])
    print("Switched to new tab.")
    time.sleep(3)  # Allow time for the new tab to load

    # Step 8: Ensure the page has loaded by checking for product title visibility
    product_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[@class='MuiTypography-root jss379 MuiTypography-body1']"))
    ).text
    
    # Step 9: Extract the product price
    product_price = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='MuiBox-root jss426']"))
    ).text
    
    # Step 10: Select the size of the product
    size_selection = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='L']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", size_selection)
    time.sleep(2)
    size_selection.click()
    print("Size selected.")
    time.sleep(2)  # Allow time for the size selection to take effect

    # Step 11: Click the 'Add to Basket' button
    try:
        # Locate the 'Add to Basket' button
        add_to_cart_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='ADD TO BASKET']"))
        )

        # Scroll into view and ensure it is clickable
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
        print("Scrolled to 'Add to Basket' button.")
        
        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        print("Add to Basket button clicked using JavaScript.")
        
        # Allow time for the item to be added to the basket
        time.sleep(3)  

        # Step 12: Wait for the page to navigate to the basket page
        WebDriverWait(driver, 10).until(
            EC.url_contains("/cart")
        )
        print("Navigated to the basket page.")
        time.sleep(3)  # Allow time for the basket page to load

        # Step 13: Click the 'Remove' button to remove the product from the cart
        try:
            remove_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Remove']"))
            )
            remove_button.click()
            print("Remove button clicked.")
            time.sleep(2)  # Allow time for the removal action

            # Handle the pop-up by clicking the 'Remove' button within the pop-up
            confirm_remove_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Remove']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", confirm_remove_button)
            time.sleep(2)
            confirm_remove_button.click()
            print("Product removed from the cart.")
            time.sleep(3)  # Allow time for the removal confirmation

        except ElementClickInterceptedException:
            print("ElementClickInterceptedException: Remove button is not clickable. Trying alternative approach.")

    except ElementClickInterceptedException:
        print("ElementClickInterceptedException: Add to Basket button is not clickable. Trying alternative approach.")

    print("Product Title:", product_title)
    print("Product Price:", product_price)

except TimeoutException as e:
    print("An element was not found within the given time:", e)
except NoSuchElementException as e:
    print("Element not found:", e)

finally:
    time.sleep(5)
    # Close the WebDriver
    driver.quit()
