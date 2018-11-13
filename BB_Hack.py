import pytesseract
import pyscreenshot as ImageGrab
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import threading

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
    print(a, end = "")
    counter_imp = [0] * 3
    counter = [0] * 3
    for result in results:
        result = result.getText().lower()
        for i in range(0, len(options)):
            counter_imp[i] = counter_imp[i] + result.count(options[i])
            words = options[i].replace('the ', '').strip().split(' ')
            for word in words:
                counter[i] = counter[i] + result.count(word.strip())
    start = "\033[1m"
    end = "\033[0;0m"

    print(start)
    for i in range(0, 3):
        print(str(counter_imp[i]), end="  ")
    print(end)
    for i in range(0, 3):
        print(str(counter[i]), end="  ")
    print("\n")


def bing(url, class_div, driver):
    global count
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("ERROR")
        if (time.time() - start_time) >= 10 or count > 10:
            print("Timeout " + str(count))
            count = count + 1
            return
        else:
            count = count + 1
        bing(url, class_div, driver)

    bing_results = soup.findAll("div", {"class": class_div})
    
    try:
        printer("Bing", bing_results)
    except Exception as e:
        driver.close()
        driver.quit()


def google(url, class_div, driver):
    global count
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("ERROR")
        if (time.time() - start_time) >= 10 or count > 10:
            print("Timeout " + str(count))
            count = count + 1
            return
        else:
            count = count + 1
        google(url, class_div, driver)

    google_results = soup.findAll("div", {"class": class_div})
    printer("Google", google_results)

start_time = time.time()

BB = (130, 348, 405, 590)
#BB = (130, 388, 405, 620)

im1 = ImageGrab.grab(BB)

options = pytesseract.image_to_string(im1, lang='eng')

options = options.strip()
if options.find('?') == -1:
    options = options.split('.', 1)
else:
    options = options.split('?', 1)

toSearch = options[0]
options[1] = options[1].lower()
count = 0

replacements()

options[1] = options[1].lower()
options = options[1].split("\n\n")

count = 0

options.pop(0)
URL1 = "http://www.bing.com/search?q=" + toSearch
CLASS1 = "b_caption"

URL2 = "http://www.google.co.in/search?q=" + toSearch
CLASS2 = "rc"

print(options)

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("headless")
driver = webdriver.Chrome(chrome_options=chromeOptions)

#thread1 = threading.Thread(target=bing(URL1, CLASS1, driver), args=())
#thread2 = threading.Thread(target=google(URL2, CLASS2, driver), args=())

bing (URL1, CLASS1, driver)
google (URL2, CLASS2, driver)

driver.close()
driver.quit()
"""
thread1.start()
thread2.start()

thread1.join()
thread2.join()
"""

print("--- %s seconds ---" % (time.time() - start_time))