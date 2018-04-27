from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from WebsiteClass import website

class TestDriver:
    def __init__(self, driver_exec_path, extension_path, adblock):
        self.driver_exec =  driver_exec_path
        self.extension_path = extension_path
        self.adblock = adblock
        self.driver = self.get_test_driver(adblock_on=self.adblock)

    def get_test_driver(self,adblock_on):
        if adblock_on:
            options = webdriver.ChromeOptions()
            switch = '--load-extension=' + self.extension_path
            options.add_argument(switch)
            driver = webdriver.Chrome(self.driver_exec, chrome_options=options)
        else:
            driver = webdriver.Chrome(self.driver_exec)

        return driver

class analyze:

    def __init__(self, site_file_path, ab_driver, nab_driver):
        self.site_name_list = self.get_site_list(site_file_path)
        self.driver_ab = ab_driver
        self.driver_nab = nab_driver
        self.website_objs = self.get_site_objs(site_name_list = self.site_name_list)

    def get_site_list(self, site_file_path):
        with open(site_file_path) as f:
            content = f.readlines()
        # List of urls
        return ['http://'+x.strip() for x in content]

    def get_site_objs(self,site_name_list):
        obj_list = []
        for s in site_name_list:
            obj_list.append(website(s))
        return obj_list

    def get_data(self):
        for i in range(0,len(self.website_objs)):
            self.website_objs[i].populate_components(driver_ab=self.driver_ab, driver_nab=self.driver_nab)






