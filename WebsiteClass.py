from time import time,sleep
class website:
    def __init__(self,url):
        self.name = url
        self.components_normal =[]
        self.components_wtblock = []

    def component_normal_update(self,elements):
        self.components_normal = elements

    def component_wtblock_update(self,elements):
        self.components_wtblock = elements

    def populate_components(self, driver_ab, driver_nab):
        driver_ab.driver.get(self.name)
        sleep(5)
        timing_ab = driver_ab.driver.execute_script("return window.performance.getEntries();")
        self.component_wtblock_update(elements=timing_ab)

        driver_nab.driver.get(self.name)
        sleep(5)
        timing_nab = driver_nab.driver.execute_script("return window.performance.getEntries();")
        self.component_normal_update(elements=timing_nab)

