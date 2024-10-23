from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_current_price(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    service = Service(executable_path='C:\\Users\\RobotComp.ru\\Documents\\webDrivers\\chromedriver-win64\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        price_element = driver.find_element(By.XPATH, '//label[contains(text(), "Начальная цена")]/following-sibling::span//span')
        price_text = price_element.text.strip().replace(' ', '').replace(',', '.')
        print(f"Цена: {price_text} ₽")
        return float(price_text)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        driver.quit()
