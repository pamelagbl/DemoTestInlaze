import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from page_objects.basePageUserLogin import LoginPage
from page_objects.basePageUserLogout import LogoutPage
from page_objects.basePageUserRegister import RegisterUserPage
import unittest


class TestUserRegister(unittest.TestCase):
    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.get('https://test-qa.inlaze.com/auth/sign-up')
        self.driver.maximize_window()  # Maximiza la ventana del navegador

    def test_user_register_happy_path(self):
        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test@example.com')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')
        base_page_user_register.click_login()
        success_message = "Successful registration!"

        # Verificamos que el usuario fue redirigido a la página sign-up

        WebDriverWait(self.driver, 10).until(
            EC.url_contains('https://test-qa.inlaze.com/auth/sign-up')
        )
        self.assertIn('https://test-qa.inlaze.com/auth/sign-up', self.driver.current_url)
        print(f"Se ha registrado con éxito al usuario y fue redirigido a la página correspondiente")

        success = base_page_user_register.get_successfully_registration()
        print(f"El mensaje obtenido es: {success}")
        self.assertEqual(success, success_message, f"Se espera que el nombre de usuario sea: {success_message} pero se "
                                                   f"recibió: {success}")

    def test_user_registration_validate_unique_email(self):
        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test@example.com')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')
        base_page_user_register.click_login()

        # Intentar registrar nuevamente con el mismo correo
        self.driver.get("https://test-qa.inlaze.com/auth/sign-up")
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test@example.com')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')
        base_page_user_register.click_login()

        try:
            error = base_page_user_register.get_error_registration()
            print(f"Error message: {error}")
            self.assertEqual(error, "Este correo ya está registrado.", "El mensaje de error no coincide.")
        except Exception as e:
            print("No se encontró mensaje de error, el registro fue permitido.")

    def test_user_registration_validate_email(self):
        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')
        # base_page_user_register.click_login()

        # Validar el formato del correo electrónico antes de hacer clic en registrar

        valid_format = base_page_user_register.valid_email_format(base_page_user_register.get_email())

        if not valid_format:
            print("El formato del correo electrónico no es válido.")

        else:
            base_page_user_register.click_login()
            print("El formato del correo electrónico es válido.")

    def test_user_registration_validate_password(self):
        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test9@example.com')
        password = "SRT2024!"
        confirm_password = "SRT2024!"
        base_page_user_register.enter_password_field(password)
        base_page_user_register.enter_confirm_password_field(confirm_password)

        is_valid_password, message_password = base_page_user_register.validate_password_format(password)
        print(f"Resultado de la validación para la contraseña '{password}': {message_password}")

        self.assertTrue(is_valid_password, f"No se puede registrar usuario por: {message_password}")

        base_page_user_register.click_login()

    def test_user_registration_validate_confirm_password(self):

        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test@example.com')
        password = "Test2024"
        confirm_password = "Test2024"
        base_page_user_register.enter_password_field(password)
        base_page_user_register.enter_confirm_password_field(confirm_password)

        is_valid_confirm_password, message_confirm_password = base_page_user_register.validate_password_format(
            confirm_password)
        print(
            f"Resultado de la validación para la confirmación de la contraseña '{confirm_password}': {message_confirm_password}")

        self.assertTrue(is_valid_confirm_password,
                        "El campo confirm password no está cumpliendo el criterio de aceptación.")

        base_page_user_register.click_login()

    def test_user_registration_validate_fullname(self):
        base_page_user_register = RegisterUserPage(self.driver)

        base_page_user_register.enter_full_name("Jon")
        base_page_user_register.enter_email('test@example.com')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')

        button_disabled = base_page_user_register.sign_up_button_disabled()
        print("El botón de login estau deshabilitado cuando el campo full_name no "
              "tiene un espacio y texto después del espacio.")

        self.assertTrue(button_disabled, "El botón de login debe estar deshabilitado cuando el campo full_name no "
                                         "tiene un espacio y texto después del espacio.")

    def test_user_registration_validate_full_name_special_values(self):
        base_page_user_register = RegisterUserPage(self.driver)

        base_page_user_register.enter_full_name("Ary@ Not Tod@y!")
        base_page_user_register.enter_email('test@example.com')
        base_page_user_register.enter_password_field('Test-2024')
        base_page_user_register.enter_confirm_password_field('Test-2024')

        full_name_value = base_page_user_register.get_full_name_field_value()
        print(full_name_value)
        is_valid_name = base_page_user_register.is_valid_full_name(full_name_value)

        # validar que el nombre no es válido
        self.assertTrue(is_valid_name, "El nombre completo no debería contener números ni caracteres especiales.")

        is_register_button_enabled = base_page_user_register.sign_up_button_enabled()
        self.assertFalse(is_register_button_enabled, "El botón de registro no debería estar habilitado para un nombre "
                                                     "inválido.")
        base_page_user_register.click_login()

    def test_user_registration_password_coincidence(self):
        base_page_user_register = RegisterUserPage(self.driver)
        base_page_user_register.enter_full_name("Jon Snow")
        base_page_user_register.enter_email('test@example.com')

        password = 'Test-2024'
        confirm_password = 'Test-2025'
        base_page_user_register.enter_password_field(password)
        base_page_user_register.enter_confirm_password_field(confirm_password)

        expected_message = "Passwords don't match"

        with self.subTest(msg="Validating password mismatch message"):
            self.assertTrue(base_page_user_register.passwords_match(), "Las contraseñas no coinciden.")

        with self.subTest(msg="Validating some other condition"):
            actual_message = base_page_user_register.get_error_message()
            self.assertEqual(expected_message, actual_message, "El mensaje de error no coincide con el esperado.")

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
