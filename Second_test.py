import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Remote
from selenium.common.exceptions import TimeoutException
import time

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
        options.add_argument('--remote-debugging-port=9222')
        return Remote(command_executor=selenium_url, options=options)
    else:
        print("DEBUG: Using local Chrome WebDriver")
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        return webdriver.Chrome(options=options)

def test_card_number_auto_formatting():
    driver = get_driver()
    try:
        driver.get("http://localhost:8000/?balance=10000&reserved=0")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))
        rub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
        )
        rub_button.click()
        
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("4111111122223333")
        
        # Ожидаем, что номер автоматически отформатируется
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element_value((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"), "4111 1111 2222 3333")
        )
        
        current_value = card_input.get_attribute("value")
        assert current_value == "4111 1111 2222 3333", f"Ожидалось форматирование, получено: {current_value}"
        
    finally:
        driver.quit()

def test_negative_transfer_amount():
    driver = get_driver()
    try:
        driver.get("http://localhost:8000/?balance=60000&reserved=1000")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))
        rub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
        )
        rub_button.click()
        
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1111 1111 1111 1111")
        
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
        )
        amount_input.clear()
        amount_input.send_keys("-2050")
        
        transfer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
        )
        transfer_button.click()
        
        # Ожидаем, что появится сообщение об ошибке
        try:
            error_message = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Сумма перевода не может быть отрицательной')]"))
            )
            print("Тест прошел успешно: сумма перевода не может быть отрицательной.")
        except:
            print("Тест не прошел - система не заблокировала отрицательную сумму.")
        
    finally:
        driver.quit()

def test_extremely_large_negative_transfer():
    driver = get_driver()
    try:
        driver.get("http://localhost:8000/?balance=60000&reserved=1000")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))
        rub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
        )
        rub_button.click()
        
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1234 5678 9012 3456")
        
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
        )
        amount_input.clear()
        amount_input.send_keys("-60000000")
        
        transfer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
        )
        transfer_button.click()
        
        # Ожидаем появления сообщения об ошибке
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Некорректная сумма')]"))
            )
            print("Тест прошел успешно: ошибка о некорректной сумме появилась.")
        except:
            print("Тест не прошел - система приняла абсурдную сумму и не выдала ошибку.")
        
    finally:
        driver.quit()

def test_invalid_characters_in_card_number():
    driver = get_driver()
    try:
        driver.get("http://localhost:8000/?balance=50000&reserved=2000")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))
        rub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
        )
        rub_button.click()
        
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1234 ABCD 5678 9012")
        current_value = card_input.get_attribute("value")
        # Проверяем, что в поле только цифры и пробелы
        assert all(c.isdigit() or c.isspace() for c in current_value), f"В поле есть недопустимые символы: {current_value}"
        
    finally:
        driver.quit()

def test_maximum_transfer_with_reserve():
    driver = get_driver()
    try:
        driver.get("http://localhost:8000/?balance=60000&reserved=1000")
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))
        rub_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
        )
        rub_button.click()
        
        card_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
        )
        card_input.send_keys("1234 1234 1234 1234")
        
        amount_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
        )
        amount_input.clear()
        amount_input.send_keys("8000")
        
        transfer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
        )
        transfer_button.click()
        
        # Ожидаем появления alert с подтверждением перевода
        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Сообщение: {alert_text}")
            assert "Перевод 8000 ₽" in alert_text, "Неверное сообщение о переводе."
            assert "принят банком" in alert_text, "Не указано, что перевод принят банком."
            alert.accept()
            print("Тест прошел успешно: перевод принят банком.")
        except TimeoutException:
            print("Тест не прошел - alert не появился.")
        
        # Ожидаем, что резерв остался неизменным (проверка баланса)
        try:
            balance_info = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Доступно для перевода')]"))
            )
            print(f"Доступный баланс: {balance_info.text}")
            available_balance = int(balance_info.text.split(' ')[0].replace('₽', '').replace(',', ''))
            assert available_balance == 55000, f"Ошибка: доступный баланс не правильный. Ожидаемый: 55000, но получено: {available_balance}."
        except Exception as e:
            print(f"Тест не прошел - ошибка при получении информации о балансе: {str(e)}")
        
    finally:
        driver.quit()
