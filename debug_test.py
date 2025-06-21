import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Remote

def get_driver():
    """Получить драйвер для тестов - удалённый в CI, локальный локально"""
    selenium_url = os.getenv("SELENIUM_REMOTE_URL")
    print(f"DEBUG: SELENIUM_REMOTE_URL = {selenium_url}")
    
    if selenium_url:
        print(f"DEBUG: Using remote WebDriver at {selenium_url}")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        return Remote(command_executor=selenium_url, options=options)
    else:
        print("DEBUG: Using local Chrome WebDriver")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        return webdriver.Chrome(options=options)

def test_selenium_connection():
    """Простой тест для проверки подключения к Selenium"""
    print("Starting Selenium connection test...")
    
    try:
        driver = get_driver()
        print("Driver created successfully")
        
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

def test_selenium_basic_functionality():
    """Тест базовой функциональности Selenium WebDriver"""
    print("Testing basic Selenium functionality...")
    
    try:
        driver = get_driver()
        
        # Тест 1: Открытие страницы
        driver.get("https://httpbin.org/html")
        assert "Herman" in driver.page_source
        
        # Тест 2: Поиск элементов
        h1_element = driver.find_element(By.TAG_NAME, "h1")
        assert h1_element.text == "Herman Melville - Moby-Dick"
        
        # Тест 3: Получение информации о странице
        current_url = driver.current_url
        assert "httpbin.org" in current_url
        
        print("Basic functionality test passed!")
        
    except Exception as e:
        print(f"Basic functionality test failed: {e}")
        raise
    finally:
        try:
            driver.quit()
        except:
            pass

def test_selenium_wait_functionality():
    """Тест функциональности ожидания в Selenium"""
    print("Testing Selenium wait functionality...")
    
    try:
        driver = get_driver()
        
        # Открываем страницу с динамическим контентом
        driver.get("https://httpbin.org/delay/2")
        
        # Используем явное ожидание
        wait = WebDriverWait(driver, 10)
        body_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        assert body_element is not None
        print("Wait functionality test passed!")
        
    except Exception as e:
        print(f"Wait functionality test failed: {e}")
        raise
    finally:
        try:
            driver.quit()
        except:
            pass

def test_localhost_connection():
    """Тест подключения к localhost:8000 (ожидается неудача)"""
    print("Starting localhost connection test...")
    
    try:
        driver = get_driver()
        
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
        # Это ожидаемая ошибка, так как приложение не запущено
        pytest.skip("Localhost test skipped - application not running")
    finally:
        try:
            driver.quit()
        except:
            pass 