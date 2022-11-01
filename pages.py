from elements import LoginInputFieldElement, PasswdInputFieldElement, \
    DestinationFieldElement, SubjectFieldElement, MessageTextboxElement
from locators import LoginPageLocators, MainPageLocators

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, driver):
        # Private field
        self._driver = driver

    @property
    def driver(self):
        """ Returns executing driver. Does not contain any setter so the property is read-only.
         It is needed for the page being executable by only driver that was given in constructor"""
        return self._driver


class GMailPage(BasePage):
    def is_title_matches(self):
        """ Method that checks if driver reached Gmail by scanning page title """
        return 'Gmail' in self.driver.title


class GMailLoginPage(GMailPage):
    login_field = LoginInputFieldElement()

    def reach(self, *args):
        """ Method that helps us to reach needed page """
        self.driver.get('http://gmail.com')
        return self.is_title_matches()

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
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*MainPageLocators.WRITE_MESSAGE_BUTTON)
        ).click()

    def count_messages(self) -> int:
        """ Finds count of letters with given subject """
        return len(self.driver.find_elements(*MainPageLocators.MESSAGES_TO_COUNT_ELEMENTS))

    def send_message(self) -> None:
        """ Sends message using hotkeys in letter writing dialog box """
        self.message_textbox.send_keys(Keys.CONTROL + Keys.RETURN)

    def check_message_with_count(self, count: int) -> bool:
        """ Checks if message with count contains needed number """
        return WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*MainPageLocators.MESSAGE_WITH_COUNT_ELEMENT)
        ).text[4:] == str(count)  # Skipping first 4 symbols as they are " - \n"

    def wait_for_dialog_box(self):
        """ Waits for message writing dialog box to appear """
        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(MainPageLocators.DIALOG_BOX_ELEMENT)
        )

    def wait_for_count_in_sent_message_to_appear(self):
        """ Waits for message sent automatically to appear """
        WebDriverWait(self.driver, 100).until(
            EC.text_to_be_present_in_element(MainPageLocators.MESSAGE_WITH_COUNT_ELEMENT, ' - ')
        )

    def wait_for_messages_to_count_to_appear(self):
        """ Waits for appearance of messages that need to be counted """
        WebDriverWait(self.driver, 100).until(
            EC.presence_of_element_located(MainPageLocators.MESSAGES_TO_COUNT_ELEMENTS)
        )




