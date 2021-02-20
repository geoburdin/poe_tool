URL = 'https://www.poeprices.info/dashboard'
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_price(search_for, headless):
    webpage = r"https://www.poeprices.info/#pricesingleitem"

    options = Options()
    # options.headless = True
    if headless:
        options.add_argument('--headless')

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")

    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    capabilities = {
        'browserName': 'chrome',
        'chromeOptions': {
            'useAutomationExtension': False,
            'forceDevToolsScreenshot': True,
            'args': ['--start-maximized', '--disable-infobars']
        }
    }
    driver = webdriver.Chrome(executable_path="geckodriver.exe", options=options, desired_capabilities=capabilities)

    driver.get(webpage)

    sbox = driver.find_element_by_name('itemtext')
    sbox.send_keys(search_for)

    submit = driver.find_element_by_id("submitsingle")
    driver.execute_script("arguments[0].click();", submit)
    driver.switch_to.window(window_name=driver.window_handles[-1])
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,
                                                                        '/html/body/div/form/table[2]/tbody/tr/td['
                                                                        '2]/div[1]/table/tbody/tr/td['
                                                                        '1]/table/tbody/tr[2]/td/p[2]/span')))
        # print(driver.page_source)

        price = str(driver.find_element_by_xpath(
            '/html/body/div/form/table[2]/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/p[2]/span').text)
        if headless:
            driver.quit()

        return price
    except:
        with open('page.html', 'w') as f:
            f.write(driver.page_source)
        driver.quit()
        return '9999 Chaos'
