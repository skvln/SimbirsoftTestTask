from dataclasses import dataclass

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from elements import WAIT_TIMEOUT
from pages import GMailLoginPage


@dataclass(frozen=True)
class GridHost(object):
    URL = 'http://localhost:4444'


@dataclass(frozen=True)
class Credentials(object):
    EMAIL = 'simbir.test.task@gmail.com'
    PASSWD = 'simbirtest'


@dataclass(frozen=True)
class LetterData(object):
    SUBJECT = 'Simbirsoft Тестовое задание. Скворцов'


def create_screenshot(page, name):
    """ Function that makes a screenshot of a screen and attaches it into allure report """
    allure.attach(
        page.driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


@pytest.fixture(scope='session', params=[webdriver.ChromeOptions, webdriver.EdgeOptions])
def login_page(request):
    """ Fixture that helps to reach the Gmail login page """
    driver = webdriver.Remote(command_executor=GridHost.URL, options=request.param())
    login_page = GMailLoginPage(driver)
    WebDriverWait(driver, WAIT_TIMEOUT).until(login_page.reach)
    create_screenshot(login_page, "Reached login page")
    yield login_page
    driver.quit()


def test_title(login_page):
    """ Test that finds out if title is right """
    assert login_page.is_title_matches()


@pytest.fixture(scope='session')
def login_input(login_page):
    """ Fixture that inputs email into login field on login page """
    login_page.login_field = Credentials.EMAIL
    create_screenshot(login_page, "Page after email input")
    passwd_page = login_page.click_next_button()
    return passwd_page


@pytest.fixture(scope='session')
def password_input(login_input):
    """ Fixture that inputs password into password field on login page """
    create_screenshot(login_input, "Password page")
    login_input.passwd_field = Credentials.PASSWD
    create_screenshot(login_input, "Password page after password input")
    main_page = login_input.click_next_button()
    create_screenshot(main_page, "Mail main page")
    return main_page


@pytest.fixture(scope='session')
def main_page(password_input):
    """ Fixture that gets a main page from password input fixture and then gives it away """
    main_page = password_input
    return main_page


@pytest.fixture(scope='session')
def messages_count(main_page):
    """ Fixture that counts messages with needed subject and returns the number of them """
    main_page.wait_for_messages_to_count_to_appear()
    return main_page.count_messages()


def test_messages_count(messages_count):
    """ Test that checks if count executed automatically is equal to real count """
    assert messages_count == 2


@pytest.fixture(scope='session')
def send_message(main_page, messages_count):
    """ Fixture that sends a message with count to the same email """
    main_page.click_write_message_button()
    main_page.wait_for_dialog_box()
    create_screenshot(main_page, "Page after pressing the 'Write message' button")
    main_page.destination_field = Credentials.EMAIL
    main_page.subject_field = LetterData.SUBJECT
    main_page.message_textbox = messages_count
    create_screenshot(main_page, "Page after filling field in a message form")
    main_page.send_message()
    main_page.wait_for_count_in_sent_message_to_appear()
    create_screenshot(main_page, "Page after sending a message")


def test_message_sent(main_page, send_message, messages_count):
    """ Test that checks if a count in received message is correct """
    assert main_page.check_message_with_count(messages_count)
