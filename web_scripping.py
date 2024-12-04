from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pyautogui

# Set up the Chrome WebDriver
driver = webdriver.Chrome()  # Or specify the path if not in PATH

# Open Swiggy and log in manually (for security reasons, login automation is complex)
driver.get("https://www.swiggy.com/")
input("Please log in to your Swiggy account, then press Enter to continue...")

# Navigate to the Orders page
driver.get("https://www.swiggy.com/my-account/orders")

# Wait for orders to load
time.sleep(5)

# Perform the scroll-and-click action 30 times to load all orders
for _ in range(30):
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load more orders

        # Find the button and click it
        button = driver.find_element(By.CLASS_NAME, "_2uho9")
        button.click()
        time.sleep(2)  # Wait for more orders to load
    except Exception as e:
        print("Error during scroll and click:", e)
        break

# Allow some time for the last batch of orders to load
time.sleep(5)

# Locate all order elements after loading all pages
orders = driver.find_elements(By.XPATH, "//div[contains(@class, '_3olXG')]")

# Create a folder to save screenshots
if not os.path.exists("Swiggy_Invoices_FullScreen"):
    os.makedirs("Swiggy_Invoices_FullScreen")

# Loop over each order and take a full desktop screenshot of the bill details
for i, order in enumerate(orders):
    try:
        order.click()  # Open the order details
        time.sleep(2)

        # Take a full desktop screenshot and save it using pyautogui
        screenshot_path = f"Swiggy_Invoices_FullScreen/invoice_{i+1}.png"
        pyautogui.screenshot(screenshot_path)
        print(f"Full desktop screenshot saved: {screenshot_path}")
        
        # Close the bill details to return to order list
        close_button = driver.find_element(By.XPATH, "//span[contains(@class, '_1X6No icon-close')]")
        close_button.click()
        time.sleep(1)
    except Exception as e:
        print(f"Could not capture screenshot for order {i+1}: {e}")
        # Attempt to close the bill details if an error occurs
        try:
            close_button = driver.find_element(By.XPATH, "//span[contains(@class, '_1X6No icon-close')]")
            close_button.click()
        except:
            pass

# Close the browser
driver.quit()