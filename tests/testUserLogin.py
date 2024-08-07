import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from page_objects.basePageUserLogin import LoginPage
from page_objects.basePageUserLogout import LogoutPage
import unittest


class TestLogin(unittest.TestCase):
    def setUp(self):
        # Configura el servicio del driver usando webdriver_manager
        service = Service(ChromeDriverManager().install())
        # Inicializa el driver con el servicio configurado
        self.driver = webdriver.Chrome(service=service)
        # Abre la página que deseas probar
        self.driver.get('https://test-qa.inlaze.com/auth/sign-in')
        self.driver.maximize_window()  # Maximiza la ventana del navegador

    def test_login(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('pamela.gbrito7@gmail.com')
        base_page_user_login.enter_password('Test2024')
        base_page_user_login.click_login()
        expected_name = "pamela brito"

        # Verificamos que el usuario fue redirigido a la página Panel

        WebDriverWait(self.driver, 10).until(
            EC.url_contains('https://test-qa.inlaze.com/panel')
        )

        self.assertIn('https://test-qa.inlaze.com/panel', self.driver.current_url)
        print(f"Se ha redirigido con éxito al usuario a la página correspondiente")

        user_name = base_page_user_login.get_user_login()
        print(f"El nombre de usuario obtenido es: {user_name}")
        self.assertEqual(user_name, expected_name, f"Se espera que el nombre de usuario sea: {expected_name} pero se "
                                                   f"recibió: {user_name}")

    def test_login_logout(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('pamela.gbrito7@gmail.com')
        base_page_user_login.enter_password('Test2024')
        base_page_user_login.click_login()

        WebDriverWait(self.driver, 10).until(
            EC.url_contains('https://test-qa.inlaze.com/panel')
        )
        self.assertIn('https://test-qa.inlaze.com/panel', self.driver.current_url)

        base_page_user_logout = LogoutPage(self.driver)
        base_page_user_logout.click_logout()
        # Se verifica que el usuario fue redirigido a la página sign-in
        WebDriverWait(self.driver, 10).until(
            EC.url_contains('https://test-qa.inlaze.com/auth/sign-in')
        )
        self.assertIn('https://test-qa.inlaze.com/auth/sign-in', self.driver.current_url)

    def test_mandatory_fields_empty(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('')
        base_page_user_login.enter_password('')
        #base_page_user_login.click_login()

        button_disabled = base_page_user_login.login_button_disabled()
        print(f"El botón de inicio de sesión tiene el elemento disabled: {button_disabled}")
        self.assertTrue(button_disabled, "El botón de inicio de sesión debería estar "
                                         "deshabilitado cuando los campos están vacíos.")

    def test_incorrect_password(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('pamela.gbrito7@gmail.com')
        base_page_user_login.enter_password('Hola2024')
        base_page_user_login.click_login()
        message = base_page_user_login.invalid_password()
        print(f"El mensaje esperado es: {message}")

        self.assertIn("Password doesn't match", message)

    def test_incorrect_email(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('testexample@gmail.com')
        base_page_user_login.enter_password('Test2024')
        base_page_user_login.click_login()
        message = base_page_user_login.invalid_email()
        print(f"El mensaje esperado es: {message}")

        self.assertIn("User not found", message)

    def test_validate_password_less_than_eigth_characters(self):
        base_page_user_login = LoginPage(self.driver)
        base_page_user_login.enter_email('pamela.gbrito7@gmail.com')
        base_page_user_login.enter_password('Test')

        button_password = base_page_user_login.login_button_disabled()
        print(f"El botón de inicio de sesión tiene el elemento disabled: {button_password}")
        self.assertTrue(button_password, "El botón de inicio de sesión debería estar "
                                         "deshabilitado cuando el campo contraseña tiene "
                                         "menos de 5 caracteres.")
        print("No se puede iniciar sesión ya que el campo password tiene menos de 5 caracteres")

        #el campo password puede tener 4 caracteres si se incluye mayus y numero, pero da mensaje de error cuando se intenta iniciar sesión

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
