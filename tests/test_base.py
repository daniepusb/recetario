from flask_testing import TestCase
from flask import current_app, url_for

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app


    #1 probar que existe la app
    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    #2 probar que estamos en modo TESTING
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    #3 probar que el index nos redirige a login
    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('auth.login'))

    #4 probar que recipes con GET nos responde un 200
    def test_recipes_get(self):
        response = self.client.get(url_for('recipes'))
        self.assert200(response)

    #5 probar que recipes no tiene metodo POST
    def test_recipes_post(self):
        response = self.client.post(url_for('recipes'))
        self.assert405(response)
        #self.assertTrue(response.status_code, 405)
        #sirve cualquiera de los self
"""
    #6 probar que luego de un post 
    def test_login_post(self):
        response = self.client.post(url_for('auth.login'))
        self.assert405(response)
        #self.assertTrue(response.status_code, 405)


    #7
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    #8
    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')

    #7
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    #8


    #9
    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))
"""