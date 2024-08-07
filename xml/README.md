# Demo TEST INLAZE

Evaluación técnica de los elementos pertenecientes de la página Inlaze (https://test-qa.inlaze.com/auth/)
## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Ejemplos de Casos de Uso](#uso)
- [Instalación](#instalación)
- [Requisitos](#requisitos)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Descripción

Evaluar los conocimientos y pericia del analista de calidad de software sobre la automatización de pruebas en la página de prueba: https://test-qa.inlaze.com/auth/.
## Características

- Diseño de Casos de Prueba
- Implementación de los casos de prueba automatizados
- Pruebas para funcionalidades de elementos text field, forms.

## Ejemplos de Casos de Uso
- Para verificar el ingreso de los campos textField válidos.
- Para comprobar el comportamiento de los radioButton

## Instalación

Instrucciones para configurar el proyecto en un entorno local.

### Requisitos

- IDE IntelliJ IDEA
- Python 3.x
- Selenium
- WebDriver para el navegador que estés utilizando (ChromeDriver, GeckoDriver, etc.)
- Un navegador web compatible (por ejemplo, Google Chrome)

### Pasos para la Instalación

```bash
# Clona el repositorio
git clone https://github.com/pamelagbl/DemoTestInlaze

# Navega al directorio del proyecto
cd DemoTestInlaze

#Instalar dependencias
pip install -r requirements.txt

# Crea un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activa
```
# Configuración
Asegúrate de tener el WebDriver para el navegador que planeas usar. Por ejemplo, para Chrome:

Descarga ChromeDriver y coloca el ejecutable en tu PATH, o en el mismo directorio del proyecto.

# Ejecución de las Pruebas

```bash
python -m unittest discover -s tests
```

# Estructura del Proyecto
```bash
nombre-del-repositorio/
├TestInlazepy
├── drivers
├── page_objects/
│   ├── basePageUserLogin.py
│   ├── basePageUserLogout.py
│   └── basePageUserRegister.py
├── tests/
│   ├── testUserLogin.py
│   ├── testUserRegister.py
├── xml/
│   ├── README.md
└──
```
- tests/: Contiene los archivos de prueba.
- pages_objects/: Contiene las clases de página para la estructura Page Object Model (POM).

# Ejemplo de Uso
Un ejemplo de prueba para registrar un usuario se puede encontrar en testUserRegister.py:
```
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
                                                   
        def tearDown(self):
        time.sleep(5)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
```
# Contribuir
Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

- Haz un fork del repositorio.
- Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
- Realiza tus cambios y commitea (git commit -am 'Añadir nueva funcionalidad').
- Sube tus cambios (git push origin feature/nueva-funcionalidad).
- Abre un Pull Request

# Licencia
Asegúrate de que las secciones que no deseas que se visualicen como bloques de código no estén encerradas entre ```bash o ```sh. Solo usa esos delimitadores para las secciones específicas que deseas resaltar como código. Las demás secciones deben estar en texto regular fuera de esos delimitadores.
