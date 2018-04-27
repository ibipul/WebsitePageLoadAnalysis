from Analyzer import TestDriver
from Analyzer import analyze
ab = TestDriver(driver_exec_path = 'C:\\Users\\ibipul\\chromedriver.exe',
                extension_path='C:\\Users\\ibipul\\codes\\cse534\\extension_3_28_0_0.crx',
                adblock=True)
nab = TestDriver(driver_exec_path = 'C:\\Users\\ibipul\\chromedriver.exe',
                 extension_path='C:\\Users\\ibipul\\codes\\cse534\\extension_3_28_0_0.crx',
                 adblock=False)
x = analyze(site_file_path='C:\\Users\\ibipul\\codes\\cse534\\test_list.txt',ab_driver=ab,nab_driver=nab)
x.get_data()
