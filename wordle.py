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

# how to provide input to the game
keyboard.write(choice(word_list), 0.05)
keyboard.press_and_release('enter')

# get each row after it is evaluated
game_app = browser.find_element(By.TAG_NAME, 'game-app')
board = browser.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app)
game_rows = board.find_elements(By.TAG_NAME, 'game-row')
game_row = game_rows[0]

# execute this after each consecutive new guess
row = browser.execute_script('return arguments[0].shadowRoot', game_row)
tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")
for tile in tiles:
    print(tile.get_attribute("evaluation"))
print(game_rows)

