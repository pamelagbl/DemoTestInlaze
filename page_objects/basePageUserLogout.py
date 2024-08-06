from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu = (By.CSS_SELECTOR, ".btn.btn-ghost.btn-circle.avatar")
        self.logout_button = (By.CSS_SELECTOR, "ul.menu.menu-sm.dropdown-content > li:last-child")

    def click_logout(self):
        try:
            # Espera a que el botón de logout sea clickeable y luego haz clic
            logout_button_menu = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.menu)
            )
            logout_button_menu.click()

            logout_button_element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.logout_button)
            )
            logout_button_element.click()

        except TimeoutException as e:
            print("Error: TimeoutException - No se pudo encontrar el botón de logout en el tiempo esperado.")
            # Puedes manejar la excepción aquí, como tomar capturas de pantalla o registrar información adicional
        except Exception as e:
            print(f"Error: {str(e)}")
            # Manejo de otras excepciones, si es necesario
