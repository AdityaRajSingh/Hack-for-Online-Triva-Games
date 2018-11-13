import pytesseract
import pyscreenshot as ImageGrab
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def replacements():
    global toSearch
    normal_replaces = {'The ', 'Who ', 'What ', 'Which ', 'Whom ', 'of ', 'these '}
    plus_replaces = {' following ', ' is ', ' these ', ' an ', ' a ', ' the ', ' which ', ' not ', ' what ', ' who '}

    for rep in normal_replaces:
        toSearch = toSearch.replace(rep, '')
    toSearch = toSearch.lower()

    for rep in plus_replaces:
        toSearch = toSearch.replace(rep, '+')

    toSearch = toSearch.replace('?', '').replace('\'', '').replace('\n', '+').replace(' ', '+').replace(',', '').replace('_', '')
    print("\n" + toSearch + "\n")


def printer(a, results):
    print(a + "\n")
    counter_imp = [0] * 3
    counter = [0] * 3
    for result in results:
        result = result.getText().lower()
        length = len(options)
        for i in range(0, length):
            counter_imp[i] = counter_imp[i] + result.count(options[i])
            words = options[i].replace('the ', '').strip().split(' ')
            for word in words:
                counter[i] = counter[i] + result.count(word.strip())

    for i in range(0, 3):
        print(str(counter_imp[i]), end="  ")

    print()
    for i in range(0, 3):
        print(str(counter[i]), end="  ")
    print("\n")


def bing(url, class_div, driver):
    global count
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    bing_results = soup.findAll("div", {"class": class_div})
    printer("Bing", bing_results)


def google(url, class_div, driver):
    global count
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    google_results = soup.findAll("div", {"class": class_div})
    printer("Google", google_results)


start_time = time.time()

HQ1 = (135, 315, 400, 435)
HQ2 = (155, 450, 370, 592)

im1 = ImageGrab.grab(HQ1)
toSearch = pytesseract.image_to_string(im1, lang='eng')

im1 = ImageGrab.grab(HQ2)
options = pytesseract.image_to_string(im1, lang='eng')

options = options.lower()
replacements()

options = options.split("\n")
options = list(filter(None, options))

print(options)
print("\n")

count = 0

URL1 = "http://www.bing.com/search?q=" + toSearch
CLASS1 = "b_caption"

URL2 = "http://www.google.co.in/search?q=" + toSearch
CLASS2 = "rc"

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("headless")
driver = webdriver.Chrome(chrome_options=chromeOptions)

bing(URL1, CLASS1, driver)
google(URL2, CLASS2, driver)

driver.close()
driver.quit()

print("--- %s seconds ---" % (time.time() - start_time))