import time
import pytest
import pytest_flask
import pytest_selenium
from flask import url_for
from urllib.request import urlopen
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from ebisu_flashcards.app import app as flask_app
from ebisu_flashcards.database.models import User, Deck



# from https://github.com/pytest-dev/pytest-selenium/issues/135
@pytest.fixture
def firefox_options(request, firefox_options):
    firefox_options.add_argument('--headless')
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

@pytest.fixture
def login(selenium):
    selenium.get('http://localhost:3500/login')
    username_field = selenium.find_element_by_name("username")
    username_field.clear()
    username_field.send_keys("me")
    
    password_field = selenium.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys("rightpassword")

    submit_button = selenium.find_element_by_xpath("//input[@type='submit']")
    submit_button.click()



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

    def test_home_no_decks(self, selenium, app, login):
        user_id = User.objects.get(username="me").id
        assert len(Deck.objects(author=user_id).all()) == 0
        
        selenium.get('http://localhost:3500/home')
        boxes = selenium.find_elements_by_class_name("box")
        for box in boxes:
            assert 'hidden' in box.get_attribute('class').split()

        assert "hidden" not in selenium.find_element_by_id("create-box").get_attribute("class").split()

    def test_home_create_decks(self, selenium, app, login):
        user_id = User.objects.get(username="me").id
        assert len(Deck.objects(author=user_id).all()) == 0

        selenium.get('http://localhost:3500/home')
        new_deck = selenium.find_element_by_id("create-box")
        assert "hidden" not in new_deck.get_attribute("class").split()
        
        new_deck_form = new_deck.find_element_by_tag_name("form")
        assert "hidden" in new_deck_form.get_attribute("class").split()
        
        new_deck.click()

        assert "hidden" not in new_deck_form.get_attribute("class").split()

        title_field = new_deck.find_element_by_name("name")
        title_field.clear()
        title_field.send_keys("title")

        desc_field = new_deck.find_element_by_name("description")
        desc_field.clear()
        desc_field.send_keys("desc")

        alg_field = new_deck.find_element_by_name("algorithm")
        alg_field.select_by_visible_text("Random Order")

        submit_button = new_deck.find_element_by_xpath("//input[text()='Save']")
        submit_button.click()
