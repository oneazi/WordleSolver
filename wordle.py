from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import keyboard     # used to type the words
from numpy.random import choice     # set random initialization

from word_list import word_list

# configure browser window
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--start-maximized')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
browser.implicitly_wait(5)

browser.get('https://www.nytimes.com/games/wordle/index.html')
browser.find_element(by=By.XPATH, value="//body").click()
keyboard.write(choice(word_list), 0.05)
keyboard.press_and_release('enter')
