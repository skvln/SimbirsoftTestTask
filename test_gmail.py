from dataclasses import dataclass

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from elements import WAIT_TIMEOUT
from pages import BasePage, GMailLoginPage, GMailPasswordPage, GMailMainPage


@dataclass(frozen=True)
class GridHost(object):
    URL = 'http://localhost:4444'


@dataclass(frozen=True)
class Credentials(object):
    EMAIL = 'simbir.test.task@gmail.com'
    PASSWD = 'simbirtest'


@dataclass(frozen=True)
class MessagesToCountProperties(object):
    SUBJECT = 'Simbirsoft Тестовое задание'
    COUNT = 2


@dataclass(frozen=True)
class MessagesToSendProperties(object):
    SUBJECT = 'Simbirsoft Тестовое задание. Скворцов'
    CONTENT = str(MessagesToCountProperties.COUNT)


def create_screenshot(driver, name):
    """ Function that makes a screenshot of a screen and attaches it into allure report """
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )


@pytest.fixture(scope='session', params=[webdriver.ChromeOptions, webdriver.EdgeOptions])
def login_page(request):
    """ Fixture that helps to reach the Gmail login page """
    driver = webdriver.Remote(command_executor=GridHost.URL, options=request.param())
    login_page = GMailLoginPage(driver)
    WebDriverWait(driver, WAIT_TIMEOUT).until(login_page.reach())
    yield login_page
    driver.quit()


@allure.step("Checking matching title")
def check_matching_title(page: BasePage):
    return page.is_title_matches()


@allure.step("Login input and reaching password page")
def enter_login_and_reach_passwd_page(login_page: GMailLoginPage):
    login_page.login_field = Credentials.EMAIL
    passwd_page = login_page.click_next_button()
    return passwd_page


@allure.step("Password input and reaching gmail main page")
def enter_passwd_and_reach_main_page(passwd_page: GMailPasswordPage):
    passwd_page.passwd_field = Credentials.PASSWD
    return passwd_page.click_next_button()


@allure.step("Count messages with the given subject")
def count_messages_with_subject(page: GMailMainPage, subject):
    page.wait_for_messages_to_count_to_appear(subject)
    return page.count_messages(subject)


@allure.step("Click on write message button and wait for message dialog box to appear")
def click_write_button_and_wait_for_dialog_box(page: GMailMainPage):
    page.click_write_message_button()
    page.wait_for_dialog_box()


@allure.step("Filling the message form and send it")
def fill_message_and_send(page: GMailMainPage, to, subject, content):
    page.destination_field = to
    page.subject_field = subject
    page.message_textbox = content
    page.send_message()


@allure.step("Wait for message to receive and check its content")
def wait_for_message_and_check_content(page: GMailMainPage, subject: str, expected_content: str) -> bool:
    page.wait_for_count_in_sent_message_to_appear(MessagesToSendProperties.SUBJECT)
    return page.check_message_with_content(subject, expected_content)


def test_gmail(login_page):
    driver = login_page.driver
    try:
        assert check_matching_title(login_page)
        passwd_page = enter_login_and_reach_passwd_page(login_page)
        main_page = enter_passwd_and_reach_main_page(passwd_page)
        messages_count = count_messages_with_subject(main_page, MessagesToCountProperties.SUBJECT)
        assert messages_count == MessagesToCountProperties.COUNT
        click_write_button_and_wait_for_dialog_box(main_page)
        fill_message_and_send(main_page, Credentials.EMAIL, MessagesToSendProperties.SUBJECT, messages_count)
        assert wait_for_message_and_check_content(main_page,
                                                  MessagesToSendProperties.SUBJECT, MessagesToSendProperties.CONTENT)
    except Exception as e:
        create_screenshot(driver, "Screen of page where test failed")
        raise e
