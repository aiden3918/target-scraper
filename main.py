from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

def process():
    with open('info.json', 'r') as file:
        data = json.load(file)

    link = data["target-link"]
    user = data["username"]
    pw = data["password"]

    # Launches a managed Chrome browser instance
    driver = webdriver.Chrome()

    # nav to target
    driver.get(link)

    # check if in stock
    try:
        in_stock = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "h-text-greenDark"))
        )
    except:
        print("Item does not appear to be in stock; closing program")
        time.sleep(2)
        driver.quit()

    # add to cart
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id*='addToCartButtonOrTextIdFor']"))
    )
    ActionChains(driver).click(add_to_cart_button).perform()

    # go to cart
    driver.get("https://www.target.com/cart")

    # sign in process
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in to check out']"))
    )
    ActionChains(driver).click(sign_in_button).perform()

    user_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "username"))
    )
    user_input.send_keys(user)

    log_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign in to check out']"))
    )
    ActionChains(driver).click(log_in_button).perform()

    # Wait to see the results, then close the browser safely
    time.sleep(1000)
    driver.quit()

if __name__ == '__main__':
    process()

# addToCartButtonOrTextIdFor94881673
# addToCartButtonOrTextIdFor15023951
# styles_btn__zZcJr styles_ndsButton__VgXft styles_md__N9Usy styles_filled__uq68y styles_fullWidth__ztP_d
# Sign in to check out
# username
