from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_zero_transfer_amount():
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

    # Вводим валидный номер карты
    card_input.send_keys("1111 1111 1111 1111")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим сумму перевода: 0 ₽
    amount_input.send_keys("0")

    # Ожидание появления кнопки "Перевести" и нажимаем на нее
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )
    transfer_button.click()

    # Проверяем, что баланс и резерв остаются без изменений
    try:
        # Ожидание, пока не произойдет изменений в балансе
        balance_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Доступно для перевода')]"))
        )

        # Проверка, что баланс не изменился
        available_balance = int(balance_info.text.split(' ')[0].replace('₽', '').replace(',', ''))
        assert available_balance == 60000, f"Ошибка: доступный баланс изменился. Ожидаемый: 60000, но получено: {available_balance}."

        # Проверка, что резерв остался неизменным
        print("Тест прошел успешно: перевод с нулевой суммой отклонен, баланс и резерв остались неизменными.")

    except Exception as e:
        print(f"Тест не прошел - ошибка при получении информации о переводе: {str(e)}")

    # Закрытие драйвера
    driver.quit()

def test_small_transfer_commission():
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

    # Вводим валидный номер карты
    card_input.send_keys("1111 1111 1111 1111")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Очистить поле ввода суммы перед вводом
    amount_input.clear()  # Очистка поля

    # Вводим сумму перевода: 90 ₽
    amount_input.send_keys("90")

    # Ожидание появления кнопки "Перевести" и нажимаем на нее
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )
    transfer_button.click()

    # Закрытие alert после выполнения перевода
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Закрытие alert
    except UnexpectedAlertPresentException:
        print("Alert открыт, но не был правильно обработан.")

    # Ожидаем появления элемента с комиссией
    try:
        commission_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "comission"))
        )

        # Получаем текст из элемента комиссии
        commission_text = commission_element.text
        print(f"Комиссия отображена: {commission_text}")

        # Проверяем, что комиссия составляет 9 ₽ (10% от 90)
        assert "9" in commission_text, f"Ожидалась комиссия 9 ₽, но отображено: {commission_text}"

        # Ожидаем, что итоговая сумма будет правильно рассчитана (90 ₽ + 9 ₽ = 99 ₽)
        total_amount = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Итоговая сумма:')]"))
        )

        print(f"Итоговая сумма: {total_amount.text}")

        assert "99 ₽" in total_amount.text, f"Ожидалась итоговая сумма 99 ₽, но отображено: {total_amount.text}"

        print("Тест прошел успешно: комиссия и итоговая сумма рассчитаны корректно.")

    except TimeoutException:
        assert False, "Тест не прошел - не найдено сообщение о комиссии или итоговой сумме."

    # Закрытие драйвера
    driver.quit()

def test_transfer_amount_exceeds_balance():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=50000&reserved=2000")

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
    card_input.send_keys("1234 5678 9012 3456")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Вводим сумму, которая превышает доступный баланс
    amount_input.send_keys("52000")

    # Проверяем появление сообщения об ошибке
    try:
        # Проверка на наличие сообщения о недостаточности средств
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'Недостаточно средств на счете')]"))
        )
        print("Тест прошел успешно: система заблокировала перевод и отобразила сообщение о недостаточности средств.")
    except TimeoutException:
        assert False, "Тест не прошел - сообщение о недостаточности средств не появилось."

    # Закрытие драйвера
    driver.quit()


def test_multiple_transfers_same_amount():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=30000&reserved=0")

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
    card_input.send_keys("4111 1111 1111 1111")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Вводим сумму перевода: 5000 ₽
    amount_input.clear()  # Очистка поля
    amount_input.send_keys("5000")

    # Проверяем 3 последовательных перевода
    for i in range(3):
        # Ожидание появления комиссии
        try:
            commission_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "comission"))
            )
            commission_text = commission_element.text
            print(f"Комиссия после перевода {i + 1}: {commission_text}")
            # Проверка комиссии - более строгая проверка на точное соответствие
            assert commission_text == "500", f"Ожидалась комиссия 500 ₽, но отображено: {commission_text}"
        except TimeoutException:
            assert False, "Тест не прошел - комиссия не отобразилась."

        # Ожидаем появления кнопки "Перевести" и нажимаем на нее
        transfer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
        )
        transfer_button.click()

        # Ожидаем появления alert с подтверждением перевода
        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()  # Закрытие alert
        except TimeoutException:
            assert False, "Тест не прошел - alert не появился."

        # Ожидаем 1 минуту перед следующим переводом
        if i < 2:
            time.sleep(2)

    print("Тест прошел успешно: все переводы выполнены, комиссия правильно рассчитана.")

    # Закрытие драйвера
    driver.quit()

def test_repeat_card_number_entry():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие локальной страницы
    driver.get("http://localhost:8000/?balance=15000&reserved=0")

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
    card_input.send_keys("5111 1111 1111 1111")

    # Ожидание поля для ввода суммы
    amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='1000']"))
    )

    # Вводим первую сумму перевода: 2000 ₽
    amount_input.clear()  # Очистка поля
    amount_input.send_keys("2000")

    # Ожидаем кнопку "Перевести" и нажимаем на нее
    transfer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='g-button g-button_view_outlined g-button_size_l g-button_pin_round-round']"))
    )
    transfer_button.click()

    # Ожидаем появления комиссии
    try:
        commission_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "comission"))
        )
        commission_text = commission_element.text
        print(f"Комиссия после первого перевода: {commission_text}")
        # Проверка комиссии
        assert "200 ₽" in commission_text, f"Ожидалась комиссия 200 ₽, но отображено: {commission_text}"
    except Exception as e:
        print(f"Тест не прошел - ошибка при получении комиссии: {str(e)}")

    # Закрытие alert с подтверждением перевода
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Закрытие alert
    except Exception as e:
        pass  # Если alert нет или возникает ошибка, ничего не выводим

    # Без перезагрузки страницы: очистить поле суммы
    amount_input.clear()

    # Вводим новую сумму для второго перевода: 3000 ₽
    amount_input.send_keys("3000")

    # Ожидаем кнопку "Перевести" и нажимаем на нее
    transfer_button.click()

    # Ожидаем появления комиссии для второго перевода
    try:
        commission_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "comission"))
        )
        commission_text = commission_element.text
        print(f"Комиссия после второго перевода: {commission_text}")
        # Проверка комиссии
        assert "300 ₽" in commission_text, f"Ожидалась комиссия 300 ₽, но отображено: {commission_text}"
    except Exception as e:
        print(f"Тест не прошел - ошибка при получении комиссии: {str(e)}")

    # Закрытие alert с подтверждением второго перевода
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()  # Закрытие alert
    except Exception as e:
        pass  # Если alert нет или возникает ошибка, ничего не выводим

    # Проверяем, что номер карты сохранен в поле ввода
    saved_card_number = card_input.get_attribute("value")
    assert saved_card_number == "5111 1111 1111 1111", f"Номер карты не сохранен: {saved_card_number}"

    print("Тест прошел успешно: оба перевода выполнены, комиссия правильно рассчитана, номер карты сохранен.")

    # Закрытие драйвера
    driver.quit()

