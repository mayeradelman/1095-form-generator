from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import pyautogui 

# Path to the directory containing PDFs
pdf_directory = r'C:\Users\mayer\Desktop\pdf-project\foo'
download_directory = r'C:\Users\mayer\Desktop\pdf-project\bar'
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]  # List PDF files in the directory

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
    "plugins.always_open_pdf_externally": False,  # Try to open PDFs in Chrome

    "download.default_directory": download_directory,  # Set the default download directory
})
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)  # Full path to the PDF
    pdf_url = f'file:///{pdf_path.replace(os.path.sep, "/")}'  # Convert path to URL format
    driver.get(pdf_url)
    
    # Wait for PDF to load
    time.sleep(2)
    
    # Open print dialog by executing JavaScript
    driver.execute_script('window.print();')
    time.sleep(2)

    # press tab 5 times then down then enter                    
    # pyautogui.press('tab')

                    
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('down')
    pyautogui.press('enter')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # pyautogui.press('tab')
    # # press the "Enter" button on keyboard
    # pyautogui.press('enter')

    time.sleep(30)

# Cleanup: close the browser window
driver.quit()