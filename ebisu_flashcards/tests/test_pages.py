import time
import pytest
import pytest_flask
import pytest_selenium
from flask import url_for
from urllib.request import urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ebisu_flashcards.app import app as flask_app
from ebisu_flashcards.database.models import User



# from https://github.com/pytest-dev/pytest-selenium/issues/135
@pytest.fixture
def firefox_options(request, firefox_options):
    # firefox_options.add_argument('--headless')
    return firefox_options

@pytest.fixture
def selenium(selenium):
    flask_app.config.from_object('ebisu_flashcards.config.TestingConfig')
    return selenium

# from https://pytest-flask.readthedocs.io/en/latest/tutorial.html#step-2-configure
@pytest.fixture(scope="session", autouse=True)
def app():
    User.drop_collection()

    new_user = User(username="me", email="me@me.me", password="rightpassword")
    new_user.hash_password()
    new_user.save()

    yield flask_app

    User.drop_collection()

@pytest.fixture(scope="function")
def authenticate(monkeypatch):
  """Monkeypatch the JWT verification functions"""
  monkeypatch.setattr("flask_jwt_extended.verify_jwt_in_request", lambda: print("Verify"))


# from https://pytest-flask.readthedocs.io/en/latest/features.html#start-live-server-start-live-server-automatically-default
@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_frontpage(self, selenium, app):
        selenium.get('http://localhost:3500/')
        login = selenium.find_element_by_xpath('//a[text()="Login"]')
        assert login is not None
        signup = selenium.find_element_by_xpath('//a[text()="Signup"]')
        assert signup is not None

    def test_login_appearance(self, selenium, app):
        selenium.get('http://localhost:3500/login')
        username_field = selenium.find_element_by_name("username")
        assert username_field is not None
        password_field = selenium.find_element_by_name("password")
        assert password_field is not None
        submit_button = selenium.find_element_by_xpath("//input[@type='submit']")
        assert submit_button is not None
        register_link = selenium.find_element_by_xpath('//a[@href="/register"]')
        assert register_link is not None
        reset_link = selenium.find_element_by_xpath('//a[@href="/reset-password"]')
        assert reset_link is not None

    def test_login_form_allows_correct_logins(self, selenium, app):
        assert len(User.objects.all()) == 1

        selenium.get('http://localhost:3500/login')
        username_field = selenium.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys("me")
        
        password_field = selenium.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys("rightpassword")

        submit_button = selenium.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        assert selenium.current_url == "http://localhost:3500/home"

    def test_login_form_not_allow_wrong_login(self, selenium, app):
        assert len(User.objects.all()) == 1

        selenium.get('http://localhost:3500/login')
        username_field = selenium.find_element_by_name("username")
        username_field.clear()
        username_field.send_keys("me")
        
        password_field = selenium.find_element_by_name("password")
        password_field.clear()
        password_field.send_keys("wrongpassword")

        submit_button = selenium.find_element_by_xpath("//input[@type='submit']")
        submit_button.click()

        assert selenium.current_url == "http://localhost:3500/login"

        feedback = selenium.find_element_by_class_name("feedback-negative")
        assert feedback.is_displayed()

