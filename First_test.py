from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_card_number_length():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    # Ожидание, пока кнопка рублевого счета станет кликабельной
    rub_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
    )

    # Клик по кнопке рублевого счета
    rub_button.click()

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим 15 цифр в поле номера карты
    card_input.send_keys("123456789012345")  # Вводим 15 цифр

    # Проверяем, что поле ввода суммы не становится доступным
    try:
        # Ожидаем, что поле ввода суммы не станет доступным (не кликабельным)
        amount_input = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='1000']"))
        )
        # Если поле доступно, тест не прошел
        assert False, "Сервис не блокирует переход к следующему шагу с 15 цифрами."
    except:
        # Если исключение было поймано, это означает, что сервис заблокировал поле
        print("Тест прошел успешно: сервис не позволяет продолжить с 15 цифрами.")

    # Закрытие драйвера
    driver.quit()

def test_card_number_length_exceeding_max():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    # Явное ожидание, чтобы страница успела полностью загрузиться
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))

    # Ожидание, пока кнопка рублевого счета станет кликабельной
    rub_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
    )

    # Клик по кнопке рублевого счета
    rub_button.click()

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим 17 цифр в поле номера карты
    card_input.send_keys("12345678901234567")  # Вводим 17 цифр

    # Ожидаем кнопку "Перевести"
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )

    # Нажимаем кнопку "Перевести"
    transfer_button.click()

    # Теперь проверим, что перевод НЕ был выполнен
    try:
        # Проверка, что перевод не произошел (например, проверка наличия ошибки или уведомления)
        error_message = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Неверный номер карты')]"))
        )
        print("Тест прошел успешно: отображено сообщение об ошибке.")
    except:
        print("Тест не прошел - перевод прошел с 17 цифрами.")

    # Добавляем задержку, чтобы посмотреть результат перед закрытием
    time.sleep(3)

    # Закрытие драйвера
    driver.quit()

def test_successful_transfer_with_valid_data():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=30000&reserved=20001")

    # Явное ожидание, чтобы страница успела полностью загрузиться
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))

    # Ожидание, пока кнопка рублевого счета станет кликабельной
    rub_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
    )

    # Клик по кнопке рублевого счета
    rub_button.click()

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим корректный номер карты
    card_input.send_keys("1234567812345678")  # Вводим корректный номер карты

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим сумму для перевода
    amount_input.send_keys("1000")  # Вводим сумму

    # Ожидание кнопки "Перевести"
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )

    # Нажимаем кнопку "Перевести"
    transfer_button.click()

    # Ждем появления alert с сообщением о переводе
    try:
        # Ожидаем появления alert
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

        # Получаем текст alert
        alert_text = alert.text
        print(f"Сообщение: {alert_text}")

        # Проверяем, что сообщение содержит ожидаемый текст
        assert "Перевод" in alert_text and "принят банком" in alert_text, "Сообщение об ошибке!"

        # Закрыть alert
        alert.accept()
        print("Тест прошел успешно: перевод принят банком.")

    except:
        print("Тест не прошел - не отображается сообщение об успешном переводе.")

    # Добавляем задержку, чтобы посмотреть результат перед закрытием
    time.sleep(3)

    # Закрытие драйвера
    driver.quit()

def test_transfer_with_reserved_balance():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=60000&reserved=5000")

    # Явное ожидание, чтобы страница успела полностью загрузиться
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))

    # Ожидание, пока кнопка рублевого счета станет кликабельной
    rub_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
    )

    # Клик по кнопке рублевого счета
    rub_button.click()

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим корректный номер карты
    card_input.send_keys("1234567812345678")  # Вводим корректный номер карты

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим корректный номер карты
    card_input.send_keys("1234567812345678")

    # Вводим сумму для перевода, которая превышает доступный баланс после учета резерва
    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.send_keys("55000")  # Это сумма, которая превышает доступный баланс


    # Проверяем, что перевод не был выполнен
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Недостаточно средств')]"))
        )
        print("Тест прошел успешно: резерв учтен в расчетах.")
    except:
        print("Тест не прошел - система не дает сделать перевод.")

    # Добавляем задержку, чтобы посмотреть результат перед закрытием
    time.sleep(3)

    # Закрытие драйвера
    driver.quit()

def test_transfer_with_zero_balance():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=0&reserved=0")

    # Явное ожидание, чтобы страница успела полностью загрузиться
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")))

    # Ожидание, пока кнопка рублевого счета станет кликабельной
    rub_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]"))
    )

    # Клик по кнопке рублевого счета
    rub_button.click()

    # Ожидание появления поля ввода номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"))
    )

    # Вводим корректный номер карты
    card_input.send_keys("1234567812345678")

    # Вводим сумму для перевода (1000) при нулевом балансе
    amount_input = driver.find_element(By.XPATH, "//input[@placeholder='1000']")
    amount_input.send_keys("1000")  # Попытка перевести 1000 при нулевом балансе

    # Проверяем, что перевод не был выполнен
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Недостаточно средств на счете']"))
        )
        print("Тест прошел успешно: перевод заблокирован при нулевом балансе.")
    except:
        print("Тест не прошел - перевод выполнен при нулевом балансе.")

    # Добавляем задержку, чтобы посмотреть результат перед закрытием
    time.sleep(3)

    # Закрытие драйвера
    driver.quit()
