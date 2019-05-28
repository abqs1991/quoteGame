import requests
from bs4 import BeautifulSoup
from random import choice
from os import system, name
from time import sleep

def clear():
	"""Function responsible for cleaning the console"""
	if name == 'nt':
		_ = system('cls')

def new_game():
	game = input('Do you wanna play again? (yes/no):\n>>> ')
	while game not in ('yes','y','no','n'):
		game = input('Do you wanna play again? (yes/no):\n>>> ')
	if game.lower() == 'yes' or game.lower() == 'y':
		start_game()
		return True
	print('Ok! Goodbye!')
	return False
#GAME LOGIC
def start_game(data):
	quote_data = choice(data)
	quote, author, url = quote_data.values()
	chances = 4
	while chances >= 0:
		print(f'\nWho said this: {quote}?\nYou have {chances} chances remaining.')
		guess = input('>>> ')
		if guess != author:
			chances -= 1
			res = requests.get(f'http://quotes.toscrape.com/{url}')
			soup = BeautifulSoup(res.content,'html.parser')
			born_date = soup.find(class_="author-born-date").get_text()
			born_place = soup.find(class_="author-born-location").get_text()
			bio = soup.find(class_="author-description").get_text()[:300]
			if author in bio:
				bio_sample = bio.replace(author, '*'*len(author))
			else:
				bio_sample = bio			
			if chances == 3:
				print(f'Author of this quote was born {born_date} {born_place}.')

			elif chances == 2:
				print(f"Author's first letter of first name is: {author[0]}.")

			elif chances == 1:
				print(f"Author's first letter of last name is: {author.split(' ')[1][0]}.")

			elif chances == 0:
				first_name_len = len(author.split(' ')[1])-1
				last_name_len = len(author.split(' ')[1])-1
				print(f"{author[0]}{'*'*first_name_len} {author.split(' ')[1][0]}{'*'*last_name_len} bio sample: {bio_sample}")
			else:
				print(f'Sorry, you were incorrect. Correct answer was: {author}.')
				if not new_game(): return
		else:
			print('You guessed right! Congratulations!')
			if not new_game(): return

def get_data():
	i = 1
	quotes = []
	while True:
		clear()
		#printing progress bar to the console
		progress_bar = '_'*(i-1) + '|' + '_'*(11-i)
		print(f'Generating quiz: {progress_bar}')
		#initiate response and soup
		res = requests.get(f'http://quotes.toscrape.com/page/{i}')
		soup = BeautifulSoup(res.content,'html.parser')

		#check if soup reached last page
		end_info = soup.div.findAll(class_='row')[1].get_text()
		if 'No quotes found!' in end_info: break
		# if end_info.get_text() == 'No quotes found!': break

		# print(end_info.get_text())
		#look for all div elements with class "quote"
		divs = soup.findAll("div", {"class": "quote"})

		#loop through each element with "quote" class and extract
		# quote, author and url and append it to the list
		for el in divs:
			quote = el.find("span", class_="text").get_text()
			author = el.find(class_="author").get_text()
			url = el.find('a')['href']
			entry = {'quote':quote,'author':author,'url':url}
			quotes.append(entry)
		i += 1
	return quotes

#game

data = get_data()
clear()
start_game(data)
