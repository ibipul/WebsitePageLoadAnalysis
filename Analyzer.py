from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from WebsiteClass import website

class TestDriver:
    """
    This class encapsulates the selenium drivers initialized
    in different configurations of adblocks
    """
    def __init__(self, driver_exec_path, extension_path, adblock):
        self.driver_exec =  driver_exec_path
        self.extension_path = extension_path
        self.adblock = adblock
        self.driver = self.get_test_driver(adblock_on=self.adblock)

    def get_clear_browsing_button(self, driver):
        """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
        return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

    def clear_cache(self, timeout=60):
        """Clear the cookies and cache for the ChromeDriver instance."""
        # navigate to the settings page
        self.driver.get('chrome://settings/clearBrowserData')
        # wait for the button to appear
        wait = WebDriverWait(self.driver, timeout)
        wait.until(self.get_clear_browsing_button)
        # click the button to clear the cache
        self.get_clear_browsing_button(self.driver).click()
        # wait for the button to be gone before returning
        wait.until_not(self.get_clear_browsing_button)

    def get_test_driver(self,adblock_on):
        """
        This functions creates and returns a driver as a class variable
        :param adblock_on:
        :return:
        """
        if adblock_on:
            options = webdriver.ChromeOptions()
            switch = '--load-extension=' + self.extension_path
            options.add_argument(switch)
            driver = webdriver.Chrome(self.driver_exec, chrome_options=options)
            #self.clear_cache(driver)
        else:
            driver = webdriver.Chrome(self.driver_exec)
            #self.clear_cache(driver)

        return driver

class analyze:
    """
    This is the analyzer class.
    Object of this class runs the analysis on the provided set of websites
    - added one line each in a textfile
    - drivers are added for comparison
    (right now drivers cannot be NULL)
    """
    def __init__(self, site_file_path, ab_driver, nab_driver):
        self.site_name_list = self.get_site_list(site_file_path)
        self.driver_ab = ab_driver
        self.driver_nab = nab_driver
        self.website_objs = self.get_site_objs(site_name_list = self.site_name_list)

    def get_site_list(self, site_file_path):
        """
        Reads the site names into a list, from the file provided.
        :param site_file_path:
        :return:
        """
        with open(site_file_path) as f:
            content = f.readlines()
        # List of urls
        return ['http://'+x.strip() for x in content]

    def get_site_objs(self,site_name_list):
        """
        Creates the website objects list
        :param site_name_list:
        :return:
        """
        obj_list = []
        for s in site_name_list:
            obj_list.append(website(s))
        return obj_list

    def get_data(self):
        """
        Interface point of this class.
        Starts the analysis, starts populating the website object with analyzable data
        :return:
        """
        for i in range(0,len(self.website_objs)):
            self.website_objs[i].populate_components(driver_ab=self.driver_ab, driver_nab=self.driver_nab)
