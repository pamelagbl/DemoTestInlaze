import re
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.ID, "email")
        self.password_field = (By.XPATH, "//*[@id='password']")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.show_hide_button = (By.CLASS_NAME, 'fa-eye')
        self.label = (By.XPATH, "//div[@class='flex gap-4 items-center']//h2[@class='font-bold']")
        self.button_disabled = (By.CSS_SELECTOR, "button[type='submit']")
        self.message = (By.XPATH, "//div[@class='ml-3 text-sm font-normal']")
        self.message_email = (By.XPATH, "//div[normalize-space()='User not found']")

    def enter_email(self, email):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)
        )
        element.send_keys(email)

    def enter_password(self, password):
        show_hide_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.show_hide_button)
        )
        show_hide_button.click()

        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.password_field)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().send_keys(password).perform()

    def click_login(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def login_button_disabled(self):
        login_button_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.login_button)
        )
        return not login_button_element.is_enabled()

    def get_user_login(self):
        user_name_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.label)
        )
        return user_name_element.text

    def invalid_password(self):
        return WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.message)
        ).text

    def is_valid_login_password(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe contener al menos una letra mayúscula."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return False, "La contraseña debe contener al menos un dígito."
        if not re.search(r"[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};':\"\|,.<>\/?]", password):
            return False, "La contraseña debe contener al menos un carácter especial."
        return True, ""


    def invalid_email(self):
        return WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.message)
        ).text
