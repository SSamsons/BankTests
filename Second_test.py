from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_card_number_auto_formatting():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=10000&reserved=0")

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

    # Вводим номер карты без пробелов
    card_input.send_keys("4111111122223333")

    # Ожидаем, что номер автоматически отформатируется
    formatted_number = WebDriverWait(driver, 3).until(
        EC.text_to_be_present_in_element_value((By.XPATH, "//input[@placeholder='0000 0000 0000 0000']"), "4111 1111 2222 3333")
    )

    # Проверяем, что номер отформатирован
    assert formatted_number, "Номер карты не отформатирован корректно."

    # Закрытие драйвера
    driver.quit()

def test_negative_transfer_amount():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=60000&reserved=1000")

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
    card_input.send_keys("1111 1111 1111 1111")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим отрицательную сумму
    amount_input.send_keys("-2050")

    # Ожидаем появление кнопки "Перевести" и нажимаем на нее
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

    # Закрытие драйвера
    driver.quit()


def test_extremely_large_negative_transfer():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=60000&reserved=1000")

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
    card_input.send_keys("1234 5678 9012 3456")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим аномально большую отрицательную сумму
    amount_input.send_keys("-60000000")

    # Ожидание появления кнопки "Перевести" и нажимаем на нее
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

    # Закрытие драйвера
    driver.quit()

def test_invalid_characters_in_card_number():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=50000&reserved=2000")

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

    # Вводим буквы в поле номера карты
    card_input.send_keys("1234 ABCD 5678 9012")  # Вводим буквы и цифры

    # Проверяем, что буквы были заблокированы и поле содержит только цифры
    current_value = card_input.get_attribute("value")

    # Ожидаем, что в поле будут только цифры, без букв
    assert current_value == "1234 5678 9012", f"Тест не прошел: введенные буквы не были заблокированы. Текущее значение: {current_value}"

    # Закрытие драйвера
    driver.quit()


def test_maximum_transfer_with_reserve():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=60000&reserved=1000")

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
    card_input.send_keys("1234 1234 1234 1234")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим сумму перевода: 8000 ₽, комиссия 800 ₽, общая сумма = 8800 ₽
    amount_input.send_keys("8000")

    # Ожидание появления кнопки "Перевести" и нажимаем на нее
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )
    transfer_button.click()

    # Ожидаем появления alert с подтверждением перевода
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

        # Получаем текст из alert
        alert_text = alert.text
        print(f"Сообщение: {alert_text}")

        # Проверяем, что сообщение о переводе содержит нужные данные
        assert "Перевод 8000 ₽" in alert_text, "Неверное сообщение о переводе."
        assert "принят банком" in alert_text, "Не указано, что перевод принят банком."

        # Закрыть alert
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

        # Проверяем, что резерв не был использован для перевода
        available_balance = int(balance_info.text.split(' ')[0].replace('₽', '').replace(',', ''))
        assert available_balance == 55000, f"Ошибка: доступный баланс не правильный. Ожидаемый: 55000, но получено: {available_balance}."

    except Exception as e:
        print(f"Тест не прошел - ошибка при получении информации о балансе: {str(e)}")

    # Закрытие драйвера
    driver.quit()
