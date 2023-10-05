from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import threading
import time
from webdriver_manager.chrome import ChromeDriverManager
import config as cf
from selenium.webdriver.common.by import By
from config import username_cf, password_cf


def start():
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")

    # Argument 1 to allow, 2 to block
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    })

    service_path = ChromeDriverManager().install()
    service = Service(service_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(
        "https://accounts.google.com/ServiceLogin/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F&followup=https%3A%2F%2Fclassroom.google.com%2F&emr=1&flowName=GlifWebSignIn&flowEntry=AddSession")

    # Enter username
    username = driver.find_element(By.ID, 'identifierId')
    username.click()
    username.send_keys(username_cf)
    proceed = driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span')
    proceed.click()
    time.sleep(5)

    # Enter password
    password = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
    password.click()
    password.send_keys(password_cf)
    proceed2 = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    proceed2.click()

    # Find and enter the needed class
    time.sleep(6)

    # For now, it manually added class name that we need to click
    target_class = "2023 (осінь) Завадостійке кодування та захист біомедичної інфор"

    elements = driver.find_elements(By.CLASS_NAME, "YVvGBb.z3vRcc-ZoZQ1")

    print(elements)

    element_text_list = []

    # Small parser of all classes name
    for element in elements:
        element_text_list.append(element.text)

    for element in elements:
        if element.text == target_class:
            element.click()
            break

    print(element_text_list)
    print(type(element_text_list))

    # Click on button to join Meet conference
    time.sleep(2)
    meet_button = driver.find_element(By.XPATH,
                                      '//*[@id="yDmH0d"]/c-wiz[2]/div[2]/div/div[7]/div[2]/aside/div/div[1]/div/div[2]/div/a')
    meet_button.click()

    # Switch to tab with conference
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    # Find all elements with the class "GKGgdd"
    elements = driver.find_elements(By.CLASS_NAME, 'GKGgdd')

    # Click on the first element
    if elements:
        elements[0].click()
    time.sleep(0.5)

    # Find all elements with the class "GKGgdd" again (to get the second element)
    elements = driver.find_elements(By.CLASS_NAME, 'GKGgdd')

    # Click on the second element
    if len(elements) >= 2:
        elements[1].click()
    time.sleep(0.5)

    # Click on Join button
    join_button = driver.find_element(By.XPATH,
                                      '//*[@id="yDmH0d"]/c-wiz/div/div/div[15]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]')
    join_button.click()

    time.sleep(5000)


def main():
    profiles = []

    for i in range(cf.AMOUNT_THREAD):
        profiles += [threading.Thread(target=start)]

    for i in profiles:
        i.start()

    for i in profiles:
        i.join()


if __name__ == '__main__':
    main()
