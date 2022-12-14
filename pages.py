from typing import Optional

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from elements import LoginInputFieldElement, PasswdInputFieldElement, \
    DestinationFieldElement, SubjectFieldElement, MessageTextboxElement, WAIT_TIMEOUT
from locators import LoginPageLocators, MainPageLocators


class BasePage(object):
    def __init__(self, driver):
        # Private field
        self._driver = driver

    @property
    def driver(self):
        """ Returns executing driver. Does not contain any setter so the property is read-only.
            It is needed for the page being executable by only driver that was given in constructor"""
        return self._driver

    def is_title_matches(self, title: Optional[str] = None):
        if title is None:
            raise ValueError("Title must be not None")
        return title in self.driver.title


class GMailPage(BasePage):
    def is_title_matches(self):
        """ Method that checks if driver reached Gmail by scanning page title """
        return super().is_title_matches('Gmail')


class GMailLoginPage(GMailPage):
    login_field = LoginInputFieldElement()

    def __init__(self, driver, address: Optional[str] = None):
        """ Initializes parent class and sets address field to a given value
            or, if not given, to a default value """
        super().__init__(driver)
        if address is None:
            self._address = 'http://gmail.com'
        else:
            self._address = address

    @property
    def address(self) -> str:
        """ Returns string containing an address of login page. Read-only property """
        return self._address

    def reach(self):
        """ Method that helps us to reach needed page.
            Returns a subfunction that gets unnecessary driver as argument for WebDriverWait.until calls """
        def _reach(driver=None):
            self.driver.get(self.address)
            return self.is_title_matches()
        return _reach

    def click_next_button(self):
        """ Clicks next button on login input screen """
        self.driver.find_element(*LoginPageLocators.LOGIN_NEXT_BUTTON).click()
        return GMailPasswordPage(self.driver)


class GMailPasswordPage(GMailPage):
    passwd_field = PasswdInputFieldElement()

    def click_next_button(self):
        """ Clicks next button on password input screen """
        self.driver.find_element(*LoginPageLocators.PASSWORD_NEXT_BUTTON).click()
        return GMailMainPage(self.driver)


class GMailMainPage(GMailPage):
    destination_field = DestinationFieldElement()
    subject_field = SubjectFieldElement()
    message_textbox = MessageTextboxElement()

    def click_write_message_button(self):
        """ Clicks on button that open letter writing dialog box """
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            lambda driver: driver.find_element(*MainPageLocators.WRITE_MESSAGE_BUTTON)
        ).click()

    def count_messages(self, subject) -> int:
        """ Finds count of letters with given subject """
        mode, value = MainPageLocators.MESSAGES_TO_COUNT_ELEMENTS
        value = value.format(subject)
        return len(self.driver.find_elements(mode, value))

    def send_message(self) -> None:
        """ Sends message using hotkeys in letter writing dialog box """
        self.message_textbox.send_keys(Keys.CONTROL + Keys.RETURN)

    def check_message_with_content(self, subject: str, expected_content: str) -> bool:
        """ Checks if message with count contains needed number """
        substr_to_skip = ' - \n'
        mode, value = MainPageLocators.MESSAGE_WITH_COUNT_ELEMENT
        elem = WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            lambda driver: driver.find_element(mode, value.format(subject))
        )
        return elem.text[len(substr_to_skip):] == expected_content  # Skipping first 4 symbols as they are " - \n"

    def wait_for_dialog_box(self):
        """ Waits for message writing dialog box to appear """
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located(MainPageLocators.DIALOG_BOX_ELEMENT)
        )

    def wait_for_count_in_sent_message_to_appear(self, subject: str):
        """ Waits for message sent automatically to appear """
        mode, value = MainPageLocators.MESSAGE_WITH_COUNT_ELEMENT
        value = value.format(subject)
        locator = tuple([mode, value])
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.text_to_be_present_in_element(locator, ' - ')
        )

    def wait_for_messages_to_count_to_appear(self, subject: str):
        """ Waits for appearance of messages that need to be counted """
        mode, value = MainPageLocators.MESSAGES_TO_COUNT_ELEMENTS
        value = value.format(subject)
        locator = tuple([mode, value])
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )





