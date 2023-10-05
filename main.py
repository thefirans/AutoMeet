from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import threading
import time
from webdriver_manager.chrome import ChromeDriverManager
import config as cf
from selenium.webdriver.common.by import By


def start():
    username, password = enter_log_pass()

    driver = run_driver()

    driver.get(
        "https://accounts.google.com/ServiceLogin/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F&followup=https%3A%2F%2Fclassroom.google.com%2F&emr=1&flowName=GlifWebSignIn&flowEntry=AddSession")

    # Enter username
    enter_text(driver, By.ID, 'identifierId', username)
    click_element(driver, By.XPATH, '//*[@id="identifierNext"]/div/button/span')
    time.sleep(5)

    # Enter password
    enter_text(driver, By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input', password)
    click_element(driver, By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    time.sleep(5)

    # Find and enter the needed class

    # For now, it manually added class name that we need to click
    target_class = "2023 (осінь) Завадостійке кодування та захист біомедичної інфор"

    elements = driver.find_elements(By.CLASS_NAME, "YVvGBb.z3vRcc-ZoZQ1")

    # Parser
    # element_text_list = [element.text for element in elements]

    for element in elements:
        if element.text == target_class:
            element.click()
            break

    # Click on button to join Meet conference
    time.sleep(2)
    meet_button = find_element(driver, By.XPATH,
                               '//*[@id="yDmH0d"]/c-wiz[2]/div[2]/div/div[7]/div[2]/aside/div/div[1]/div/div[2]/div/a')
    meet_button.click()

    # Switch to tab with conference
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(2)

    off_mic_video(driver)

    # Click on Join button
    join_button = find_element(driver, By.XPATH,
                                      '//*[@id="yDmH0d"]/c-wiz/div/div/div[15]/div[3]/div/div[2]/div[4]/div/div/div['
                                      '2]/div[1]/div[2]/div[1]/div[1]')
    join_button.click()

    time.sleep(5000)


def off_mic_video(driver):
    elements = find_elements(driver, By.CLASS_NAME, 'GKGgdd')
    print(elements)

    elements[0].click()
    time.sleep(0.5)

    elements[1].click()
    time.sleep(0.5)


def run_driver():
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

    return driver


def find_element(driver, by, value):
    return driver.find_element(by, value)


def find_elements(driver, by, value):
    return driver.find_elements(by, value)


def click_element(driver, by, value):
    element = find_element(driver, by, value)
    element.click()


def enter_text(driver, by, value, text):
    element = find_element(driver, by, value)
    element.click()
    element.send_keys(text)


def enter_log_pass():
    username = input("Enter your school Gmail: ")
    password = input("Enter your password: ")
    return username, password


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
