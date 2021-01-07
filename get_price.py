URL = 'https://www.poeprices.info/dashboard'
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_price(searchterm, headless):
    webpage = r"https://www.poeprices.info/#pricesingleitem"

    options = Options()
    # options.headless = True
    if headless:
        options.add_argument('--headless')

    options.add_argument('window-size=1920x1480')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    driver.get(webpage)

    sbox = driver.find_element_by_name('itemtext')
    sbox.send_keys(searchterm)

    submit = driver.find_element_by_id("submitsingle")
    driver.execute_script("arguments[0].click();", submit)
    driver.switch_to.window(window_name=driver.window_handles[-1])
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form/table[2]/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/p[2]/span')))
        #print(driver.page_source)

        price = str(driver.find_element_by_xpath('/html/body/div/form/table[2]/tbody/tr/td[2]/div[1]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/p[2]/span').text)
        if headless:
            driver.close()

        return price
    except:
        with open('page.html', 'w') as f:
            f.write(driver.page_source)
        driver.close()
        return '999 Chaos'
