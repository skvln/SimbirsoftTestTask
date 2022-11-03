from dataclasses import dataclass

from selenium.webdriver.common.by import By


@dataclass(frozen=True)
class LoginPageLocators(object):
    """ Locators for login page """
    LOGIN_INPUT_FIELD = (By.NAME, 'identifier')
    LOGIN_NEXT_BUTTON = (By.XPATH, './/div[@id="identifierNext"]//button')
    PASSWORD_INPUT_FIELD = (By.NAME, 'Passwd')
    PASSWORD_NEXT_BUTTON = (By.XPATH, r'.//div[@id="passwordNext"]//button')


@dataclass(frozen=True)
class MainPageLocators(object):
    """ Locators for main page """
    WRITE_MESSAGE_BUTTON = (By.XPATH, r'.//div[@role="navigation"]'
                                      r'//div[@role="button" and not (@data-tooltip)]')
    DESTINATION_FIELD = (By.XPATH, r'.//*[@name="to"]//input')
    SUBJECT_FIELD = (By.XPATH, r'.//*[contains(@name, "subject")]')
    MESSAGE_TEXTBOX = (By.XPATH, r'.//table//div[@role="textbox"]')
    MESSAGES_TO_COUNT_ELEMENTS = (By.XPATH, r'.//div[@class="UI"]//table//div[@role="link"]'
                                            r'//span[text()="{}"]')
    MESSAGE_WITH_COUNT_ELEMENT = (By.XPATH, r'.//div[@role="link"]'
                                            r'//*[contains(text(), "{}")]'
                                            r'/../../../span')
    DIALOG_BOX_ELEMENT = (By.XPATH, r'.//div[@role="dialog"]')
