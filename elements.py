from locators import LoginPageLocators, MainPageLocators

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

WAIT_TIMEOUT = 100


class BasePageElement(object):
    """ Descriptor class for pages elements """
    locator = None

    def __set__(self, obj, value):
        driver = obj.driver
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda x: x.find_element(*self.locator).is_enabled()
        )
        elem = driver.find_element(*self.locator)
        elem.clear()
        elem.send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        return WebDriverWait(driver, WAIT_TIMEOUT).until(
            lambda x: x.find_element(*self.locator)
        )


class LoginInputFieldElement(BasePageElement):
    locator = LoginPageLocators.LOGIN_INPUT_FIELD


class PasswdInputFieldElement(BasePageElement):
    locator = LoginPageLocators.PASSWORD_INPUT_FIELD


class DestinationFieldElement(BasePageElement):
    locator = MainPageLocators.DESTINATION_FIELD


class SubjectFieldElement(BasePageElement):
    locator = MainPageLocators.SUBJECT_FIELD


class MessageTextboxElement(BasePageElement):
    locator = MainPageLocators.MESSAGE_TEXTBOX
