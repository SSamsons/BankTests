import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_selenium_connection():
    """Простой тест для проверки подключения к Selenium"""
    print("Starting Selenium connection test...")
    
    selenium_url = os.getenv("SELENIUM_REMOTE_URL", None)
    print(f"SELENIUM_REMOTE_URL: {selenium_url}")
    
    try:
        if selenium_url:
            print("Attempting to connect to remote Selenium...")
            from selenium.webdriver import Remote
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            driver = Remote(command_executor=selenium_url, options=options)
            print("Successfully connected to remote Selenium")
        else:
            print("Using local Chrome driver...")
            driver = webdriver.Chrome()
            print("Successfully started local Chrome driver")
        
        # Простая проверка - открываем Google
        print("Opening test page...")
        driver.get("https://www.google.com")
        
        # Проверяем, что страница загрузилась
        title = driver.title
        print(f"Page title: {title}")
        assert "Google" in title, f"Expected Google in title, got: {title}"
        
        print("Test passed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        raise
    finally:
        try:
            driver.quit()
            print("Driver closed successfully")
        except:
            print("Failed to close driver")

def test_localhost_connection():
    """Тест подключения к localhost:8000"""
    print("Starting localhost connection test...")
    
    selenium_url = os.getenv("SELENIUM_REMOTE_URL", None)
    
    try:
        if selenium_url:
            from selenium.webdriver import Remote
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            driver = Remote(command_executor=selenium_url, options=options)
        else:
            driver = webdriver.Chrome()
        
        print("Attempting to connect to localhost:8000...")
        driver.get("http://localhost:8000")
        
        # Проверяем, что страница загрузилась (любая)
        title = driver.title
        print(f"Localhost page title: {title}")
        
        # Ищем любой элемент на странице
        body = driver.find_element(By.TAG_NAME, "body")
        print("Page body found successfully")
        
        print("Localhost test passed!")
        
    except Exception as e:
        print(f"Localhost test failed: {e}")
        raise
    finally:
        try:
            driver.quit()
        except:
            pass 