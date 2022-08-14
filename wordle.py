from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from numpy.random import choice  # set random initialization
from time import sleep

from word_list import word_list

# configure browser window
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--start-maximized')
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, options=chrome_options)
browser.implicitly_wait(5)

browser.get('https://www.nytimes.com/games/wordle/index.html')
page = browser.find_element(by=By.XPATH, value="//body")
welcome_x = browser.find_element(by=By.CLASS_NAME, value='Modal-module_closeIcon__b4z74')
welcome_x.click()
page.click()

# get reference to all the rows
game_rows = browser.find_elements(By.CLASS_NAME, 'Row-module_row__dEHfN')

# assign the first guess as one of the optimal words
first_guesses = ['irate', 'adieu']
guess = choice(first_guesses)

# take the 6 guesses
hints = {'correct': set(), 'absent': set(), 'present': set()}
for i in range(0, 6):

    print(guess)

    # how to provide input to the game
    page.send_keys(guess)
    page.send_keys(Keys.ENTER)
    sleep(1.5)

    tiles = game_rows[i].find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")

    # check if the guess was correct
    evals = [tile.get_attribute("data-state") for tile in tiles]
    print(evals)
    if evals == ['correct'] * 5:
        print("Solved Successfully")
        break

    # build the hints to narrow the list
    for j, tile in enumerate(tiles):
        evaluation = tile.get_attribute("data-state")
        if evaluation == 'correct':
            if guess[j] in hints['absent']:
                hints['absent'].remove(guess[j])
            hints['correct'].add((j, guess[j]))
        elif evaluation == 'present':
            hints['present'].add((j, guess[j]))
        elif evaluation == 'absent':
            if (any(tile.text.lower() == hint[1] for hint in hints['correct'])
                    or any(tile.text.lower() == hint[1] for hint in hints['present'])):
                pass
            else:
                hints['absent'].add(guess[j])
    print(f'{hints}\n')

    # narrow the list of possible words
    for word in word_list[:]:
        for each in hints['correct']:
            if word[each[0]] != each[1]:
                word_list.remove(word)
                break
    for word in word_list[:]:
        for each in hints['present']:
            if each[1] not in word or word[each[0]] == each[1]:
                word_list.remove(word)
                break
    for word in word_list[:]:
        for each in hints['absent']:
            if each in word:
                word_list.remove(word)
                break

    # select a word from the remaining list to be used as input
    guess = choice(word_list)
    sleep(1)
