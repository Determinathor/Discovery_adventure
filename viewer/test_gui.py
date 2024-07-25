import time


from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GuiTestWithSelenium(TestCase):

    # def test_home_page_chrome(self):
    #     selenium_webdriver = webdriver.Chrome()
    #     selenium_webdriver.get('http://127.0.0.1:8000/')
    #     time.sleep(5)
    #     assert 'Kategorie' in selenium_webdriver.page_source

    # def test_signup(self):
    #     selenium_webdriver = webdriver.Chrome()
    #     selenium_webdriver.get('http://127.0.0.1:8000/')
    #     time.sleep(5)
    #     wait = WebDriverWait(selenium_webdriver,1)
    #
    #     dropdown_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle')))
    #     dropdown_toggle.click()
    #     time.sleep(2)
    #
    #     signup_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-target="#signupModal"]')))
    #     signup_link.click()
    #     time.sleep(2)
    #
    #     signup_modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#signupModal')))
    #     assert signup_modal.is_displayed()
    #     time.sleep(2)
    #
    #     signup_username_input = signup_modal.find_element(By.NAME, 'username')
    #     signup_username_input.send_keys('white_wizzard')
    #     time.sleep(2)
    #     signup_first_name_input = signup_modal.find_element(By.NAME, 'first_name')
    #     signup_first_name_input.send_keys('Gandalf')
    #     time.sleep(2)
    #     signup_last_name_input = signup_modal.find_element(By.NAME, 'last_name')
    #     signup_last_name_input.send_keys('The Grey')
    #     time.sleep(2)
    #     signup_email_input = signup_modal.find_element(By.NAME, 'email')
    #     signup_email_input.send_keys('gandalfwhite@saruman.com')
    #     time.sleep(2)
    #     signup_address_input = signup_modal.find_element(By.NAME, 'address')
    #     signup_address_input.send_keys('By The River 6')
    #     time.sleep(2)
    #     signup_phone_input = signup_modal.find_element(By.NAME, 'phone_number')
    #     signup_phone_input.send_keys('122333444')
    #     time.sleep(2)
    #     signup_city_input = signup_modal.find_element(By.NAME, 'city')
    #     signup_city_input.send_keys('Rivendell')
    #     time.sleep(2)
    #     signup_password1_input = signup_modal.find_element(By.NAME, 'password1')
    #     signup_password1_input.send_keys('Securepassword_123')
    #     time.sleep(2)
    #     signup_password2_input = signup_modal.find_element(By.NAME, 'password2')
    #     signup_password2_input.send_keys('Securepassword_123')
    #     time.sleep(2)
    #
    #     signup_submit_button = signup_modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    #     signup_submit_button.click()
    #     time.sleep(2)
    #
    #     wait.until(EC.url_to_be('http://127.0.0.1:8000/'))  # redirect domů
    #     time.sleep(2)
    #     assert 'Registrace byla úspěšná, nyní se můžete přihlásit.' in selenium_webdriver.page_source

    # def test_login_valid(self):
    #     selenium_webdriver = webdriver.Chrome()
    #     selenium_webdriver.get('http://127.0.0.1:8000/')
    #     time.sleep(5)
    #     wait = WebDriverWait(selenium_webdriver,1)
    #
    #     dropdown_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle')))
    #     dropdown_toggle.click()
    #     time.sleep(2)
    #
    #     login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-target="#loginModal"]')))
    #     login_link.click()
    #     time.sleep(2)
    #
    #     login_modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loginModal')))
    #     assert login_modal.is_displayed()
    #     time.sleep(2)
    #
    #     login_username_input = login_modal.find_element(By.NAME, 'username')
    #     login_username_input.send_keys('white_wizzard')
    #     time.sleep(2)
    #
    #     login_password_input = login_modal.find_element(By.NAME, 'password')
    #     login_password_input.send_keys('Securepassword_123')
    #     time.sleep(2)
    #
    #     login_submit_button = login_modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    #     login_submit_button.click()
    #     time.sleep(2)
    #
    #     wait.until(EC.url_to_be('http://127.0.0.1:8000/'))  # redirect domů
    #     time.sleep(2)
    #     assert 'Přihlášení bylo úspěšné.' in selenium_webdriver.page_source


    def test_login_user_does_not_exist(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        time.sleep(5)
        wait = WebDriverWait(selenium_webdriver,1)

        dropdown_toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle')))
        dropdown_toggle.click()
        time.sleep(2)

        login_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-target="#loginModal"]')))
        login_link.click()
        time.sleep(2)

        login_modal = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#loginModal')))
        assert login_modal.is_displayed()
        time.sleep(2)

        login_username_input = login_modal.find_element(By.NAME, 'username')
        login_username_input.send_keys('neexistujiciuser')
        time.sleep(2)

        login_password_input = login_modal.find_element(By.NAME, 'password')
        login_password_input.send_keys('Securepassword_123')
        time.sleep(2)

        login_submit_button = login_modal.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_submit_button.click()
        time.sleep(2)

        wait.until(EC.url_to_be('http://127.0.0.1:8000/'))  # redirect domů
        time.sleep(2)
        assert 'Nelze se přihlásit. Uživatelské jméno neexistuje. Chcete se registrovat?' in selenium_webdriver.page_source



