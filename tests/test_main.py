from urllib import response
from flask_testing import TestCase
from flask import current_app, url_for  # la app que ejecutamos

from main import app


# se crea una clase que extiende TestCase
class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLE'] = False  # Para no hacer los WTF
        app.config['DEBUG'] = False

        return app

    def testAppExists(self):  # app existe
        self.assertIsNotNone(current_app)

    def testAppInTestMode(self):
        self.assertTrue(current_app.config['TESTING'])

    def testIndexRedirect(self):
        response = self.client.get(url_for('index'))

        # Compara si la redireccion es igual al response
        self.assertRedirects(response, url_for('auth.login'))

    def test_hello_post(self):
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    def test_auth_blueprints_exists(self):  # Si existe blueprint
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        # Llamamos a login desde auth
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_template(self):
        # verificamos si trae el template de login
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fakeForm ={
            'username': 'fake',
            'password': 'pass'
        }
        response= self.client.post(url_for('auth.login'), data = fakeForm)

        self.assertRedirects(response, url_for('index'))