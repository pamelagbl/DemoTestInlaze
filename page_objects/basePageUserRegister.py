import re

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class RegisterUserPage:
    def __init__(self, driver):
        self.driver = driver
        self.password = None
        self.confirm_password = None
        self.fullname_field = (By.ID, "full-name")
        self.email_field = (By.ID, "email")
        self.password_field = (By.ID, "password")
        self.repeat_password_field = (By.ID, "confirm-password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.success_registration = (By.CSS_SELECTOR, ".ml-3.text-sm.font-normal")
        self.error_message = "Email ya registrado"
        self.error_message_email = "El campo email no cumple con el formato test@dominio.com"
        self.txt_error = (By.CSS_SELECTOR, ".label-text-alt.text-error")

    def enter_full_name(self, fullname):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.fullname_field)
        )
        element.send_keys(fullname)

    def enter_email(self, email):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)
        )
        element.send_keys(email)

    def enter_password_field(self, password):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "password"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().send_keys(password).perform()
        self.password = password

    def enter_confirm_password_field(self, confirm_password):
        element = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.repeat_password_field)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().send_keys(confirm_password).perform()
        self.confirm_password = confirm_password

    def passwords_match(self):
        return self.password == self.confirm_password

    def click_login(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

    def get_successfully_registration(self):
        user_name_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.success_registration)
        )
        return user_name_element.text

    def get_error_registration(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message)
        ).text

    def get_error_registration_email(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.error_message_email)
        ).text

    def get_error_message(self):
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.txt_error)
        )
        return element.text

    def login_button_disabled(self):
        login_button_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.login_button)
        )
        return not login_button_element.is_enabled()

    def valid_email_format(self, email_invalid):
        # Validar el formato del correo electrónico usando una expresión regular
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email_invalid) is not None

    def get_email(self):
        return self.driver.find_element(By.ID, "email").get_attribute('value')

    def validate_password_format(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres."
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe contener al menos una letra mayúscula."
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe contener al menos una letra minúscula."
        if not re.search(r"\d", password):
            return False, "La contraseña debe contener al menos un dígito."
        if not re.search(r"[!@#\$%\^&\*\(\)_\+\-=\[\]\{\};':\"\|,.<>\/?]", password):
            return False, "La contraseña debe contener al menos un carácter especial."
        return True, ""

    def sign_up_button_disabled(self):
        login_button_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.login_button)
        )
        return not login_button_element.is_enabled()

    def sign_up_button_enabled(self):
        login_button_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.login_button)
        )
        return login_button_element.is_enabled()

    @staticmethod
    def is_valid_full_name(full_name):
        if re.fullmatch(r"[A-Za-z\s]+", full_name):
            return True

        return False

    def get_full_name_field_value(self):
        return self.driver.find_element(By.ID, "full-name").get_attribute('value')
