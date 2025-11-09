# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import random

from rich.console import Console

from rich.panel import Panel

from time import sleep

console = Console()


def compare_words(guess: list, answer: list):
    """ Return alphabetised list of letters that are in guess and answer """
    guess = sorted(guess)
    answer = sorted(answer)
    index = 0
    correct_letters = []
    for letter in guess:
        if letter in answer[index:]:
            correct_letters.append(letter)
            index = answer.index(letter) + 1
    return correct_letters        

def letter_placement(guess: list, same_letters: list):
    """ Returns guess list with infomation about the placement of each letter """
    """ same_letters is alphabetical list of same words """
    guess_temp = guess[:]
 
    for letter in same_letters:          
        if letter == answer[guess_temp.index(letter)]:
            guess_temp[guess_temp.index(letter)] = '[bold green]' + letter + '[/]'
        else:
            guess_temp[guess_temp.index(letter)] = '[bold yellow]' + letter + '[/]'
        
    return guess_temp

def color_answer(guess: list):
    """ prints guess with coloured letters denoting correct placement """
    result = ''
    for letter in guess:
        result += letter
    return result

def input_and_check(Prompt, Error):
    """ Checks input is correct and asks for another if it is not """
    player_guess = console.input(Prompt) 
    correct_input = ( player_guess.isalpha() and 
                     len(player_guess.strip()) == 5 )
    while correct_input == False:
        console.print('[bold white on red]Error')
        player_guess =  console.input(Error).lower()
        correct_input = ( player_guess.isalpha() and 
                         len(player_guess.strip()) == 5 )
    " Adds word to word list if not present "
    if player_guess.upper() not in word_list:
         with open('windy.txt','a') as t:
             t.write('\n' + player_guess)
             
    return [ letter.capitalize() for letter in player_guess ]
                   
def remove_if_bad(answer: str):
    removal = console.input('Is this a valid word? ([bold blue]yes/no[/]) ')
    if removal == 'no':
        with open('windy.txt','r') as t:
            temp_word_list = t.read()
            temp_word_list = temp_word_list.replace(answer +'\n','')
        with open('windy.txt','w') as t:
            t.write(temp_word_list)
    return
        
def title_guesses_prompt(prompt):
    console.clear()
    console.rule("[bold blue] Wordle Knock Off", align = 'center')
    console.print('')
    console.print(Panel.fit(previous_guesses, border_style="bright_blue"), justify='center')
    if prompt == True:    
        player_guess = input_and_check('Enter a 5 digit word: ',
                                   'This isn\'t a 5 letter word, please try again: ')
        return player_guess
 
def alphab_ize(word_list):
    with open(word_list) as t:
        temp = sorted( [word.strip() for word in t] )
        temp = '\n'.join(temp)
        
    with open(word_list, 'w') as t :
        t.write(temp)

"""        
Main Game Loop
"""

""" Gather list of possible 5 letter words """
with open('windy.txt') as t:
    word_list = [word.upper().strip() for word in t]
    
    """ Choose random word as answer """
    answer = list(random.choice(word_list))
    correct_guess = False

previous_guesses = ''

with console.screen():
    
    """ Player can attempt 5 times """
    for num_try in range(1, 6):
        """ Take player input and transform into list of capital letters """
        
        player_guess = title_guesses_prompt(True)
        
        """ Assign variable of letters appearing in guess and answer """
        same_letters = compare_words(player_guess, answer)
        """ Return player guess with colour coded letters """
        result = letter_placement(player_guess, same_letters)
        """ Print of coloured word """
        result = color_answer(result)
        previous_guesses += result + '\n'
               
        if player_guess == answer:
            """ Break loop if player gets answer """
            
            correct_guess = True
            title_guesses_prompt(False)
            console.print('Correct!', style = 'bold white on blue', 
                          justify = 'center')
            break
        
    if correct_guess == False:
        title_guesses_prompt(False)
        console.print('You ran out of guesses :( ', style = 'bold white on red', 
                      justify = 'center')
        console.print('The correct word is {}!'.format(''.join(answer)))
        remove_if_bad(''.join(answer).lower())
        
        
        
    with console.status("Closing Game ...", spinner = 'point'):
        sleep(5)    
    
alphab_ize('windy.txt')  