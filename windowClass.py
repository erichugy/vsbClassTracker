from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller
from selenium.common import exceptions


chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path


"""
Usefull driver commands:
driver.get("url")
driver.back()
driver.forward()
driver.refresh()
"""


class Window(webdriver.Chrome):
    def __init__(self, page_url, bypass_wait = False, detach = True, maximize_window = True) -> None:

        #to exclude weird bug
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('detach', detach)

        super().__init__(options=options)
        self.get(page_url)

        if maximize_window:
            self.maximize_window()

        #implicit wait to let page load
        if not bypass_wait:
            self.implicitly_wait(0.5)
        

    def __str__(self):
        return(f'Page Title: {self.title};\nCurrent Url: {self.current_url}')

    def close_page(self):
        self.quit()

    def click_button_xpath(self,button_xpath):
        button = self.find_element(By.XPATH, button_xpath)
        button.click()
        self.implicitly_wait(0.5)

    def click_button_id(self,id_name):
        button = self.find_element(By.ID, id_name)
        button.click()
        self.implicitly_wait(0.5)

    def click_button_class(self,class_id): # need to find each lvl to use this so fuck that
        assert type(class_id) == str, "Class ID needs to be a string"
        button = self.find_element(By.CLASS_NAME, class_id)
        button.click()
        self.implicitly_wait(0.5)

    def fill_out_id(self, id_name:str, value):
        """
        Fills out an input box on the page that you found by id tag
        """
        self.find_element(By.ID, id_name).send_keys(value + Keys.ENTER)
        self.implicitly_wait(0.5)

   

# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.get("https://vsb.mcgill.ca/vsb/welcome.jsp")
#     driver.find_element(By.ID, id_name).send_keys(value + Keys.ENTER)