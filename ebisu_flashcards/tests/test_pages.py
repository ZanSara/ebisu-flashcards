import time
import pytest
import pytest_flask
import pytest_selenium
from ebisu_flashcards.app import app as flask_app


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
    return flask_app

# from https://pytest-flask.readthedocs.io/en/latest/features.html#start-live-server-start-live-server-automatically-default
@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_homepage(self, selenium, app):
        selenium.get('http://localhost:3500/')
        h1 = selenium.find_element_by_tag_name('h1')
        assert False