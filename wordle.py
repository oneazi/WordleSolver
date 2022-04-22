from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import keyboard  # used to type the words
from numpy.random import choice  # set random initialization
from time import sleep

from word_list import word_list

# configure browser window
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--start-maximized')
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
browser.implicitly_wait(5)

browser.get('https://www.nytimes.com/games/wordle/index.html')
browser.find_element(by=By.XPATH, value="//body").click()

# get reference to all the rows
game_app = browser.find_element(By.TAG_NAME, 'game-app')
board = browser.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app)
game_rows = board.find_elements(By.TAG_NAME, 'game-row')

# assign the first guess as one of the optimal words
first_guesses = ['irate', 'adieu']
guess = choice(first_guesses)

# take the 6 guesses
hints = {'correct': set(), 'wrong': set(), 'included': set()}
for i in range(0, 6):

    print(guess)

    # how to provide input to the game
    keyboard.write(guess, 0.05)
    keyboard.press_and_release('enter')

    row = browser.execute_script('return arguments[0].shadowRoot', game_rows[i])
    tiles = row.find_elements(By.CSS_SELECTOR, "game-tile")

    # check if the guess was correct
    evals = [tile.get_attribute("evaluation") for tile in tiles]
    print(evals)
    if evals == ['correct'] * 5:
        print("Solved Successfully")
        break

    # build the hints to narrow the list
    for j, tile in enumerate(tiles):
        evaluation = tile.get_attribute("evaluation")
        if evaluation == 'correct':
            hints['correct'].add((j, guess[j]))
        elif evaluation == 'present':
            hints['included'].add((j, guess[j]))
        # FIXME: If the letter is present in the word twice and the first instance is grey
        #   while the second instance is Green, the Grey should not be added to 'wrong'.
        #   Either check the remaining letters of the word in advance OR
        #   Check the 'wrong' list when adding to 'correct' and delete from 'wrong'
        elif evaluation == 'absent':
            if (any(tile.text.lower() == hint[1] for hint in hints['correct'])
                    or any(tile.text.lower() == hint[1] for hint in hints['included'])):
                pass
            else:
                hints['wrong'].add(guess[j])
    print(f'{hints}\n')

    # narrow the list of possible words
    for word in word_list[:]:
        for each in hints['correct']:
            if word[each[0]] != each[1]:
                word_list.remove(word)
                break
    for word in word_list[:]:
        for each in hints['included']:
            if each[1] not in word or word[each[0]] == each[1]:
                word_list.remove(word)
                break
    for word in word_list[:]:
        for each in hints['wrong']:
            if each in word:
                word_list.remove(word)
                break

    # select a word from the remaining list to be used as input
    guess = choice(word_list)
    sleep(2)
