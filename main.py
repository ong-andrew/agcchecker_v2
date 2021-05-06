from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

PATH = "/home/island/Downloads/chromedriver"
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
# chrome_options.add_argument('--disable-dev-shm-usage')
page = webdriver.Chrome(PATH,chrome_options=options)
page.get('https://lom.agc.gov.my/subsid.php?type=pua')
time.sleep(10)
print(page.page_source)

