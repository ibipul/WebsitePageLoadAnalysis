from time import time,sleep
class website:
    """
    This class encapsulates the analyzable data for each website
    component_normal: holds the performance metric from when no adblock is there
    component_wtblock: holds the performance metric when adblock is enabled
    """
    def __init__(self,url):
        self.name = url
        self.components_normal =[]
        self.components_wtblock = []

    def component_normal_update(self,elements):
        '''
        updates the components_normal
        :param elements:
        :return:
        '''
        self.components_normal = elements

    def component_wtblock_update(self,elements):
        '''
        updates the components_wtblock
        :param elements:
        :return:
        '''
        self.components_wtblock = elements

    def populate_components(self,driver_ab, driver_nab):
        '''
        Interface function that is called with selenium drivers
        to generate the data for each website (serially)
        :param driver_ab:
        :param driver_nab:
        :return:
        '''
        self.populate_components_wtblock(driver_ab)
        self.populate_components_normal(driver_nab)

    def populate_components_wtblock(self, driver_ab):
        '''
        The selenium logic to update the class with performance variables
        for components with adblock switched on
        :param driver_ab:
        :return:
        '''
        driver_ab.driver.get(self.name)
        sleep(40)
        timing_ab = driver_ab.driver.execute_script("return window.performance.getEntries();")
        self.component_wtblock_update(elements=timing_ab)

    def populate_components_normal(self, driver_nab):
        '''
        The selenium logic to update the class with performance variables
        for normal components
        :param driver_nab:
        :return:
        '''
        driver_nab.driver.get(self.name)
        sleep(40)
        timing_nab = driver_nab.driver.execute_script("return window.performance.getEntries();")
        self.component_normal_update(elements=timing_nab)

