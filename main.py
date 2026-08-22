from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

def find_and_click_id(id_input, driver):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, id_input))
    )
    ActionChains(driver).click(btn).perform()

def find_and_click_text(x_path_input, driver):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, x_path_input))
    )
    ActionChains(driver).click(btn).perform()

def find_and_click_css_selector(css_input, driver):
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_input))
    )
    ActionChains(driver).click(btn).perform()

def find_and_enter_text_input_by_id(text_input, element_id, driver):
    input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    input.send_keys(text_input)

def buy():
    # read credentials in json
    with open('info.json', 'r') as file:
        data = json.load(file)

    # open chrome and go to target
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(data["target-link"])

    # check if in stock
    # DEBUG: fix later
    try:
        in_stock = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "h-text-greenDark"))
        )
    except:
        print("Item does not appear to be in stock; closing program")
        time.sleep(2)
        driver.quit()

    # add to cart
    driver.execute_script("window.scrollBy(0, 500);")
    find_and_click_css_selector("button[id*='addToCartButtonOrTextIdFor']", driver)
    driver.get("https://www.target.com/cart")

    # sign in process
    find_and_click_text("//button[text()='Sign in to check out']", driver)
    find_and_enter_text_input_by_id(data["username"], "username", driver)
    find_and_click_id("login", driver)

    find_and_click_text("Enter your password", driver)
    find_and_enter_text_input_by_id(data["password"], "password", driver)
    find_and_click_text("//span[text()='Sign in to check out']", driver)

    # mobile phone authentication
    try:
        find_and_click_text("//a[text()='Skip']", driver)
        print("Skipped mobile phone authentication")
    except:
        print("Mobile phone authentication does not exist. Continuing...")

    # birthday (why is this even a thing)
    try:
        find_and_click_id("EnrollmentMaybeLaterButton", driver)
        print("Skipped birthday input")
    except:
        print("Birthday input does not exist. Continuing...")

    # Enter payment information
    find_and_click_id("AddCreditDebitCellRadio", driver)
    find_and_click_id("save_card", driver)
    find_and_click_id("save-as-default-payment-checkbox", driver)

    find_and_enter_text_input_by_id(data["card-number"], "", driver)
    find_and_enter_text_input_by_id(data["expiration"], "", driver)
    find_and_enter_text_input_by_id(data["cvv"], "", driver)
    find_and_enter_text_input_by_id(data["name-on-card"], "", driver)

    # Enter billing address

    # Wait to see the results, then close the browser safely
    time.sleep(1000)
    driver.quit()

if __name__ == '__main__':
    buy()

# addToCartButtonOrTextIdFor94881673
# addToCartButtonOrTextIdFor15023951
# styles_btn__zZcJr styles_ndsButton__VgXft styles_md__N9Usy styles_filled__uq68y styles_fullWidth__ztP_d
# Sign in to check out
# username
# https://www.target.com/p/mesh-binder-pouch-up-up/-/A-1011020920?preselect=94881673#lnk=sametab
