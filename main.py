from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import time
import json

def find_id(id_input, driver, maxWait=10):
    btn = WebDriverWait(driver, maxWait).until(
        EC.element_to_be_clickable((By.ID, id_input))
    )
    return btn

def find_text(x_path_input, driver, maxWait=10):
    btn = WebDriverWait(driver, maxWait).until(
        EC.element_to_be_clickable((By.XPATH, x_path_input))
    )
    return btn

def find_css_selector(css_input, driver, maxWait=10):
    btn = WebDriverWait(driver, maxWait).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_input))
    )
    return btn

def find_and_enter_text_input_by_id(text_input, element_id, driver, maxWait=10):
    input = WebDriverWait(driver, maxWait).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    input.send_keys(text_input)

def spam_click_button(input_button, end_condition, driver, second_end_condition = None, clickDelay=0.1):
    while True:
        try:
            # if end condition found, stop
            if WebDriverWait(driver, clickDelay).until(EC.presence_of_element_located(end_condition)):
                break
            if second_end_condition != None:
                if WebDriverWait(driver, clickDelay).until(EC.presence_of_element_located(second_end_condition)):
                    break
        except TimeoutException:
            # no end condition: keep clicking
            try:
                ActionChains(driver).click(input_button).perform()
                time.sleep(clickDelay)
            except ElementNotInteractableException:
                pass

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

    # choose pickup, delivery, or shipping
    try:
        purchase_option_str = "//span[text()='" + data["purchase-type"].capitalize() + "']"
        purchase_option_btn = find_text(purchase_option_str, driver, 3)
        ActionChains(driver).click(purchase_option_btn).perform()
    except:
        print("No choices. Shipping automatically chosen.")

    # add to cart
    driver.execute_script("window.scrollBy(0, 650);")
    time.sleep(0.5)
    # spam until theres something in cart
    add_to_cart_btn = find_css_selector("button[id*='addToCartButtonOrTextIdFor']", driver)
    spam_click_button(add_to_cart_btn, (By.XPATH, "//a[text()='View cart & check out']"), driver)
    driver.get("https://www.target.com/cart")

    # sign in process
    check_out_btn = find_text("//button[text()='Sign in to check out']", driver)
    spam_click_button(check_out_btn, (By.ID, "login"), driver)

    find_and_enter_text_input_by_id(data["username"], "username", driver)
    submit_user_btn = find_id("login", driver)
    spam_click_button(submit_user_btn, (By.XPATH, "//span[text()='Enter your password']"), driver)

    find_and_enter_text_input_by_id(data["password"], "password", driver)
    submit_pw_btn = find_text("//button[text()='Sign in with password']", driver)
    spam_click_button(submit_pw_btn, (By.XPATH, "//a[text()='Skip']"), driver, (By.XPATH, "//a[text()='Skip']"))

    # mobile phone authentication
    try:
        skip_mobile_btn = find_text("//a[text()='Skip']", driver)
        ActionChains(driver).click(skip_mobile_btn).perform()
        print("Skipped mobile phone authentication")
    except:
        print("Mobile phone authentication does not exist. Continuing...")

    # birthday (why is this even a thing)
    try:
        skip_birthday_btn = find_id("EnrollmentMaybeLaterButton", driver)
        ActionChains(driver).click(skip_birthday_btn).perform()
        print("Skipped birthday input")
    except:
        print("Birthday input does not exist. Continuing...")

    # Enter payment information
    add_credit_checkbox = find_id("AddCreditDebitCellRadio", driver, 3)
    ActionChains(driver).click(add_credit_checkbox).perform()
    save_card_btn = find_id("saveCard", driver)
    ActionChains(driver).click(save_card_btn).perform()

    find_and_enter_text_input_by_id(data["card-number"], "credit-card-number-input", driver)
    find_and_enter_text_input_by_id(data["expiration"], "credit-card-expiration-input", driver)
    find_and_enter_text_input_by_id(data["cvv"], "credit-card-cvv-input", driver)
    find_and_enter_text_input_by_id(data["name-on-card"], "credit-card-name-input", driver)

    find_and_enter_text_input_by_id(data["address-line-1"], "billing-address-first-name-input", driver)
    # address line 2 if needed
    if data["address-line-2"] != "":
        find_text("//button[text()='+ Address line 2']", driver)
        find_and_enter_text_input_by_id(data["address-line-2"], "billing-address-line2-input", driver)

    find_and_enter_text_input_by_id(data["zip-code"], "billing-address-zip-code-input", driver)
    find_and_enter_text_input_by_id(data["city"], "billing-address-city-input", driver)
    # state should autocomplete
    find_and_enter_text_input_by_id(data["phone"], "billing-address-phone-input", driver)

    save_billing_btn = find_text("//button[text()='Save and continue']", driver)
    spam_click_button(save_billing_btn, (By.CSS_SELECTOR, "button[disabled='']"))

    # place order
    time.sleep(0.5)
    place_order_btn = find_text("//button[text()='Place your order']", driver)
    spam_click_button(place_order_btn, (By.XPATH, "//h1[text()='Thanks for your order!']"))

    # Wait to see the results, then close the browser safely
    print("Order successfully placed; check email for confirmation details")
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
# ActionChains(driver).click(btn).perform()

'''
<button class="styles_btn__zZcJr styles_ndsButton__VgXft styles_md__N9Usy styles_filled__uq68y styles_fullWidth__ztP_d" type="button" data-test="placeOrderButton" fdprocessedid="5j8yif">Place your order</button>
<button class="styles_btn__zZcJr styles_ndsButton__VgXft styles_md__N9Usy styles_filled__uq68y styles_fullWidth__ztP_d" type="button" data-test="placeOrderButton" disabled="">Place your order</button>
'''
